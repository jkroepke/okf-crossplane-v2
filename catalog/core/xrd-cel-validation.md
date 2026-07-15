---
type: Crossplane Development Guide
title: CEL validation for XRD-backed custom resources
description: Apply Kubernetes CEL validation to declared XR schema data and account for Crossplane's root-rule release boundary.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, cel, validation]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
feature_state: Stable by repository default
---

# Scope rules to declared schema

Kubernetes attaches CEL rules with `x-kubernetes-validations` to structural
schemas. At a resource root, a rule can use declared `spec` and `status`
fields as well as selected metadata fields.[1] Rules only see schema-known
data; [preserved unknown data](xrd-unknown-data.md) is not CEL-accessible.

For diagnostics, `messageExpression` must produce a string and supersedes
`message` when it succeeds; `message` remains the fallback. `reason` is a
machine-readable reason and `fieldPath` is a relative, schema-scoped JSON path
that cannot index an array numerically.[2]

A rule referring to `oldSelf` is a transition rule: it compares an update's
old and new value. Put it only on correlatable schema portions; array parents
need a map-list rather than an atomic or set list.[3]

# Crossplane release boundary

The v2.3.3 XRD schema accepts OpenAPI schema data, but do not rely on a
schema-root rule outside `spec` being propagated by that release. Merged PR
#7018 added copying root `x-kubernetes-validations` to the generated CRD; its
merge commit is post-v2.3.3. This enables future rules that compare, for
example, `spec` with `status` or metadata, but it is not selected-release
behavior.[4][5]

# Citations

[1] [Kubernetes CEL validation scope](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L783-L933)
[2] [Kubernetes CEL diagnostic fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1096-L1181)
[3] [Kubernetes CEL transition rules](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1221-L1254)
[4] [PR #7018](https://github.com/crossplane/crossplane/pull/7018)
[5] [Post-v2.3.3 root-validation propagation](https://github.com/crossplane/crossplane/blob/7e8d6e108b846555abdd09f60188b7adcf451495/internal/xcrd/crd.go#L175-L204)
