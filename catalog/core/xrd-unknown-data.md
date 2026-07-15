---
type: Crossplane Development Guide
title: Unknown data and collection semantics for XRD schemas
description: Choose pruning, opaque JSON, and Kubernetes list semantics deliberately in an XRD-backed XR schema.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, openapi, validation]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
source_repository: kubernetes/website
source_commit: be897babb9149b808e2ab8ed5367e5d0651b3dca
feature_state: Stable by repository default
---

# Preserve intentionally, not by accident

Kubernetes prunes fields that the structural schema does not declare.
`x-kubernetes-preserve-unknown-fields: true` preserves arbitrary JSON beneath
the marked subtree; pruning resumes beneath explicitly declared properties or
`additionalProperties`. Historical PR #5908 records a Crossplane change for
propagating this extension at `spec`; it is included as release history rather
than as proof of the current release's behavior.[1][2]

Opaque data is unsuitable for CEL constraints: unknown data preserved by the
extension is inaccessible in CEL expressions. CEL-accessible property names
must match `[a-zA-Z_.-/][a-zA-Z0-9_.-/]*`; special characters and CEL keywords
need the documented escaping rules.[3]

# Lists and maps

Set `x-kubernetes-list-type` deliberately. A `map` list is keyed by
`x-kubernetes-list-map-keys`, with unique key combinations and map-style CEL
equality. A `set` requires unique entries and has set-style equality; leaving
the type unspecified gives atomic semantics. These choices also determine
where an `oldSelf` transition rule can be placed.[4]

Use `x-kubernetes-int-or-string: true` only when an API genuinely accepts both
representations. CEL receives such a value as dynamic and can branch on
`type(value)`.[5]

# Citations

[1] [Kubernetes pruning and preserved unknown fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L394-L465)
[2] [PR #5908](https://github.com/crossplane/crossplane/pull/5908)
[3] [Kubernetes CEL access to schema-known fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1019-L1055)
[4] [Kubernetes list and CEL semantics](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1070-L1087)
[5] [Kubernetes `IntOrString` schema support](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L467-L505)
