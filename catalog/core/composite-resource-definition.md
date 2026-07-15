---
type: api
title: CompositeResourceDefinition v2
description: The cluster-scoped Crossplane v2 API that defines a custom composite resource type.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, api, v2]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml
  - apis/apiextensions/v2/xrd_types.go
  - internal/controller/apiextensions/composite/api.go
feature_state: Stable by repository default
---

# Overview

`CompositeResourceDefinition` (XRD) is a cluster-scoped `apiextensions.crossplane.io/v2` API. It defines the group, names, scope, versions, and schemas of an XR API.[1][2]

# Schema

The defined resource requires `names.kind` and `names.plural`.
Group and names are immutable, and plural and singular names must be lowercase.[3] Scope defaults to `Namespaced`, also permits `Cluster`, and is immutable.[4] Each declared version requires `name`, `served`, and `storage`.[5]

The XRD `v2` representation is served but not stored. The CRD's stored `v1` representation is explicitly deprecated; that storage detail does not make the current v2 user API legacy.[6]

# Composition selection and revision policy

`spec.defaultCompositionRef` is optional and requires a Composition `name`.
It supplies the Composition only when an XR sets neither a composition reference
nor a composition selector.[7][8] This is the documented way to set a default
when multiple Compositions reference the same XRD.[9]

`spec.defaultCompositionUpdatePolicy` is optional, defaults to `Automatic`,
and permits only `Automatic` or `Manual`. It is the fallback when an XR has no
own update policy: `Automatic` follows the revision selector after a new
CompositionRevision exists, while `Manual` retains the selected revision.[10][11]

`spec.enforcedCompositionRef` is optional, requires a Composition `name`, and
is immutable. When set, it replaces a different XR composition reference, so it
enforces one Composition for all XRs defined by the XRD rather than merely
providing a default.[12][13] Official v2.3 guidance describes this as requiring
all composite resources using the XRD to use the named Composition.[14]

Official v2.3 guidance recommends `Namespaced` for most XRDs and explains that
namespace scope confines composed resources to the XR namespace.[15]

# Limitations

No selected current source labels XRD v2 Alpha, Beta, Preview, or Deprecated,
and no relevant served alpha or beta API version applies. Its feature state is
therefore Stable by repository default; the `/v1` storage representation alone
is not the basis for that classification.
Claims, claim references, deprecated XRD v1 schema, legacy v1 XR semantics, and `LegacyCluster` guidance are excluded.
Some v2.3 documentation snippets use the deprecated XRD `/v1` API; they are not used as v2 schema evidence.

# Citations

[1] [XRD CRD identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L7-L21)
[2] [Current v2 XRD example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L35-L73)
[3] [XRD names and group validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1007-L1015)
[4] [XRD scope schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1095-L1107)
[5] [XRD version fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1200-L1263)
[6] [XRD serving and storage flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1360-L1368)
[7] [Default Composition reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L925-L935)
[8] [Default Composition selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L298-L326)
[9] [Default Composition guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L544-L570)
[10] [Default update-policy schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L984-L992)
[11] [CompositionRevision policy behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L154-L207)
[12] [Enforced Composition reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L993-L1006)
[13] [Enforced Composition override](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L355-L381)
[14] [Enforced Composition guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L603-L627)
[15] [XRD scope guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L500-L530)
