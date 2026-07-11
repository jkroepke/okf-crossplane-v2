# Open Knowledge Format for Crossplane v2

This repository provides a structured knowledge catalog for the Crossplane v2 ecosystem using the [Open Knowledge Format](https://okf.md/spec/).

The goal is to make Crossplane concepts, APIs, providers, composition functions, development tools, documentation, and practical examples easier to discover and understand. The catalog is designed for both humans and knowledge-aware tools.

## Why this repository exists

Crossplane knowledge is distributed across many repositories and different kinds of sources:

- Go API types and runtime implementations
- CustomResourceDefinitions and OpenAPI schemas
- package metadata
- tests and executable examples
- official Crossplane documentation
- community implementations and real-world composition examples

Upjet-based providers add another layer. Their Crossplane managed resources are generated from Terraform provider resources, while the Terraform documentation often contains more details about the underlying cloud APIs and configuration fields.

This repository connects these sources in one versioned catalog without replacing the original documentation.

## Scope

The catalog covers:

- Crossplane core concepts and APIs
- the Crossplane CLI and development tools
- provider development with `crossplane-runtime`
- composition function development with `function-sdk-go`
- common composition functions and testing tools
- native providers such as `provider-kubernetes` and `provider-helm`
- Upjet-based AWS and Azure providers
- relationships between Upjet managed resources and their Terraform provider resources
- versioned guidance from the official Crossplane documentation
- selected community repositories that demonstrate practical Crossplane patterns

## Knowledge structure

Knowledge is stored as small Markdown documents under `catalog/`. Each document represents an independently useful concept and includes OKF metadata, relationships to related concepts, and citations to the original sources.

The catalog is intended to be:

- **Source-backed:** important statements link to source code, schemas, tests, examples, or official documentation.
- **Version-aware:** sources are tied to specific repository revisions.
- **Navigable:** overview documents connect related concepts without requiring readers to know the source repository layout.
- **Incremental:** providers, functions, services, documentation areas, and example repositories can be added in focused batches.

## Documentation and community examples

The official Crossplane documentation is used for versioned terminology, guidance, supported workflows, and user-facing examples.

Community repositories may be included to show practical platform and composition patterns. These examples are clearly identified as third-party implementations. They are not treated as official Crossplane guidance or as proof of general Crossplane behavior.

Third-party material is summarized and linked by default. Code or configuration is copied or adapted only when its license allows reuse and the original source is attributed.

## Upjet and Terraform resources

For Upjet providers, a relationship between a Crossplane managed resource and a Terraform resource is documented only when it can be traced through the provider configuration or generated metadata.

The catalog also describes Crossplane-specific behavior that is not part of the Terraform resource, such as references, selectors, provider configuration, management policies, late initialization, external names, and connection details.

## Project status

The catalog is built incrementally. Initial work focuses on the common Crossplane concepts, development libraries, composition functions, official documentation, selected community examples, and representative providers before expanding into individual cloud services and managed resources.

## Disclaimer

This is an independent community project. It is not official Crossplane documentation and does not replace the documentation of Crossplane, its providers, or the underlying Terraform providers.
