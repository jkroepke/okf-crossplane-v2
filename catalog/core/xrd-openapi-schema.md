---
type: Crossplane Development Guide
title: OpenAPI schemas for XRD-backed custom resources
description: Model an XR API with the structural OpenAPI v3 schema that Crossplane carries into its generated CRD.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, openapi]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: xrd-schema-passthrough-and-common-field-injection
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1196-L1211'
    title: 'XRD schema passthrough and common-field injection'
  - id: kubernetes-structural-schema-requirements-and-exceptions
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L197-L220'
    title: 'Kubernetes structural schema requirements and exceptions'
  - id: kubernetes-object-maps-and-additionalproperties-constraints
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L587-L609'
    title: 'Kubernetes object maps and additionalProperties constraints'
  - id: kubernetes-crd-schema-enum-example
    resource: 'https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1227-L1233'
    title: 'Kubernetes CRD schema enum example'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
feature_state: Stable by repository default
feature_state_basis: The guidance inherits the selected stable XRD and Kubernetes CRD API surfaces; the authoring procedure has no independent maturity.
---

# Overview

An XRD is a Crossplane definition that generates an XR CRD. Put the XR API's
schema at `spec.versions[*].schema.openAPIV3Schema`; Crossplane uses it for
validation, pruning, and defaulting, then injects the common XR fields. A
supplied field with a common XR name is overridden, so model only your API's
fields.[^xrd-schema-passthrough-and-common-field-injection]

# Structural schema guidance

The carried schema follows Kubernetes structural OpenAPI v3 rules: declare
types for the root, object fields/maps, and array items. The notable schema
extensions are `x-kubernetes-int-or-string` for a scalar that deliberately
accepts either type and `x-kubernetes-preserve-unknown-fields` for opaque JSON
subtrees.[^kubernetes-structural-schema-requirements-and-exceptions]

Use `required` for fields that must be present. For maps, use
`additionalProperties` with a value schema; Kubernetes does not permit
`additionalProperties: false`, nor mixing it with `properties` on one schema
node.[^kubernetes-object-maps-and-additionalproperties-constraints] See [unknown data and collections](xrd-unknown-data.md) before making
a field opaque or selecting list semantics, and [CEL validation](xrd-cel-validation.md)
for constraints across declared fields.

# Region as a constrained product choice

Do not expose a provider region in an XR API by default. Select it in the
Composition when location is a platform implementation decision. If the
human-orderable product genuinely needs a location choice, model a
service-level `region` field and constrain it to the platform's approved
locations with an OpenAPI `enum`.

```yaml
spec:
  region:
    type: string
    description: Approved deployment location for this service.
    enum:
      - eu-central-1
      - eu-west-1
```

The values are illustrative: choose the allowlist for the selected provider,
account boundary, data-residency policy, and service capability. Do not treat
an unrestricted provider-region string as a default XR API field. This is a
platform API design recommendation; Crossplane permits an XRD schema to model
other choices when the product intentionally supports them.[^kubernetes-crd-schema-enum-example]

[^xrd-schema-passthrough-and-common-field-injection]: [XRD schema passthrough and common-field injection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1196-L1211)
[^kubernetes-structural-schema-requirements-and-exceptions]: [Kubernetes structural schema requirements and exceptions](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L197-L220)
[^kubernetes-object-maps-and-additionalproperties-constraints]: [Kubernetes object maps and `additionalProperties` constraints](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L587-L609)
[^kubernetes-crd-schema-enum-example]: [Kubernetes CRD schema `enum` example](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions.md#L1227-L1233)
