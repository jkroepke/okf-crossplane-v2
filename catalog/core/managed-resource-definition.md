---
type: api
title: ManagedResourceDefinition
description: The Alpha API that defines and selectively activates a provider-managed resource API.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, managed-resources, api, alpha]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml]
feature_state: Alpha
---

# Overview

`ManagedResourceDefinition` (MRD) is the Alpha, cluster-scoped `apiextensions.crossplane.io/v1alpha1` API for defining a provider-managed resource API.[1][2]

# Schema

An MRD requires `group`, `names`, `scope`, and `versions`; names require `kind` and `plural`.[3] Scope defaults to `Namespaced`, also permits `Cluster`, and is immutable.[4] Every version requires
`name`, `served`, and `storage`, and exactly one version must be stored.[5]

# Behavior

`spec.state` defaults to `Inactive` in the schema and permits `Active` or `Inactive`.
It controls whether Crossplane creates the underlying CRD, and cannot return to `Inactive` after activation.[6] User-facing defaults are qualified by provider capability: providers with `safe-start`
initially keep MRDs inactive for selective activation; providers without it initially activate MRDs for backward compatibility.[7]

# Relationships

MRDs describe and activate the concrete APIs behind [managed resources](managed-resources.md). They expose status conditions and an `Established` printer column.[8]

# Limitations

Alpha maturity is directly stated by the v2.3 documentation and applies to MRDs, not all managed resources.
The released generated CRD is authoritative for this catalog's schema claims, but its generator and Go source-of-truth types were not established in this bounded source batch.
Concrete MR schemas and controller behavior remain provider-specific.

# Citations

[1] [MRD feature state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L1-L6)
[2] [MRD CRD identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L7-L35)
[3] [MRD required fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L444-L456)
[4] [MRD scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L251-L261)
[5] [MRD version serving and storage](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L387-L395)
[6] [MRD activation state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L263-L272)
[7] [Provider safe-start behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L248-L279)
[8] [MRD status and printer columns](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L457-L507)
