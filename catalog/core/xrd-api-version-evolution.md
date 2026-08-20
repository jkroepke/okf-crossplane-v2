---
type: Crossplane Development Guide
title: XRD API version evolution and conversion
description: Evolve an XR API by separating serving and storage concerns, with CRD conversion boundaries made explicit.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, api-version, conversion]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: xrd-v2-version-and-referenceable-fields
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L162-L177'
    title: 'XRD v2 version and referenceable fields'
  - id: v2-3-3-crd-renderer
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L158-L172'
    title: 'v2.3.3 CRD renderer'
  - id: kubernetes-served-and-storage-version-rules
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L103-L146'
    title: 'Kubernetes served and storage version rules'
  - id: kubernetes-conversion-choices
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L42-L61'
    title: 'Kubernetes conversion choices'
  - id: kubernetes-webhook-conversion-configuration
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L453-L522'
    title: 'Kubernetes webhook conversion configuration'
crossplane_release: v2.3.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
feature_state: Stable by repository default
feature_state_basis: The guidance inherits the selected stable XRD and Kubernetes CRD API surfaces; the authoring procedure has no independent maturity.
---

# XRD version mapping

For an XRD version, `served` controls whether the XR endpoint is offered.
Exactly one XRD version is `referenceable`; it must be served and maps to the
generated CRD storage version.[^xrd-v2-version-and-referenceable-fields] `storage` is therefore not an XRD-version
input. For example, an XRD version with `name: v1alpha1`, `served: true`, and
`referenceable: true` is rendered as a generated CRD version with
`name: v1alpha1`, `served: true`, and `storage: true`.[^v2-3-3-crd-renderer] A safe early
API-design convention is to name
an experimental first version `v1alpha1`; this is a project convention, not a
Kubernetes requirement. It should communicate an intentionally unstable API,
not substitute for a migration plan.

A CRD can continue serving a non-storage version with `served: true` and
`storage: false`. Kubernetes requires exactly one storage version.[^kubernetes-served-and-storage-version-rules]

# Schema changes and conversion

Use compatible schema evolution where possible. If two served schemas require
custom conversion, Kubernetes supports a conversion webhook; the webhook is
configured with `strategy: Webhook`, supported ConversionReview versions, and
a service or URL client configuration. With `None` conversion, Kubernetes only
changes `apiVersion`.[^kubernetes-conversion-choices][^kubernetes-webhook-conversion-configuration]

The versioning mechanism is Kubernetes CRD behavior. Verify the generated CRD
and test conversions before promising compatibility to XR consumers.

[^xrd-v2-version-and-referenceable-fields]: [XRD v2 version and referenceable fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L162-L177)
[^v2-3-3-crd-renderer]: [v2.3.3 CRD renderer](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L158-L172)
[^kubernetes-served-and-storage-version-rules]: [Kubernetes served and storage version rules](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L103-L146)
[^kubernetes-conversion-choices]: [Kubernetes conversion choices](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L42-L61)
[^kubernetes-webhook-conversion-configuration]: [Kubernetes webhook conversion configuration](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md#L453-L522)
