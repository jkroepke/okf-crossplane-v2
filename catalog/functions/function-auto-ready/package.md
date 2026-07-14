---
type: function
title: function-auto-ready
description: A Composition Function that determines desired composed-resource readiness from observed resources.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, composition, readiness]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [README.md, package/crossplane.yaml]
release: v0.7.0
feature_state: Stable
feature_state_basis: Stable by repository default because selected sources contain no explicit non-stable label and the core function has no relevant served alpha or beta API.
---

# Overview

`function-auto-ready` is a Composition Function. It runs after earlier pipeline steps have added desired composed resources,
compares them with observed resources, and reports the readiness it can determine. The selected catalog release is `v0.7.0`.[1][2]

The package declares only the `composition` capability. Its metadata identifies the source repository and Apache-2.0 license.[2]

# Pipeline placement

Reference the installed Function by its Kubernetes object name in a later pipeline step. No function input is required for default readiness detection.[1]

The function consumes desired resources created by preceding steps; see [readiness behavior](readiness.md). Optional response caching and CEL fields are documented in [Input](input.md).

# Version scope

This concept describes stable tag `v0.7.0`, pinned to commit `ed7886de159af73b9d6976f04f9171ec7a4cb411`. The immediately preceding stable release is `v0.6.6`, pinned to `046fe9eca400dfdb835911d8b22da9b0e27a5547`.

The repository does not state a minimum supported Crossplane version. Its Go dependency on Crossplane API modules is build-time evidence, not a user-facing compatibility guarantee.[3]

# Citations

[1] [README pipeline example](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L149-L186)
[2] [Function package metadata](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/package/crossplane.yaml#L2-L22)
[3] [Selected release dependencies](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/go.mod#L5-L16)
