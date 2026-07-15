FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

ARG OKF_MCP_VERSION=0.3.0

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        ca-certificates \
        git \
        tini \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --system --no-cache "okf-mcp==${OKF_MCP_VERSION}"

RUN groupadd --gid 65532 okf \
    && useradd \
        --uid 65532 \
        --gid 65532 \
        --create-home \
        --home-dir /home/okf \
        --shell /usr/sbin/nologin \
        okf

WORKDIR /app

COPY mcp/server.py /app/server.py
COPY mcp/entrypoint.sh /app/entrypoint.sh

RUN chmod 0755 /app/entrypoint.sh \
    && mkdir -p /data \
    && chown -R okf:okf /app /data /home/okf

USER 65532:65532

ENV BUNDLE_URL="https://github.com/jkroepke/okf-crossplane-v2.git" \
    BUNDLE_REF="main" \
    BUNDLE_SUBDIR="catalog" \
    BUNDLE_NAME="crossplane-v2-okf" \
    DB_PATH="/data/catalog.duckdb" \
    MCP_HOST="0.0.0.0" \
    MCP_PORT="8000" \
    MCP_PATH="/mcp" \
    MCP_JSON_RESPONSE="true" \
    MCP_STATELESS_HTTP="true" \
    MCP_ALLOWED_HOSTS="crossplane.mcp.jkroepke.de,crossplane.mcp.jkroepke.de:*,127.0.0.1:*,localhost:*" \
    MCP_ALLOWED_ORIGINS="https://crossplane.mcp.jkroepke.de,http://127.0.0.1:*,http://localhost:*" \
    PYTHONUNBUFFERED="1" \
    UV_NO_PROGRESS="1"

VOLUME ["/data"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).close()"

ENTRYPOINT ["/usr/bin/tini", "--", "/app/entrypoint.sh"]
