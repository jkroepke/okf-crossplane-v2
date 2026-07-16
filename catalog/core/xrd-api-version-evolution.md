---
type: Crossplane Development Guide
title: XRD API version evolution and conversion
description: Evolve an XR API by separating serving and storage concerns, with CRD conversion boundaries made explicit.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, api-version, conversion]
timestamp: 2026-07-16T00:00:00Z
crossplane_release: v2.3.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
feature_state: Stable by repository default
---

# XRD version mapping

For an XRD version, `served` controls whether the XR endpoint is offered.
Exactly one XRD version is `referenceable`; it must be served and maps to the
generated CRD storage version.[1] `storage` is therefore not an XRD-version
input. For example, an XRD version with `name: v1alpha1`, `served: true`, and
`referenceable: true` is rendered as a generated CRD version with
`name: v1alpha1`, `served: true`, and `storage: true`.[2] A safe early
API-design convention is to name
an experimental first version `v1alpha1`; this is a project convention, not a
Kubernetes requirement. It should communicate an intentionally unstable API,
not substitute for a migration plan.

A CRD can continue serving a non-storage version with `served: true` and
`storage: false`. Kubernetes requires exactly one storage version.[3]

# Schema changes and conversion

Use compatible schema evolution where possible. If two served schemas require
custom conversion, Kubernetes supports a conversion webhook; the webhook is
configured with `strategy: Webhook`, supported ConversionReview versions, and
a service or URL client configuration. With `None` conversion, Kubernetes only
changes `apiVersion`.[4][5]

The versioning mechanism is Kubernetes CRD behavior. Verify the generated CRD
and test conversions before promising compatibility to XR consumers.

# Citations

[1] [XRD v2 version and referenceable fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L162-L177)
[2] [v2.3.3 CRD renderer](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L158-L172)
[3] [Kubernetes served and storage version rules](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L103-L146)
[4] [Kubernetes conversion choices](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L42-L61)
[5] [Kubernetes webhook conversion configuration](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L453-L522)
