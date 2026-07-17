from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from mcp.server.transport_security import TransportSecuritySettings
from okf_mcp import server as upstream
from starlette.requests import Request
from starlette.responses import JSONResponse

from crossplane_marketplace import MarketplaceClient


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
marketplace = MarketplaceClient(
    base_url=os.environ.get("UPBOUND_API_URL", "https://api.upbound.io"),
    timeout=float(os.environ.get("UPBOUND_API_TIMEOUT", "15")),
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
    """Get the latest stable and available versions for a provider or function.

    The name can be a short package name such as ``provider-aws`` or
    ``function-go-templating``, an ``account/package`` reference, or a full
    ``xpkg.upbound.io/account/package:version`` reference.
    """
    return marketplace.get_versions(name)


@mcp.tool()
def provider_crd_search(
    provider: str,
    pattern: str = "*",
    version: str = "latest",
    limit: int = 100,
) -> dict[str, Any]:
    """Search a provider's CRDs with a case-insensitive wildcard pattern.

    The pattern is matched against the resource group, kind, ``group/kind``,
    and ``Kind.group``. It supports shell-style wildcards such as ``*`` and
    ``?``. The latest stable provider version is used by default.
    """
    return marketplace.search_resources(provider, pattern, version, limit)


@mcp.tool()
def provider_crd_get(
    provider: str,
    resource: str,
    version: str = "latest",
) -> dict[str, Any]:
    """Get the CRD definition for one resource from a provider.

    Resource accepts a kind such as ``Bucket`` or a qualified
    ``group/Kind`` value such as ``s3.aws.upbound.io/Bucket``. Use the
    qualified form when the kind exists in more than one API group.
    """
    return marketplace.get_definitions(provider, resource, version)


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
