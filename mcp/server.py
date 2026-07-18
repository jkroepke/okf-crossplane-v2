from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from mcp.server.transport_security import TransportSecuritySettings
from okf_mcp import server as upstream
from starlette.requests import Request
from starlette.responses import JSONResponse

from fetch_cache import FetchCache
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


db_path = Path(os.environ.get("DB_PATH", "/data/catalog.duckdb")).resolve()
bundle_name = os.environ.get("BUNDLE_NAME", "crossplane-v2-okf")
fetch_cache = FetchCache(
    ttl_seconds=float(os.environ.get("FETCH_CACHE_TTL_SECONDS", "300")),
    max_entries=int(os.environ.get("FETCH_CACHE_MAX_ENTRIES", "512")),
)
github_source = GitHubSourceClient(
    base_url=os.environ.get("GITHUB_API_URL", "https://api.github.com"),
    timeout=float(os.environ.get("GITHUB_API_TIMEOUT", "15")),
    cache=fetch_cache,
    token=os.environ.get("GITHUB_TOKEN"),
)
provider_crds = ProviderCRDTools(
    github_source,
    github_raw_url=os.environ.get(
        "GITHUB_RAW_URL", "https://raw.githubusercontent.com"
    ),
    timeout=float(os.environ.get("GITHUB_API_TIMEOUT", "15")),
    cache=fetch_cache,
    token=os.environ.get("GITHUB_TOKEN"),
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
def get_versions(name: str) -> dict[str, Any]:
    """Resolve an OSS source and list its available versions.

    The name can be a short package name such as ``provider-aws`` or
    ``function-go-templating``, an ``account/package`` reference, or a full
    ``xpkg.upbound.io/account/package:version`` reference. The returned
    ``provider`` is the canonical OSS GitHub repository. Pass that value to
    the provider CRD tools with ``versions.latest`` or a listed recent stable
    version. Counts summarize additional historical and prerelease tags.
    """
    return github_source.get_versions(name)


@mcp.tool()
def provider_crd_search(
    provider_name: str,
    provider_version: str,
    crd_search_term: str,
) -> dict[str, Any]:
    """Search CRDs in one explicit provider package version.

    The search term is a case-insensitive shell wildcard matched against the
    group, kind, group/kind, and Kind.group identities.
    """
    return provider_crds.search(provider_name, provider_version, crd_search_term)


@mcp.tool()
def provider_crd_get_definition(
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
    return provider_crds.get_definition(provider_name, provider_version, crd_name, path)


@mcp.tool()
def provider_crd_get_examples(
    provider_name: str,
    provider_version: str,
    crd_name: str,
) -> dict[str, Any]:
    """Get GitHub repository paths for generated and handwritten CRD examples.

    When no API version is included in ``crd_name``, the latest served CRD API
    version is used for the example directory.
    """
    return provider_crds.get_examples(provider_name, provider_version, crd_name)


@mcp.tool()
def provider_crd_get_terraform_docs(
    provider_name: str,
    provider_version: str,
    crd_name: str,
) -> dict[str, Any]:
    """Get the Terraform documentation repository and path for an Upjet CRD.

    The provider Makefile selects the Terraform repository and version. The
    generated controller identifies the exact Terraform resource name.
    """
    return provider_crds.get_terraform_docs(provider_name, provider_version, crd_name)


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
