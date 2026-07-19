from __future__ import annotations

import asyncio
import os
import tempfile
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any

from mcp.server.transport_security import TransportSecuritySettings
from okf_mcp import server as upstream
from starlette.requests import Request
from starlette.responses import JSONResponse

from fetch_cache import FetchCache
from git_source import GitSourceCache
from github_source import GitHubSourceClient
from provider_crd_tools import ProviderCRDTools


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean, received {raw!r}")


def env_csv(name: str) -> list[str]:
    return [value.strip() for value in os.getenv(name, "").split(",") if value.strip()]


def env_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as error:
        raise ValueError(
            f"{name} must be a positive integer, received {raw!r}"
        ) from error
    if value < 1:
        raise ValueError(f"{name} must be a positive integer, received {raw!r}")
    return value


async def run_blocking(
    function: Callable[..., dict[str, Any]], *args: object
) -> dict[str, Any]:
    """Run blocking source work outside the Streamable HTTP event loop."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(blocking_work_pool, partial(function, *args))


def ensure_writable_directory(path: Path) -> Path:
    """Create and verify the directory used for persistent source snapshots."""
    probe_path: Path | None = None
    try:
        path.mkdir(parents=True, exist_ok=True)
        descriptor, probe = tempfile.mkstemp(prefix=".write-probe-", dir=path)
        os.close(descriptor)
        probe_path = Path(probe)
    except OSError as error:
        raise RuntimeError(f"CACHE_DIR must be writable: {path}") from error
    finally:
        if probe_path is not None:
            probe_path.unlink(missing_ok=True)
    return path


db_path = Path(os.environ.get("DB_PATH", "/data/catalog.duckdb")).resolve()
cache_dir = ensure_writable_directory(
    Path(os.environ.get("CACHE_DIR", "/data/cache")).resolve()
)
bundle_name = os.environ.get("BUNDLE_NAME", "crossplane-v2-okf")
blocking_work_pool = ThreadPoolExecutor(
    max_workers=env_positive_int("MCP_BLOCKING_WORKERS", 4),
    thread_name_prefix="mcp-source",
)
fetch_cache = FetchCache(
    ttl_seconds=float(os.environ.get("FETCH_CACHE_TTL_SECONDS", "300")),
    max_entries=int(os.environ.get("FETCH_CACHE_MAX_ENTRIES", "512")),
)
git_source_cache = GitSourceCache(
    cache_dir=cache_dir,
    timeout=float(os.environ.get("GITHUB_GIT_TIMEOUT", "30")),
    git_base_url=os.environ.get("GITHUB_GIT_URL", "https://github.com"),
)
github_source = GitHubSourceClient(
    base_url=os.environ.get("GITHUB_API_URL", "https://api.github.com"),
    timeout=float(os.environ.get("GITHUB_API_TIMEOUT", "15")),
    cache=fetch_cache,
    token=os.environ.get("GITHUB_TOKEN"),
    source_cache=git_source_cache,
)
provider_crds = ProviderCRDTools(
    github_source,
    github_raw_url=os.environ.get(
        "GITHUB_RAW_URL", "https://raw.githubusercontent.com"
    ),
    timeout=float(os.environ.get("GITHUB_API_TIMEOUT", "15")),
    cache=fetch_cache,
    token=os.environ.get("GITHUB_TOKEN"),
    source_cache=git_source_cache,
)

if not db_path.is_file():
    raise RuntimeError(f"DuckDB catalog does not exist: {db_path}")

upstream.reg.add(bundle_name, str(db_path))

mcp = upstream.mcp
mcp.settings.host = os.environ.get("MCP_HOST", "0.0.0.0")
mcp.settings.port = int(os.environ.get("MCP_PORT", "8000"))
mcp.settings.streamable_http_path = os.environ.get("MCP_PATH", "/mcp")
mcp.settings.json_response = env_bool("MCP_JSON_RESPONSE", True)
mcp.settings.stateless_http = env_bool("MCP_STATELESS_HTTP", True)

allowed_hosts = env_csv("MCP_ALLOWED_HOSTS")
allowed_origins = env_csv("MCP_ALLOWED_ORIGINS")
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=bool(allowed_hosts),
    allowed_hosts=allowed_hosts,
    allowed_origins=allowed_origins,
)


@mcp.tool()
async def get_versions(name: str) -> dict[str, Any]:
    """Resolve an OSS source and list its available versions.

    The name can be a short package name such as ``provider-aws`` or
    ``function-go-templating``, an ``account/package`` reference, or a full
    ``xpkg.upbound.io/account/package:version`` reference. The returned
    ``provider`` is the canonical OSS GitHub repository. Pass that value to
    the provider CRD tools with ``versions.latest`` or a listed recent stable
    version. Counts summarize additional historical and prerelease tags.
    """
    return await run_blocking(github_source.get_versions, name)


@mcp.tool()
async def provider_crd_search(
    provider_name: str,
    provider_version: str,
    crd_search_term: str,
) -> dict[str, Any]:
    """Search CRDs in one explicit provider package version.

    The search term is a case-insensitive shell wildcard matched against the
    group, kind, group/kind, and Kind.group identities.
    """
    return await run_blocking(
        provider_crds.search, provider_name, provider_version, crd_search_term
    )


@mcp.tool()
async def provider_crd_get_definition(
    provider_name: str,
    provider_version: str,
    crd_name: str,
    path: str | None = None,
) -> dict[str, Any]:
    """Get one provider CRD definition as YAML from an explicit package version.

    ``crd_name`` accepts Kind, group/Kind, group/version/Kind, or a YAML fragment
    containing apiVersion and kind. Optionally select a subtree with a dotted
    path such as ``.spec`` or ``.spec.versions[0]``.
    """
    return await run_blocking(
        provider_crds.get_definition, provider_name, provider_version, crd_name, path
    )


@mcp.tool()
async def provider_crd_get_examples(
    provider_name: str,
    provider_version: str,
    crd_name: str,
) -> dict[str, Any]:
    """Get all matching YAML examples from an immutable provider source snapshot.

    Every YAML document under ``examples/`` and ``examples-generated/`` is
    considered. Each result includes the zero-based indexes of matching
    documents when a file contains multiple YAML documents. When no API version
    is included in ``crd_name``, the latest served CRD API version is selected.
    """
    return await run_blocking(
        provider_crds.get_examples, provider_name, provider_version, crd_name
    )


@mcp.tool()
async def provider_crd_get_terraform_docs(
    provider_name: str,
    provider_version: str,
    crd_name: str,
) -> dict[str, Any]:
    """Get Terraform documentation content and source metadata for an Upjet CRD.

    The provider Makefile selects the Terraform repository and version. The
    generated controller identifies the exact Terraform resource name. The
    response includes the immutable repository, ref, path, and document content.
    """
    return await run_blocking(
        provider_crds.get_terraform_docs, provider_name, provider_version, crd_name
    )


@mcp.custom_route("/healthz", methods=["GET"], include_in_schema=False)
async def healthz(_: Request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "bundle": bundle_name,
            "mcp_path": mcp.settings.streamable_http_path,
        }
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
