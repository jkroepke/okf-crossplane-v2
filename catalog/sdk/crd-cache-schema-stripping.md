---
type: Crossplane Development Guide
title: Custom-resource gate CRD cache schema stripping
description: Configure crossplane-runtime's opt-in CRD cache transform without hiding data that another cache consumer requires.
resource: https://github.com/crossplane/crossplane-runtime/tree/71f319796d597c2c6cf004cc4bf5f44011a5aeaa/pkg/reconciler/customresourcesgate
tags: [crossplane, provider-development, crossplane-runtime, crd, cache]
timestamp: 2026-08-19T00:00:00Z
source_repository: crossplane/crossplane-runtime
source_commit: 71f319796d597c2c6cf004cc4bf5f44011a5aeaa
source_paths:
  - pkg/reconciler/customresourcesgate/cache.go
  - pkg/reconciler/customresourcesgate/cache_test.go
  - pkg/reconciler/customresourcesgate/reconciler.go
  - pkg/reconciler/customresourcesgate/setup.go
feature_state: Not stated by selected sources
feature_state_basis: Unlabelled non-API Go helper in crossplane-runtime v2.4.0.
---

# Overview

`crossplane-runtime` v2.4.0 exports `TransformStripCRDSchema` for use as
the per-object controller-runtime cache transform for
`CustomResourceDefinition` objects. It removes data that the
`customresourcesgate` reconciler does not read while retaining the CRD identity,
served-version, and establishment state that the reconciler needs.[1][3]

The transform is opt-in. `customresourcesgate.Setup` registers the controller
but does not configure the manager's cache, so the controller author must add
the transform explicitly through `cache.Options.ByObject`.[1][4]

# Transformation contract

| Cached object | Returned object | Removed data |
| --- | --- | --- |
| `*apiextensionsv1.CustomResourceDefinition` | The same pointer, mutated in place | Every `spec.versions[*].schema`, `metadata.managedFields`, and the `kubectl.kubernetes.io/last-applied-configuration` annotation |
| Any other object | The original object unchanged | Nothing |

The implementation does not deep-copy a CRD. Tests cover multiple versions,
empty versions, nil annotations, preservation of other annotations, and
non-CRD pass-through.[1][2]

# Gate compatibility

The gate reconciler constructs GVKs from the CRD group, version names, served
flags, and kind. It also checks the `Established` status condition. The
transform leaves those fields available, so its reduced CRD representation
still contains the data used by this reconciler.[3]

# Cache-consumer boundary

Treat the transform as a data contract for every reader sharing the configured
CRD cache. After opting in, cache readers cannot inspect validation schemas,
managed-field ownership, or the removed last-applied annotation from those
cached CRDs. Do not enable it on a shared cache when another controller needs
one of those fields.

For authoring or validating managed-resource manifests, retrieve the selected
provider package's immutable CRD artifact using [provider CRD schema
discovery](../providers/crd-schema-discovery.md); a transformed informer-cache object no
longer contains that schema.

# Limitations

The selected sources do not quantify memory savings or state that every
controller should install the transform. They also do not assign a lifecycle
state to this non-API Go helper. Its feature state is therefore **Not stated by
selected sources**, even though the implementation is present in the stable
`v2.4.0` tag.[1][5]

# Citations

[1] [`TransformStripCRDSchema` API, cache configuration, and implementation](https://github.com/crossplane/crossplane-runtime/blob/71f319796d597c2c6cf004cc4bf5f44011a5aeaa/pkg/reconciler/customresourcesgate/cache.go#L23-L57)

[2] [Transform behavior tests](https://github.com/crossplane/crossplane-runtime/blob/71f319796d597c2c6cf004cc4bf5f44011a5aeaa/pkg/reconciler/customresourcesgate/cache_test.go#L43-L235)

[3] [Fields consumed by the custom-resources gate reconciler](https://github.com/crossplane/crossplane-runtime/blob/71f319796d597c2c6cf004cc4bf5f44011a5aeaa/pkg/reconciler/customresourcesgate/reconciler.go#L39-L85)

[4] [Controller-only custom-resources gate setup](https://github.com/crossplane/crossplane-runtime/blob/71f319796d597c2c6cf004cc4bf5f44011a5aeaa/pkg/reconciler/customresourcesgate/setup.go#L30-L45)

[5] [crossplane-runtime v2.3.3 to v2.4.0 comparison](https://github.com/crossplane/crossplane-runtime/compare/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827...71f319796d597c2c6cf004cc4bf5f44011a5aeaa)
