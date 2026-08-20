---
type: function
title: function-environment-configs
description: Retrieve and merge EnvironmentConfig resources into Composition function pipeline context.
resource: https://github.com/crossplane-contrib/function-environment-configs
tags: [crossplane, function, environment-config, composition]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: package-description-and-context-key
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/crossplane.yaml#L10-L20'
    title: 'Package description and context key'
  - id: package-crossplane-version-constraint-and-capability
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/crossplane.yaml#L21-L25'
    title: 'Package Crossplane version constraint and capability'
  - id: readme-crossplane-2-x-warning
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/README.md#L5-L7'
    title: 'README Crossplane 2.x warning'
source_repository: crossplane-contrib/function-environment-configs
source_tag: v0.7.2
source_commit: 5589092483aea1d65b9988f5116106585c4b516b
source_paths: [README.md, package/crossplane.yaml, go.mod]
feature_state: Not stated by selected sources
---

# Overview

`function-environment-configs` is a Composition Function that requests
cluster-scoped [EnvironmentConfig](../../core/environment-config.md) resources,
merges their data, and writes the result to pipeline context at
`apiextensions.crossplane.io/environment`.[^package-description-and-context-key]

The selected stable release is v0.7.2 at
`5589092483aea1d65b9988f5116106585c4b516b`; v0.7.1 is pinned at
`054a6b8d08ae3e0c957a0e75359b14f88340ca39`.

# Compatibility and placement

Package metadata and the README require Crossplane `>=v2.0.0-0`; do not deploy this release on Crossplane 1.x.[^package-crossplane-version-constraint-and-capability][^readme-crossplane-2-x-warning]

Place it before every step that needs the merged environment. Typical consumers are:

- [function-go-templating Environment source](../function-go-templating/environment-source.md), direct `.context` reads, or Alpha Context updates;
- [function-auto-ready CEL customizations](../function-auto-ready/cel-health-checks.md) loaded from an environment context path.

Package maturity is **Not stated by selected sources**. Its separate
[Input API](input.md) is Beta; that served version does not label the whole
Function package.

# Limitations

- Build-time module versions do not establish a broader compatibility guarantee than the package's explicit Crossplane constraint.

[^package-description-and-context-key]: [Package description and context key](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/crossplane.yaml#L10-L20)
[^package-crossplane-version-constraint-and-capability]: [Package Crossplane version constraint and capability](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/crossplane.yaml#L21-L25)
[^readme-crossplane-2-x-warning]: [README Crossplane 2.x warning](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/README.md#L5-L7)
