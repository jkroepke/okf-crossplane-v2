[![CI](https://github.com/jkroepke/okf-crossplane-v2/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/jkroepke/okf-crossplane-v2/actions/workflows/ci.yaml)
[![GitHub license](https://img.shields.io/github/license/jkroepke/okf-crossplane-v2)](https://github.com/jkroepke/okf-crossplane-v2/blob/main/LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/jkroepke/okf-crossplane-v2?style=flat&logo=github)](https://github.com/jkroepke/okf-crossplane-v2/stargazers)
[![BundleDex](https://bundledex.net/badge/okf-crossplane-v2.svg)](https://bundledex.net/bundles/okf-crossplane-v2/)

# Open Knowledge Format for Crossplane v2

This repository provides a structured knowledge catalog for the Crossplane v2 ecosystem using the [Open Knowledge Format](https://okf.md/spec/).

The goal is to make Crossplane concepts, APIs, providers, composition functions, documentation, and practical examples easier to discover and understand. The catalog is designed for both humans and knowledge-aware tools.

## Installation

> [!WARNING]
> The public MCP server is a temporary early-access service for early adopters. Its availability is not guaranteed, and it may change or be removed without notice. It is intended to bridge the current tooling gap until the OKF ecosystem provides practical, end-user-friendly solutions that run locally. For reliable or production use, self-host the included container.

Install the hosted OKF-aware MCP server globally for your detected agent:

```shell
npx add-mcp \
  https://crossplane.mcp.jkroepke.de/mcp \
  --name crossplane-v2-okf \
  --global
```

Install the companion skill so the agent prefers this bundle over generic documentation providers for Crossplane v2 questions:

```shell
npx skills add jkroepke/okf-crossplane-v2 \
  --skill crossplane-v2-okf \
  --global
```

Both installers detect supported agents and ask where the integration should be installed. Restart the selected agent after installation.

The public MCP health endpoint is available at `https://crossplane.mcp.jkroepke.de/healthz`.

## Self-hosting the MCP server

The included container fetches this repository, ingests `catalog/` into a DuckDB catalog, and serves the `okf-mcp` tools over Streamable HTTP.

```shell
docker compose up --build --detach
```

The local MCP endpoint is `http://127.0.0.1:8000/mcp`. Put it behind a TLS reverse proxy for `crossplane.mcp.jkroepke.de`.

The catalog is refreshed at container startup. If fetching or ingestion fails and a previous catalog exists in the volume, the server continues with that last successful catalog.

The MCP tools are read-only, but the public endpoint has no application-level authentication. Apply request limits and access controls at the reverse proxy when required.

### Crossplane package tools

The server adds three tools backed by the public Upbound Marketplace API:

- `get_versions(name)` resolves a provider or function package and returns its latest stable version, latest published version, and available versions.
- `provider_crd_search(provider, pattern="*", version="latest", limit=100)` searches the CRDs in a provider with case-insensitive shell-style wildcards. Patterns are matched against the API group, kind, `group/kind`, and `Kind.group`.
- `provider_crd_get(provider, resource, version="latest")` returns the CRD definition for a kind or qualified `group/Kind` resource.

Package names can be short names such as `provider-aws` and `function-go-templating`, qualified names such as `crossplane-contrib/provider-aws`, or full `xpkg.upbound.io` references. Short-name resolution prefers packages published by `crossplane-contrib`, then `crossplane`, then `upbound`. Use a qualified name to select another publisher explicitly.

The default `latest` value selects the highest stable semantic version. Set an explicit version to inspect another published package version. Self-hosted deployments need outbound HTTPS access to the configured `UPBOUND_API_URL`, which defaults to `https://api.upbound.io`.

## Why this repository exists

Crossplane knowledge is distributed across many repositories and kinds of sources:

- Go API types and runtime implementations
- CustomResourceDefinitions and OpenAPI schemas
- package metadata
- tests and executable examples
- official Crossplane documentation
- community implementations and real-world composition examples

Upjet-based providers add another layer. Their Crossplane managed resources are generated from Terraform provider resources, while the Terraform documentation often contains more details about the underlying cloud APIs and configuration fields.

This repository connects these sources in one versioned catalog without replacing the original documentation.

## Knowledge structure

Knowledge is stored as small Markdown documents under [`catalog/`](catalog/index.md). Each document represents an independently useful concept and includes OKF metadata, relationships to related concepts, and citations to the original sources.

If the task is to build a Crossplane v2 Composition, start with the
[Composition developer starter guide](catalog/composition-developer-starter.md).
It connects the API, provider, function, security, readiness, identity,
testing, and packaging concepts without pretending that provider-specific
schemas or credentials are universal.

The catalog is intended to be:

- **Source-backed:** important statements link to source code, schemas, tests, examples, or official documentation.
- **Version-aware:** sources are tied to specific repository revisions.
- **Navigable:** overview documents connect related concepts without requiring readers to know the source repository layout.
- **Incremental:** providers, functions, services, documentation areas, and example repositories can be added in focused batches.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
