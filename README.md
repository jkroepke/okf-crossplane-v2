[![CI](https://github.com/jkroepke/okf-crossplane-v2/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/jkroepke/okf-crossplane-v2/actions/workflows/ci.yaml)
[![GitHub license](https://img.shields.io/github/license/jkroepke/okf-crossplane-v2)](https://github.com/jkroepke/okf-crossplane-v2/blob/main/LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/jkroepke/okf-crossplane-v2?style=flat&logo=github)](https://github.com/jkroepke/okf-crossplane-v2/stargazers)
[![BundleDex](https://bundledex.net/badge/okf-crossplane-v2.svg)](https://bundledex.net/bundles/okf-crossplane-v2/)
[![OKF BundleDex](https://bundledex.net/static-badge.svg)](https://bundledex.net)

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

To authenticate the server's GitHub requests, export `GITHUB_TOKEN` before
starting the container. The token is optional.

The local MCP endpoint is `http://127.0.0.1:8000/mcp`. Put it behind a TLS reverse proxy for `crossplane.mcp.jkroepke.de`.

The catalog is refreshed at container startup. If fetching or ingestion fails and a previous catalog exists in the volume, the server continues with that last successful catalog.

The MCP tools are read-only, but the public endpoint has no application-level authentication. Apply request limits and access controls at the reverse proxy when required.

### Crossplane package tools

The server adds these tools backed by OSS GitHub repositories:

- `get_versions(name)` resolves an OSS provider or function repository and returns its canonical repository name, `versions.latest`, a compact list of recent stable versions, and tag counts. Pass the returned provider name to the CRD tools.
- `provider_crd_search(provider_name, provider_version, crd_search_term)` searches CRDs in one explicit provider package version. The search term supports case-insensitive shell-style wildcards.
- `provider_crd_get_definition(provider_name, provider_version, crd_name, path?)` returns the complete CRD definition as token-efficient YAML. Use a dotted path such as `.spec` or `.spec.versions[0]` to return only a subtree.
- `provider_crd_get_examples(provider_name, provider_version, crd_name)` returns GitHub repository paths for generated and handwritten examples. Without an API version, it selects the latest served CRD API version, for example `examples-generated/namespaced/ec2/v1beta2/route.yaml`.
- `provider_crd_get_terraform_docs(provider_name, provider_version, crd_name)` returns the Terraform provider repository, version, and documentation path. It reads the Crossplane provider Makefile and the generated controller mapping instead of inferring the Terraform resource name.

`crd_name` accepts a Kind, `group/Kind`, `group/version/Kind`, or a YAML fragment containing `apiVersion` and `kind`.

Use an OSS GitHub repository name such as `crossplane-contrib/provider-upjet-aws` or `crossplane-contrib/function-go-templating`. A small set of historical package aliases is mapped to their known OSS source repositories; unmapped `upbound/...` names are rejected rather than guessed.

The CRD tools require an explicit provider version. The value `latest` is also supported and selects the highest stable semantic-version Git tag. Self-hosted deployments need outbound HTTPS access to `GITHUB_API_URL` and `GITHUB_RAW_URL`.

Successful remote fetches are cached in memory. Git tag listings use the configurable short `FETCH_CACHE_TTL_SECONDS` (default: 300 seconds); CRDs, definitions, examples, and Terraform metadata resolved at immutable Git tags are cached for 30 days. `FETCH_CACHE_MAX_ENTRIES` (default: 512) bounds memory use.

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
[Composition developer route](catalog/composition-developer-starter.md).
It routes agents through separate API/provider, pipeline/security, and
testing/packaging concepts without pretending that provider-specific schemas or
credentials are universal.

The catalog is intended to be:

- **Source-backed:** important statements link to source code, schemas, tests, examples, or official documentation.
- **Version-aware:** sources are tied to specific repository revisions.
- **Navigable:** overview documents connect related concepts without requiring readers to know the source repository layout.
- **Incremental:** providers, functions, services, documentation areas, and example repositories can be added in focused batches.

## License

This project is licensed under the [Apache License 2.0](LICENSE).