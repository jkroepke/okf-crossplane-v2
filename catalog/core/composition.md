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
source_paths: [cluster/crds/apiextensions.crossplane.io_compositions.yaml]
feature_state: Not stated by selected sources
---

# Overview

`Composition` is the current cluster-scoped `apiextensions.crossplane.io/v1` API. It is served and stored without deprecation metadata.[1] A Composition is a reusable, ordered pipeline of Functions for a selected XR type.[2]

# Schema

`spec.compositeTypeRef` is required and immutable, and requires an `apiVersion` and `kind`.[3] Mode defaults to—and currently permits only—`Pipeline`; Pipeline mode requires a pipeline.[4] A pipeline
has 1–99 uniquely named steps, each requiring `step` and `functionRef`.[5] A step may contain arbitrary embedded Kubernetes input and resource or schema requirements.[6]

# Behavior

Functions run in declared order, each receiving the preceding result. `compositeTypeRef` restricts which XR API version and kind may use the Composition.[7]

# Relationships

A Composition implements the API defined by a
[CompositeResourceDefinition](composite-resource-definition.md) and may use
packages such as [function-go-templating](../functions/function-go-templating/).
Because a Composition has no native status, GitOps tools need special treatment
when users expect a meaningful [health assessment](composition-gitops-health.md).

# Limitations

Feature maturity is not stated by the selected sources.
The released generated CRD is authoritative for this catalog's schema claims, but its generator and Go source-of-truth types were not established in this bounded source batch.
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
