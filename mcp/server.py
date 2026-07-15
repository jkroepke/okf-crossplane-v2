from __future__ import annotations

import os
from pathlib import Path

from mcp.server.transport_security import TransportSecuritySettings
from okf_mcp import server as upstream
from starlette.requests import Request
from starlette.responses import JSONResponse


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
