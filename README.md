[![CI](https://github.com/jkroepke/okf-crossplane-v2/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/jkroepke/okf-crossplane-v2/actions/workflows/ci.yaml)
[![GitHub license](https://img.shields.io/github/license/jkroepke/okf-crossplane-v2)](https://github.com/jkroepke/okf-crossplane-v2/blob/master/LICENSE.txt)
[![GitHub Repo stars](https://img.shields.io/github/stars/jkroepke/okf-crossplane-v2?style=flat&logo=github)](https://github.com/jkroepke/okf-crossplane-v2/stargazers)

# Open Knowledge Format for Crossplane v2

This repository provides a structured knowledge catalog for the Crossplane v2 ecosystem using the [Open Knowledge Format](https://okf.md/spec/).

The goal is to make Crossplane concepts, APIs, providers, composition functions, documentation, and practical examples easier to discover and understand. The catalog is designed for both humans and knowledge-aware tools.

## Usage

The project [UmairBaig8/okf-generator](https://github.com/UmairBaig8/okf-generator) supports an MCP server for OKF bundles.  



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

Knowledge is stored as small Markdown documents under `catalog/`. Each document represents an independently useful concept and includes OKF metadata, relationships to related concepts, and citations to the original sources.

The catalog is intended to be:

- **Source-backed:** important statements link to source code, schemas, tests, examples, or official documentation.
- **Version-aware:** sources are tied to specific repository revisions.
- **Navigable:** overview documents connect related concepts without requiring readers to know the source repository layout.
- **Incremental:** providers, functions, services, documentation areas, and example repositories can be added in focused batches.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
