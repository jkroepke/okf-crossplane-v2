---
type: function
title: function-auto-ready
description: A Composition Function that determines desired composed-resource readiness from observed resources.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, composition, readiness]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: readme-pipeline-example
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L149-L186'
    title: 'README pipeline example'
  - id: function-package-metadata
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/package/crossplane.yaml#L2-L22'
    title: 'Function package metadata'
  - id: selected-release-dependencies
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/go.mod#L5-L16'
    title: 'Selected release dependencies'
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [README.md, package/crossplane.yaml]
release: v0.7.0
feature_state: Not stated by selected sources
---

# Overview

`function-auto-ready` is a Composition Function. It runs after earlier pipeline steps have added desired composed resources,
compares them with observed resources, and reports the readiness it can determine. The selected catalog release is `v0.7.0`.[^readme-pipeline-example][^function-package-metadata]

The package declares only the `composition` capability. Its metadata identifies the source repository and Apache-2.0 license.[^function-package-metadata]

# Pipeline placement

Reference the installed Function by its Kubernetes object name in a later pipeline step. No function input is required for default readiness detection.[^readme-pipeline-example]

The function consumes desired resources created by preceding steps; see [readiness behavior](readiness.md). Optional response caching and CEL fields are documented in [Input](input.md).

# Version scope

This concept describes stable tag `v0.7.0`, pinned to commit `ed7886de159af73b9d6976f04f9171ec7a4cb411`. The immediately preceding stable release is `v0.6.6`, pinned to `046fe9eca400dfdb835911d8b22da9b0e27a5547`.

The repository does not state a minimum supported Crossplane version. Its Go dependency on Crossplane API modules is build-time evidence, not a user-facing compatibility guarantee.[^selected-release-dependencies]
Package maturity is **Not stated by selected sources**. The optional
[Input API](input.md) is Beta and the CEL capability is explicitly Alpha; those
states apply to their surfaces rather than labelling the package as a whole.

[^readme-pipeline-example]: [README pipeline example](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L149-L186)
[^function-package-metadata]: [Function package metadata](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/package/crossplane.yaml#L2-L22)
[^selected-release-dependencies]: [Selected release dependencies](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/go.mod#L5-L16)
