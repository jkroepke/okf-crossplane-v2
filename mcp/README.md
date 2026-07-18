# Crossplane v2 OKF MCP server

This `uv`-managed Python application serves the Crossplane v2 Open Knowledge
Format catalog and provides read-only provider package and CRD tools.

It is intentionally not a distributable Python package: the server retains its
small, flat module layout and is deployed by the repository's container image.

## GitHub authentication

Set `GITHUB_TOKEN` to authenticate GitHub API and raw-source requests. This is
optional; without it, the server continues to use unauthenticated requests.

## Development

Run commands from this directory:

```shell
uv sync
uv run python -m unittest discover -s tests -v
uv run ty check .
uv run ruff check .
uv run ruff format --check .
```

To refresh the resolved dependency versions after changing `pyproject.toml`, run
`uv lock` and commit the resulting `uv.lock`.
