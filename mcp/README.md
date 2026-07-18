# Crossplane v2 OKF MCP server

This `uv`-managed Python application serves the Crossplane v2 Open Knowledge
Format catalog and provides read-only provider package and CRD tools.

It is intentionally not a distributable Python package: the server retains its
small, flat module layout and is deployed by the repository's container image.

## GitHub authentication

Set `GITHUB_TOKEN` to authenticate GitHub API and raw-source requests. This is
optional; without it, the server continues to use unauthenticated requests.

## Provider source cache

Git tag listings use the GitHub API. Provider source files are fetched through
Git as shallow, immutable bare repositories below `CACHE_DIR` (default:
`/data/cache`), isolated by repository and requested tag. CRD definitions,
examples, and Terraform metadata are then read from that local snapshot.

Set `GITHUB_GIT_URL` (default: `https://github.com`) to use another Git host
and `GITHUB_GIT_TIMEOUT` (default: 30 seconds) to bound a Git fetch.

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
