---
type: api
title: Composition
description: The current cluster-scoped API for an ordered Crossplane Function pipeline compatible with an XR type.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, composition, functions]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: composition-crd-identity-and-version
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L32'
    title: 'Composition CRD identity and version'
  - id: composition-pipeline-overview
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L11-L73'
    title: 'Composition pipeline overview'
  - id: composite-type-reference
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L58-L78'
    title: 'Composite type reference'
  - id: composition-mode-and-validation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L79-L98'
    title: 'Composition mode and validation'
  - id: pipeline-step-requirements
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L246-L258'
    title: 'Pipeline step requirements'
  - id: step-input-and-requirements
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L144-L245'
    title: 'Step input and requirements'
  - id: function-ordering-and-xr-compatibility
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L205-L251'
    title: 'Function ordering and XR compatibility'
  - id: typereference-fields-and-constructor
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_common.go#L44-L55'
    title: 'TypeReference fields and constructor'
  - id: xrd-referenceable-gvk-derivation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L287-L298'
    title: 'XRD referenceable GVK derivation'
  - id: composition-compatibility-filter-compares-the-reconciled-xr-gvk
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L267-L280'
    title: 'Composition compatibility filter compares the reconciled XR GVK'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositions.yaml
  - apis/apiextensions/v1/composition_common.go
  - apis/apiextensions/v2/xrd_types.go
  - internal/controller/apiextensions/composite/api.go
documentation_repository: crossplane/docs
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths: [content/v2.3/composition/compositions.md]
feature_state: Stable by repository default
---

# Overview

`Composition` is the current cluster-scoped `apiextensions.crossplane.io/v1` API. It is served and stored without deprecation metadata.[^composition-crd-identity-and-version] A Composition is a reusable, ordered pipeline of Functions for a selected XR type.[^composition-pipeline-overview]

# Schema

When `spec` is present, `spec.compositeTypeRef` is required and immutable, and requires an `apiVersion` and `kind`.[^composite-type-reference] The root schema does not itself mark `spec` required. Mode defaults to—and currently permits only—`Pipeline`; Pipeline mode requires a pipeline.[^composition-mode-and-validation] A pipeline
has 1–99 uniquely named steps, each requiring `step` and `functionRef`.[^pipeline-step-requirements] A step may contain arbitrary embedded Kubernetes input and resource or schema requirements.[^step-input-and-requirements]

# Behavior

Functions run in declared order, each receiving the preceding result. `compositeTypeRef` restricts which XR API version and kind may use the Composition.[^function-ordering-and-xr-compatibility] Its values must exactly match the XR GVK: the XRD group and referenceable version form `apiVersion`, and `spec.names.kind` supplies `kind`.[^typereference-fields-and-constructor][^xrd-referenceable-gvk-derivation][^composition-compatibility-filter-compares-the-reconciled-xr-gvk]

# Relationships

A Composition implements the API defined by a
[CompositeResourceDefinition](composite-resource-definition.md) and may use
packages such as [function-go-templating](../functions/function-go-templating/index.md).
Because a Composition has no native status, GitOps tools need special treatment
when users expect a meaningful [health assessment](composition-gitops-health.md).
For an ordered authoring route, use the
[Composition developer starter guide](../composition-developer-starter.md),
[pipeline and security design](../composition-pipeline-and-security.md), and
the [reference project layout](composition-project-layout.md).

# Limitations

No selected source labels the current Composition API Alpha, Beta, Preview, or
Deprecated, and no relevant served alpha or beta API version applies. Its
feature state is therefore Stable by repository default; `/v1` alone is not
the proof of that state.
The released generated CRD is authoritative for this catalog's schema claims;
the selected Go type helper corroborates the `compositeTypeRef` GVK mapping.
The `/v1` API is current and is not excluded as legacy.
Legacy connection-secret workflows are outside this foundational scope.

[^composition-crd-identity-and-version]: [Composition CRD identity and version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L32)
[^composition-pipeline-overview]: [Composition pipeline overview](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L11-L73)
[^composite-type-reference]: [Composite type reference](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L58-L78)
[^composition-mode-and-validation]: [Composition mode and validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L79-L98)
[^pipeline-step-requirements]: [Pipeline step requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L246-L258)
[^step-input-and-requirements]: [Step input and requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L144-L245)
[^function-ordering-and-xr-compatibility]: [Function ordering and XR compatibility](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L205-L251)
[^typereference-fields-and-constructor]: [TypeReference fields and constructor](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_common.go#L44-L55)
[^xrd-referenceable-gvk-derivation]: [XRD referenceable GVK derivation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L287-L298)
[^composition-compatibility-filter-compares-the-reconciled-xr-gvk]: [Composition compatibility filter compares the reconciled XR GVK](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L267-L280)
