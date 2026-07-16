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
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml
  - internal/controller/apiextensions/definition/reconciler.go
supporting_sources:
  - repository: crossplane/crossplane-runtime
    commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
    paths: [pkg/xcrd/crd.go, pkg/xcrd/crd_test.go, pkg/xcrd/schemas.go]
  - repository: kubernetes/website
    commit: be897babb9149b808e2ab8ed5367e5d0651b3dca
    paths:
      - content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md
feature_state: Stable by repository default
feature_state_basis: The guidance is scoped to the selected stable XRD and Kubernetes CRD API surfaces; no independent maturity is assigned to the authoring pattern.
---

# Kubernetes rule scope and Crossplane boundary

Kubernetes attaches CEL rules with `x-kubernetes-validations` to structural
schemas. At a resource root, a rule can use declared `spec` and `status`
fields as well as selected metadata fields when those fields exist in the
generated CRD schema.[1] This is a Kubernetes capability, not by itself proof
that every XRD-authored root rule and metadata path survives Crossplane's
renderer. Rules only see schema-known data; [preserved unknown data](xrd-unknown-data.md)
is not CEL-accessible.

For diagnostics, `messageExpression` must produce a string and supersedes
`message` when it succeeds; `message` remains the fallback. `reason` is a
machine-readable reason and `fieldPath` is a relative, schema-scoped JSON path
that cannot index an array numerically.[2]

A rule referring to `oldSelf` is a transition rule: it compares an update's
old and new value. Put it only on correlatable schema portions; array parents
need a map-list rather than an atomic or set list.[3]

# Admission-policy layering

Prefer the CRD/XRD's built-in OpenAPI and CEL validation for invariants that
depend only on the object being admitted: the rule travels with the API schema
and is checked before admission-policy layering is needed. This is an
organizational guidance rule, not a Kubernetes mandate. Use a
[ValidatingAdmissionPolicy](tenant-xr-api-security.md) or Kyverno when a rule
needs cluster context, such as a tenant namespace label that identifies an AWS
account, Azure subscription, or OpenStack tenant.

# Crossplane support and metadata boundary

The renderer selected by Crossplane v2.3.3 copies schema-root
`x-kubernetes-validations` to the generated XR CRD and then narrows generated
metadata to `name`. A released renderer unit test proves that a root rule using
`self.metadata.name` survives in the final generated CRD.[4][5][6]

The selected Core definition controller uses that renderer, and the XRD CRD
serves v2 through the shared stored representation.[7][8] This corroborates the
current code path, but no selected-release v2-specific API-server admission or
end-to-end test establishes acceptance and enforcement through the XRD v2
endpoint. Treat end-to-end v2 root-rule behavior as unproven.

Do not infer support for arbitrary `metadata.labels`. The renderer emits only
`metadata.name`, and no selected-release API-server test establishes a
label-dependent rule. Use an admission policy for label-dependent validation
unless a current-v2 generated-CRD and API-server test proves the exact path.[6]

# Citations

[1] [Kubernetes CEL validation scope](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L783-L933)
[2] [Kubernetes CEL diagnostic fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1096-L1181)
[3] [Kubernetes CEL transition rules](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1221-L1254)
[4] [Selected renderer root-rule forwarding](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L174-L185)
[5] [Released final-rule and metadata-name test](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd_test.go#L1994-L2104)
[6] [Generated metadata schema retains only `name`](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L186-L196)
[7] [Core definition-controller renderer and CRD apply path](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L236-L263) and [apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L475-L497)
[8] [XRD v2 served and shared storage boundary](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L698-L712) and [v2 flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1367-L1370)
