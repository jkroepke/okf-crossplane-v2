---
type: api
title: ManagedResourceDefinition
description: The Alpha API that defines and selectively activates a provider-managed resource API.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, managed-resources, api, alpha]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: mrd-feature-state
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L1-L6'
    title: 'MRD feature state'
  - id: mrd-crd-identity
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L7-L35'
    title: 'MRD CRD identity'
  - id: mrd-required-fields
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L444-L456'
    title: 'MRD required fields'
  - id: mrd-scope
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L251-L261'
    title: 'MRD scope'
  - id: mrd-version-serving-and-storage
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L387-L395'
    title: 'MRD version serving and storage'
  - id: mrd-activation-state
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L263-L272'
    title: 'MRD activation state'
  - id: provider-safe-start-behavior
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L248-L279'
    title: 'Provider safe-start behavior'
  - id: mrd-status-and-printer-columns
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L457-L507'
    title: 'MRD status and printer columns'
  - id: connection-detail-metadata-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L59-L76'
    title: 'Connection detail metadata schema'
  - id: mrd-establishment-reconciliation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/managed/reconciler.go#L119-L199'
    title: 'MRD establishment reconciliation'
  - id: mrd-source-types
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_types.go#L25-L49'
    title: 'MRD source types'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml]
feature_state: Alpha
---

# Overview

`ManagedResourceDefinition` (MRD) is the Alpha, cluster-scoped `apiextensions.crossplane.io/v1alpha1` API for defining a provider-managed resource API.[^mrd-feature-state][^mrd-crd-identity]

# Schema

An MRD requires `group`, `names`, `scope`, and `versions`; names require `kind` and `plural`.[^mrd-required-fields] Scope defaults to `Namespaced`, also permits `Cluster`, and is immutable.[^mrd-scope] Every version requires
`name`, `served`, and `storage`, and exactly one version must be stored.[^mrd-version-serving-and-storage] Optional `connectionDetails` entries require a name and description.[^connection-detail-metadata-schema]

# Behavior

`spec.state` defaults to `Inactive` in the schema and permits `Active` or `Inactive`.
It controls whether Crossplane creates the underlying CRD, and cannot return to `Inactive` after activation.[^mrd-activation-state] Inactive reconciliation sets `Established=False`; active reconciliation applies the
derived CRD, reports pending establishment, then `Established=True` after Kubernetes establishes it.[^mrd-establishment-reconciliation] User-facing defaults are qualified by provider capability: providers with `safe-start`
initially keep MRDs inactive for selective activation; providers without it initially activate MRDs for backward compatibility.[^provider-safe-start-behavior]

# Relationships

MRDs describe and activate the concrete APIs behind [managed resources](managed-resources.md). They expose status conditions and an `Established` printer column.[^mrd-status-and-printer-columns]

# Limitations

Alpha maturity is directly stated by the v2.3 documentation and applies to MRDs, not all managed resources.
The released generated CRD is authoritative for schema claims. Its source types are `apis/apiextensions/v1alpha1/mrd_types.go` and a maintained fork of Kubernetes CRD types in `crd_types.go`.[^mrd-source-types]
Concrete MR schemas and controller behavior remain provider-specific.

[^mrd-feature-state]: [MRD feature state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L1-L6)
[^mrd-crd-identity]: [MRD CRD identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L7-L35)
[^mrd-required-fields]: [MRD required fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L444-L456)
[^mrd-scope]: [MRD scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L251-L261)
[^mrd-version-serving-and-storage]: [MRD version serving and storage](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L387-L395)
[^mrd-activation-state]: [MRD activation state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L263-L272)
[^provider-safe-start-behavior]: [Provider safe-start behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L248-L279)
[^mrd-status-and-printer-columns]: [MRD status and printer columns](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L457-L507)
[^connection-detail-metadata-schema]: [Connection detail metadata schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L59-L76)
[^mrd-establishment-reconciliation]: [MRD establishment reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/managed/reconciler.go#L119-L199)
[^mrd-source-types]: [MRD source types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_types.go#L25-L49)
