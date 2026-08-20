---
type: concept
title: Crossplane Functions
description: Installed function packages can support composition pipelines, operation pipelines, or both.
resource: https://docs.crossplane.io/v2.3/packages/functions/
tags: [crossplane, functions, composition-functions, operation-functions]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: shared-function-rpc-and-protocol-scope
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L19-L35'
    title: 'Shared function RPC and protocol scope'
  - id: released-function-capability-keys
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/meta/v1/capabilities.go#L24-L35'
    title: 'Released function capability keys'
  - id: operation-documentation-on-composition-and-operation-capabilities
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L94'
    title: 'Operation documentation on composition and operation capabilities'
  - id: incomplete-composition-only-functions-page
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/functions.md#L7-L23'
    title: 'Incomplete, composition-only Functions page'
  - id: historically-scoped-operation-function-note
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L96-L101'
    title: 'Historically scoped operation-function note'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - proto/fn/v1/run_function.proto
  - apis/pkg/meta/v1/capabilities.go
---

# Overview

Crossplane has two function roles:

| Role | Invocation model | Primary state model | Feature state in Crossplane v2.3.3 |
|---|---|---|---|
| [Composition function](composition-functions.md) | Continuously reconciled as an ordered `Composition` pipeline for an XR | Observed and desired composite and composed resources | Stable by repository default |
| [Operation function](operation-functions.md) | Run once to completion by an `Operation`, directly or through a schedule or watch | Required resources and arbitrary output resources | Alpha |

Both roles use the shared `FunctionRunnerService.RunFunction` RPC and the same installed [Function package](package.md).[^shared-function-rpc-and-protocol-scope] Function package metadata defines the known capability keys `composition` and `operation`; a
package may declare either or both.[^released-function-capability-keys][^operation-documentation-on-composition-and-operation-capabilities]

# Documentation boundary

The v2.3 general Functions page says it is a work in progress and describes only composition functions.[^incomplete-composition-only-functions-page] The v2.3 Operations documentation, released capability types, protocol, and APIs establish the broader two-role
model, so the composition-only page must not be treated as an exhaustive taxonomy.

Whether a particular package supports one role or both must be verified from that package's immutable metadata. The historical documentation statement that only `function-python` supported operations “at launch” is
not a current ecosystem inventory.[^historically-scoped-operation-function-note]

[^shared-function-rpc-and-protocol-scope]: [Shared function RPC and protocol scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L19-L35)
[^released-function-capability-keys]: [Released function capability keys](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/meta/v1/capabilities.go#L24-L35)
[^operation-documentation-on-composition-and-operation-capabilities]: [Operation documentation on composition and operation capabilities](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L94)
[^incomplete-composition-only-functions-page]: [Incomplete, composition-only Functions page](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/functions.md#L7-L23)
[^historically-scoped-operation-function-note]: [Historically scoped operation-function note](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L96-L101)
