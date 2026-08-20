---
type: Crossplane Development Guide
title: CEL validation for XRD-backed custom resources
description: Apply Kubernetes CEL validation to declared XR schema data and account for Crossplane's root-rule release boundary.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, cel, validation]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: kubernetes-cel-validation-scope
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L783-L933'
    title: 'Kubernetes CEL validation scope'
  - id: kubernetes-cel-diagnostic-fields
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1096-L1181'
    title: 'Kubernetes CEL diagnostic fields'
  - id: kubernetes-cel-transition-rules
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1221-L1254'
    title: 'Kubernetes CEL transition rules'
  - id: selected-renderer-root-rule-forwarding
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L174-L185'
    title: 'Selected renderer root-rule forwarding'
  - id: released-final-rule-and-metadata-name-test
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd_test.go#L1994-L2104'
    title: 'Released final-rule and metadata-name test'
  - id: generated-metadata-schema-retains-only-name
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L186-L196'
    title: 'Generated metadata schema retains only name'
  - id: core-definition-controller-renderer-and-crd-apply-path
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L236-L263'
    title: 'Core definition-controller renderer and CRD apply path'
  - id: apply
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L475-L497'
    title: 'apply'
  - id: xrd-v2-served-and-shared-storage-boundary
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L698-L712'
    title: 'XRD v2 served and shared storage boundary'
  - id: v2-flags
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1367-L1370'
    title: 'v2 flags'
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
generated CRD schema.[^kubernetes-cel-validation-scope] This is a Kubernetes capability, not by itself proof
that every XRD-authored root rule and metadata path survives Crossplane's
renderer. Rules only see schema-known data; [preserved unknown data](xrd-unknown-data.md)
is not CEL-accessible.

For diagnostics, `messageExpression` must produce a string and supersedes
`message` when it succeeds; `message` remains the fallback. `reason` is a
machine-readable reason and `fieldPath` is a relative, schema-scoped JSON path
that cannot index an array numerically.[^kubernetes-cel-diagnostic-fields]

A rule referring to `oldSelf` is a transition rule: it compares an update's
old and new value. Put it only on correlatable schema portions; array parents
need a map-list rather than an atomic or set list.[^kubernetes-cel-transition-rules]

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
`self.metadata.name` survives in the final generated CRD.[^selected-renderer-root-rule-forwarding][^released-final-rule-and-metadata-name-test][^generated-metadata-schema-retains-only-name]

The selected Core definition controller uses that renderer, and the XRD CRD
serves v2 through the shared stored representation.[^core-definition-controller-renderer-and-crd-apply-path][^apply][^xrd-v2-served-and-shared-storage-boundary][^v2-flags] This corroborates the
current code path, but no selected-release v2-specific API-server admission or
end-to-end test establishes acceptance and enforcement through the XRD v2
endpoint. Treat end-to-end v2 root-rule behavior as unproven.

Do not infer support for arbitrary `metadata.labels`. The renderer emits only
`metadata.name`, and no selected-release API-server test establishes a
label-dependent rule. Use an admission policy for label-dependent validation
unless a current-v2 generated-CRD and API-server test proves the exact path.[^generated-metadata-schema-retains-only-name]

[^kubernetes-cel-validation-scope]: [Kubernetes CEL validation scope](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L783-L933)
[^kubernetes-cel-diagnostic-fields]: [Kubernetes CEL diagnostic fields](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1096-L1181)
[^kubernetes-cel-transition-rules]: [Kubernetes CEL transition rules](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1221-L1254)
[^selected-renderer-root-rule-forwarding]: [Selected renderer root-rule forwarding](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L174-L185)
[^released-final-rule-and-metadata-name-test]: [Released final-rule and metadata-name test](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd_test.go#L1994-L2104)
[^generated-metadata-schema-retains-only-name]: [Generated metadata schema retains only `name`](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L186-L196)
[^core-definition-controller-renderer-and-crd-apply-path]: [Core definition-controller renderer and CRD apply path](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L236-L263) and [apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L475-L497)
[^apply]: [apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L475-L497)
[^xrd-v2-served-and-shared-storage-boundary]: [XRD v2 served and shared storage boundary](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L698-L712) and [v2 flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1367-L1370)
[^v2-flags]: [v2 flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1367-L1370)
