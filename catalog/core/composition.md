---
type: api
title: Composition
description: The current cluster-scoped API for an ordered Crossplane Function pipeline compatible with an XR type.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, composition, functions]
timestamp: 2026-07-14T00:00:00Z
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

`Composition` is the current cluster-scoped `apiextensions.crossplane.io/v1` API. It is served and stored without deprecation metadata.[1] A Composition is a reusable, ordered pipeline of Functions for a selected XR type.[2]

# Schema

When `spec` is present, `spec.compositeTypeRef` is required and immutable, and requires an `apiVersion` and `kind`.[3] The root schema does not itself mark `spec` required. Mode defaults to—and currently permits only—`Pipeline`; Pipeline mode requires a pipeline.[4] A pipeline
has 1–99 uniquely named steps, each requiring `step` and `functionRef`.[5] A step may contain arbitrary embedded Kubernetes input and resource or schema requirements.[6]

# Behavior

Functions run in declared order, each receiving the preceding result. `compositeTypeRef` restricts which XR API version and kind may use the Composition.[7] Its values must exactly match the XR GVK: the XRD group and referenceable version form `apiVersion`, and `spec.names.kind` supplies `kind`.[8][9][10]

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

# Citations

[1] [Composition CRD identity and version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L32)
[2] [Composition pipeline overview](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L11-L73)
[3] [Composite type reference](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L58-L78)
[4] [Composition mode and validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L79-L98)
[5] [Pipeline step requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L246-L258)
[6] [Step input and requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L144-L245)
[7] [Function ordering and XR compatibility](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L205-L251)
[8] [TypeReference fields and constructor](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_common.go#L44-L55)
[9] [XRD referenceable GVK derivation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L287-L298)
[10] [Composition compatibility filter compares the reconciled XR GVK](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L267-L280)
