---
type: concept
title: Composition functions
description: Functions that continuously reconcile composite resources through ordered Composition pipelines.
resource: https://docs.crossplane.io/v2.3/composition/compositions/
tags: [crossplane, composition-functions, stable]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: composition-invocation-and-deletion-behavior
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L65-L78'
    title: 'Composition invocation and deletion behavior'
  - id: deletion
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L139-L148'
    title: 'deletion'
  - id: released-composition-api
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L32'
    title: 'Released Composition API'
  - id: request-response-and-accumulated-desired-state
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L601-L631'
    title: 'Request, response, and accumulated desired state'
  - id: preservation-requirement
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L698-L709'
    title: 'preservation requirement'
  - id: bootstrap-and-dynamic-requirements
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L795-L812'
    title: 'Bootstrap and dynamic requirements'
  - id: iteration-limit
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L956-L969'
    title: 'iteration limit'
  - id: composition-pipeline-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L100-L258'
    title: 'Composition pipeline schema'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositions.yaml
  - proto/fn/v1/run_function.proto
feature_state: Stable by repository default
feature_state_basis: Stable applies to the owning Composition API; unlabelled Function runtime behavior has no separate maturity assignment.
---

# Overview

A composition function runs as a step in an ordered `Composition` pipeline whenever Crossplane reconciles a new or updated XR. Composition functions do not run during XR deletion.[^composition-invocation-and-deletion-behavior][^deletion]

The `Composition` API is served and stored as non-deprecated `apiextensions.crossplane.io/v1`. With no selected non-stable label or relevant served alpha or beta API, this role is **Stable by repository default**; `v1` 
alone is not used as proof.[^released-composition-api]

# Behavior

Each request contains observed state, the desired state accumulated by earlier steps, optional typed input, and pipeline context. Responses primarily update desired state. A function must preserve desired resources 
returned by prior steps when they should remain managed.[^request-response-and-accumulated-desired-state][^preservation-requirement]

Functions can receive bootstrap requirements or dynamically request resources. Dynamic requests may iterate up to five times and must stabilize.[^bootstrap-and-dynamic-requirements][^iteration-limit]

The Composition schema permits 1–99 uniquely named steps. Each step requires `functionRef.name` and may include credentials, input, required resources, and required schemas.[^composition-pipeline-schema]

# Relationships

Composition functions use the shared [Function package](package.md) and protocol, but differ from [operation functions](operation-functions.md) in invocation and state semantics. 
[function-go-templating](function-go-templating/index.md) is a release-pinned composition-function example.

The v2.3.3 [Composition Functions specification](composition-function-specification.md) defines normative implementation requirements, while runtime behavior remains separately evidenced.

[^composition-invocation-and-deletion-behavior]: [Composition invocation and deletion behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L65-L78) and [deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L139-L148)
[^deletion]: [deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L139-L148)
[^released-composition-api]: [Released Composition API](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L32)
[^request-response-and-accumulated-desired-state]: [Request, response, and accumulated desired state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L601-L631) and [preservation requirement](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L698-L709)
[^preservation-requirement]: [preservation requirement](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L698-L709)
[^bootstrap-and-dynamic-requirements]: [Bootstrap and dynamic requirements](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L795-L812) and [iteration limit](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L956-L969)
[^iteration-limit]: [iteration limit](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L956-L969)
[^composition-pipeline-schema]: [Composition pipeline schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L100-L258)
