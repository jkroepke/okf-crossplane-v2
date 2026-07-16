---
type: concept
title: Composition functions
description: Functions that continuously reconcile composite resources through ordered Composition pipelines.
resource: https://docs.crossplane.io/v2.3/composition/compositions/
tags: [crossplane, composition-functions, stable]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositions.yaml
  - proto/fn/v1/run_function.proto
feature_state: Stable by repository default
feature_state_basis: Stable applies to the owning Composition API; unlabelled Function runtime behavior has no separate maturity assignment.
---

# Overview

A composition function runs as a step in an ordered `Composition` pipeline whenever Crossplane reconciles a new or updated XR. Composition functions do not run during XR deletion.[1]

The `Composition` API is served and stored as non-deprecated `apiextensions.crossplane.io/v1`. With no selected non-stable label or relevant served alpha or beta API, this role is **Stable by repository default**; `v1` 
alone is not used as proof.[2]

# Behavior

Each request contains observed state, the desired state accumulated by earlier steps, optional typed input, and pipeline context. Responses primarily update desired state. A function must preserve desired resources 
returned by prior steps when they should remain managed.[3]

Functions can receive bootstrap requirements or dynamically request resources. Dynamic requests may iterate up to five times and must stabilize.[4]

The Composition schema permits 1–99 uniquely named steps. Each step requires `functionRef.name` and may include credentials, input, required resources, and required schemas.[5]

# Relationships

Composition functions use the shared [Function package](package.md) and protocol, but differ from [operation functions](operation-functions.md) in invocation and state semantics. 
[function-go-templating](function-go-templating/index.md) is a release-pinned composition-function example.

The v2.3.3 [Composition Functions specification](composition-function-specification.md) defines normative implementation requirements, while runtime behavior remains separately evidenced.

# Citations

[1] [Composition invocation and deletion behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L65-L78) and 
[deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L139-L148)
[2] [Released Composition API](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L32)
[3] [Request, response, and accumulated desired state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L601-L631) and [preservation 
requirement](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L698-L709)
[4] [Bootstrap and dynamic requirements](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L795-L812) and [iteration 
limit](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L956-L969)
[5] [Composition pipeline schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L100-L258)
