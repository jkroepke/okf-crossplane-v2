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

# Crossplane support and metadata boundary

Crossplane v2.2.0 includes PR #7018, which copies schema-root
`x-kubernetes-validations` to the generated XR CRD for the deprecated XRD v1
generator. Its release-pinned test uses `self.metadata.name` with
`self.spec.engineVersion`.[4][5] This is historical implementation evidence,
not proof that the current XRD v2 API exposes the same rule path.

Do not infer current-v2 support for `metadata.name` or arbitrary
`metadata.labels` from that legacy test. The matching runtime generator retains
only `name` in generated metadata and does not propagate source label
properties. Use an admission policy for label-dependent validation unless a
current-v2 generated-CRD and API-server test establishes the exact path.[6]

# Citations

[1] [Kubernetes CEL validation scope](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L783-L933)
[2] [Kubernetes CEL diagnostic fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1096-L1181)
[3] [Kubernetes CEL transition rules](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1221-L1254)
[4] [Crossplane v2.2.0 root-rule propagation](https://github.com/crossplane/crossplane/blob/b7aa9852801ca9959eefdad8233f95635df348c2/internal/xcrd/crd.go#L159-L220)
[5] [v2.2.0 test of `metadata.name` validation](https://github.com/crossplane/crossplane/blob/b7aa9852801ca9959eefdad8233f95635df348c2/internal/xcrd/crd_test.go#L1995-L2088)
[6] [Generated metadata schema retains only `name`](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L186-L196)
