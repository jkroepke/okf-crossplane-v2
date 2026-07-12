---
type: Crossplane API
title: CompositeResourceDefinition v2
description: The cluster-scoped Crossplane v2 API that defines a custom composite resource type.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, api, v2]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml]
feature_state: Not stated by selected sources
---

# Overview

`CompositeResourceDefinition` (XRD) is a cluster-scoped `apiextensions.crossplane.io/v2` API. It defines the group, names, scope, versions, and schemas of an XR API.[1][2]

# Schema

The defined resource requires `names.kind` and `names.plural`. Group and names are immutable, and plural and singular names must be lowercase.[3] Scope defaults to `Namespaced`, also permits `Cluster`, and is immutable.[4] Each declared version requires `name`, `served`, and `storage`.[5]

The XRD `v2` representation is served but not stored. The CRD's stored `v1` representation is explicitly deprecated; that storage detail does not make the current v2 user API legacy.[6]

# Behavior

The default composition update policy is `Automatic`; `Manual` is also permitted.[7] Official v2.3 guidance recommends `Namespaced` for most XRDs and explains that namespace scope confines composed resources to the XR namespace.[8]

# Limitations

Feature maturity is not stated by the selected CRD or documentation. The released generated CRD is authoritative for this catalog's schema claims, but its generator and Go source-of-truth types were not established in this bounded source batch. Claims, claim references, deprecated XRD v1 schema, legacy v1 XR semantics, and `LegacyCluster` guidance are excluded. Some v2.3 documentation snippets use the deprecated XRD `/v1` API; they are not used as v2 schema evidence.

# Citations

[1] [XRD CRD identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L7-L21)
[2] [Current v2 XRD example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L35-L73)
[3] [XRD names and group validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1007-L1015)
[4] [XRD scope schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1095-L1107)
[5] [XRD version fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1200-L1263)
[6] [XRD serving and storage flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1360-L1368)
[7] [Composition update policy](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L984-L992)
[8] [XRD scope guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L500-L530)
