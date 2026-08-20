---
type: api
title: CompositeResourceDefinition v2
description: The cluster-scoped Crossplane v2 API that defines a custom composite resource type.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, api, v2]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: xrd-crd-identity
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L7-L21'
    title: 'XRD CRD identity'
  - id: current-v2-xrd-example
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L35-L73'
    title: 'Current v2 XRD example'
  - id: xrd-names-and-group-validation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1007-L1015'
    title: 'XRD names and group validation'
  - id: xrd-scope-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1095-L1107'
    title: 'XRD scope schema'
  - id: xrd-version-fields
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1200-L1263'
    title: 'XRD version fields'
  - id: xrd-serving-and-storage-flags
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1360-L1368'
    title: 'XRD serving and storage flags'
  - id: default-composition-reference-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L925-L935'
    title: 'Default Composition reference schema'
  - id: default-composition-selection
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L298-L326'
    title: 'Default Composition selection'
  - id: default-composition-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L544-L570'
    title: 'Default Composition guidance'
  - id: default-update-policy-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L984-L992'
    title: 'Default update-policy schema'
  - id: compositionrevision-policy-behavior
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L154-L207'
    title: 'CompositionRevision policy behavior'
  - id: enforced-composition-reference-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L993-L1006'
    title: 'Enforced Composition reference schema'
  - id: enforced-composition-override
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L355-L381'
    title: 'Enforced Composition override'
  - id: enforced-composition-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L603-L627'
    title: 'Enforced Composition guidance'
  - id: xrd-scope-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L500-L530'
    title: 'XRD scope guidance'
  - id: referenceable-version-mapped-to-generated-crd-storage
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L158-L168'
    title: 'Referenceable version mapped to generated CRD storage'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml
  - apis/apiextensions/v2/xrd_types.go
  - internal/controller/apiextensions/composite/api.go
supporting_source_repository: crossplane/crossplane-runtime
supporting_source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
supporting_source_paths: [pkg/xcrd/crd.go]
documentation_repository: crossplane/docs
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths: [content/v2.3/composition/composite-resource-definitions.md]
feature_state: Stable by repository default
---

# Overview

`CompositeResourceDefinition` (XRD) is a cluster-scoped `apiextensions.crossplane.io/v2` API. It defines the group, names, scope, versions, and schemas of an XR API.[^xrd-crd-identity][^current-v2-xrd-example]

An XRD is the Crossplane definition from which Crossplane generates an XR
CustomResourceDefinition (CRD). The focused guides on [OpenAPI schemas](xrd-openapi-schema.md),
[CEL validation](xrd-cel-validation.md), [unknown data and collection semantics](xrd-unknown-data.md),
[version evolution](xrd-api-version-evolution.md), and [scale and display](xrd-subresources-and-display.md)
cover the CRD capabilities exposed through an XRD.

# Schema

The defined resource requires `names.kind` and `names.plural`.
Group and names are immutable, and plural and singular names must be lowercase.[^xrd-names-and-group-validation] Scope defaults to `Namespaced`, also permits `Cluster`, and is immutable.[^xrd-scope-schema] Each declared version requires `name`, `served`, and `referenceable`.[^xrd-version-fields] The API field contract says exactly one version must be referenceable and it must also be served; Crossplane maps that version to `storage: true` in the generated XR CRD.[^xrd-version-fields][^referenceable-version-mapped-to-generated-crd-storage]

The XRD `v2` representation is served but not stored. The CRD's stored `v1` representation is explicitly deprecated; that storage detail does not make the current v2 user API legacy.[^xrd-serving-and-storage-flags]

# Composition selection and revision policy

`spec.defaultCompositionRef` is optional and requires a Composition `name`.
It supplies the Composition only when an XR sets neither a composition reference
nor a composition selector.[^default-composition-reference-schema][^default-composition-selection] This is the documented way to set a default
when multiple Compositions reference the same XRD.[^default-composition-guidance]

`spec.defaultCompositionUpdatePolicy` is optional, defaults to `Automatic`,
and permits only `Automatic` or `Manual`. It is the fallback when an XR has no
own update policy: `Automatic` follows the revision selector after a new
CompositionRevision exists, while `Manual` retains the selected revision.[^default-update-policy-schema][^compositionrevision-policy-behavior]

`spec.enforcedCompositionRef` is optional, requires a Composition `name`, and
is immutable. When set, it replaces a different XR composition reference, so it
enforces one Composition for all XRs defined by the XRD rather than merely
providing a default.[^enforced-composition-reference-schema][^enforced-composition-override] Official v2.3 guidance describes this as requiring
all composite resources using the XRD to use the named Composition.[^enforced-composition-guidance]

Official v2.3 guidance recommends `Namespaced` for most XRDs and explains that
namespace scope confines composed resources to the XR namespace.[^xrd-scope-guidance]

# Limitations

No selected current source labels XRD v2 Alpha, Beta, Preview, or Deprecated,
and no relevant served alpha or beta API version applies. Its feature state is
therefore Stable by repository default; the `/v1` storage representation alone
is not the basis for that classification.
Claims, claim references, deprecated XRD v1 schema, legacy v1 XR semantics, and `LegacyCluster` guidance are excluded.
Some v2.3 documentation snippets use the deprecated XRD `/v1` API; they are not used as v2 schema evidence.
The selected XRD CRD does not contain a list-level CEL rule directly proving
admission enforcement of the unique-referenceable contract; the field
description and released generator establish the declared contract and mapping.

[^xrd-crd-identity]: [XRD CRD identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L7-L21)
[^current-v2-xrd-example]: [Current v2 XRD example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L35-L73)
[^xrd-names-and-group-validation]: [XRD names and group validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1007-L1015)
[^xrd-scope-schema]: [XRD scope schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1095-L1107)
[^xrd-version-fields]: [XRD version fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1200-L1263)
[^xrd-serving-and-storage-flags]: [XRD serving and storage flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1360-L1368)
[^default-composition-reference-schema]: [Default Composition reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L925-L935)
[^default-composition-selection]: [Default Composition selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L298-L326)
[^default-composition-guidance]: [Default Composition guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L544-L570)
[^default-update-policy-schema]: [Default update-policy schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L984-L992)
[^compositionrevision-policy-behavior]: [CompositionRevision policy behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L154-L207)
[^enforced-composition-reference-schema]: [Enforced Composition reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L993-L1006)
[^enforced-composition-override]: [Enforced Composition override](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L355-L381)
[^enforced-composition-guidance]: [Enforced Composition guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L603-L627)
[^xrd-scope-guidance]: [XRD scope guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L500-L530)
[^referenceable-version-mapped-to-generated-crd-storage]: [Referenceable version mapped to generated CRD storage](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L158-L168)
