---
type: concept
title: Crossplane Functions
description: Installed function packages can support composition pipelines, operation pipelines, or both.
resource: https://docs.crossplane.io/v2.3/packages/functions/
tags: [crossplane, functions, composition-functions, operation-functions]
timestamp: 2026-07-12T00:00:00Z
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

Both roles use the shared `FunctionRunnerService.RunFunction` RPC and the same installed [Function package](package.md).[1] Function package metadata defines the known capability keys `composition` and `operation`; a 
package may declare either or both.[2][3]

# Documentation boundary

The v2.3 general Functions page says it is a work in progress and describes only composition functions.[4] The v2.3 Operations documentation, released capability types, protocol, and APIs establish the broader two-role 
model, so the composition-only page must not be treated as an exhaustive taxonomy.

Whether a particular package supports one role or both must be verified from that package's immutable metadata. The historical documentation statement that only `function-python` supported operations “at launch” is 
not a current ecosystem inventory.[5]

# Citations

[1] [Shared function RPC and protocol scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L19-L35)
[2] [Released function capability keys](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/meta/v1/capabilities.go#L24-L35)
[3] [Operation documentation on composition and operation capabilities](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L94)
[4] [Incomplete, composition-only Functions page](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/functions.md#L7-L23)
[5] [Historically scoped operation-function note](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L96-L101)
