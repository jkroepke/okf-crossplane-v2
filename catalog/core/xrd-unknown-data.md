---
type: Crossplane Development Guide
title: Unknown data and collection semantics for XRD schemas
description: Choose pruning, opaque JSON, and Kubernetes list semantics deliberately in an XRD-backed XR schema.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, openapi, validation]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: kubernetes-pruning-and-preserved-unknown-fields
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L394-L465'
    title: 'Kubernetes pruning and preserved unknown fields'
  - id: pr-5908
    resource: 'https://github.com/crossplane/crossplane/pull/5908'
    title: 'PR #5908'
  - id: kubernetes-cel-access-to-schema-known-fields
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1019-L1055'
    title: 'Kubernetes CEL access to schema-known fields'
  - id: kubernetes-list-and-cel-semantics
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1070-L1087'
    title: 'Kubernetes list and CEL semantics'
  - id: kubernetes-intorstring-schema-support
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L467-L505'
    title: 'Kubernetes IntOrString schema support'
crossplane_release: v2.3.3
source_repository: kubernetes/website
source_commit: be897babb9149b808e2ab8ed5367e5d0651b3dca
source_paths:
  - content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md
project_history_repository: crossplane/crossplane
project_history_items: [pull/5908]
supporting_source_repository: crossplane/crossplane
supporting_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
supporting_source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml
feature_state: Stable by repository default
feature_state_basis: The guidance is scoped to the selected stable XRD and Kubernetes CRD API surfaces; no independent maturity is assigned to the authoring pattern.
project_history_researched_at: 2026-07-16T00:00:00Z
---

# Preserve intentionally, not by accident

Kubernetes prunes fields that the structural schema does not declare.
`x-kubernetes-preserve-unknown-fields: true` preserves arbitrary JSON beneath
the marked subtree; pruning resumes beneath explicitly declared properties or
`additionalProperties`. Historical PR #5908 records a Crossplane change for
propagating this extension at `spec`; it is included as release history rather
than as proof of the current release's behavior.[^kubernetes-pruning-and-preserved-unknown-fields][^pr-5908]

Opaque data is unsuitable for CEL constraints: unknown data preserved by the
extension is inaccessible in CEL expressions. CEL-accessible property names
must match `[a-zA-Z_.-/][a-zA-Z0-9_.-/]*`; special characters and CEL keywords
need the documented escaping rules.[^kubernetes-cel-access-to-schema-known-fields]

# Lists and maps

Set `x-kubernetes-list-type` deliberately. A `map` list is keyed by
`x-kubernetes-list-map-keys`, with unique key combinations and map-style CEL
equality. A `set` requires unique entries and has set-style equality; leaving
the type unspecified gives atomic semantics. These choices also determine
where an `oldSelf` transition rule can be placed.[^kubernetes-list-and-cel-semantics]

Use `x-kubernetes-int-or-string: true` only when an API genuinely accepts both
representations. CEL receives such a value as dynamic and can branch on
`type(value)`.[^kubernetes-intorstring-schema-support]

[^kubernetes-pruning-and-preserved-unknown-fields]: [Kubernetes pruning and preserved unknown fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L394-L465)
[^pr-5908]: [PR #5908](https://github.com/crossplane/crossplane/pull/5908)
[^kubernetes-cel-access-to-schema-known-fields]: [Kubernetes CEL access to schema-known fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1019-L1055)
[^kubernetes-list-and-cel-semantics]: [Kubernetes list and CEL semantics](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1070-L1087)
[^kubernetes-intorstring-schema-support]: [Kubernetes `IntOrString` schema support](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L467-L505)
