---
type: api
title: EnvironmentConfig
description: Beta cluster-scoped data resources retained after native Composition environment integration was removed.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, environment-config, composition, beta]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane/crossplane
source_tag: v2.3.3
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_environmentconfigs.yaml
  - apis/apiextensions/v1beta1/environment_config_types.go
documentation_repository: crossplane/docs
documentation_series: v2.3
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
feature_state: Beta
feature_state_basis: The current CRD serves only apiextensions.crossplane.io/v1beta1 and official v2.3 documentation explicitly labels the API Beta.
---

# Overview

`EnvironmentConfig` remains a cluster-scoped Crossplane resource in v2.3.3. It
has an optional schemaless `data` object for arbitrary JSON-compatible values,
plural `environmentconfigs`, and short name `envcfg`.[1][2]

The resource is not a native Composition selector or merge engine. Current
pipelines use
[function-environment-configs](../functions/function-environment-configs/index.md) to
retrieve selected objects, merge their data, and place the result in function
context.[3]

# API lifecycle

| Release | Served and storage versions | Meaning |
|---|---|---|
| v1.17.3 | `v1alpha1` served and storage | Alpha resource used by the then-native Alpha Composition environment integration.[4] |
| v1.18.0 | `v1alpha1` served for compatibility; `v1beta1` served and storage | The resource was promoted while native Composition integration was removed.[5] |
| v2.3.3 | `v1beta1` served and storage | Current retained Beta API.[1] |

Official v2.3 documentation describes the in-memory environment as unique to
an XR and unavailable to other XRs. That statement concerns the per-run
pipeline context assembled from shared cluster-scoped resources, not isolation
of the `EnvironmentConfig` objects themselves.[3]

# Limitations

- Do not say that Crossplane v1.18 removed the `EnvironmentConfig` API. It removed native selection, loading, and environment patching.
- The schemaless `data` field does not validate application-specific structure. Downstream functions define any required keys and value types.
- Current documentation sometimes says Crossplane merges referenced EnvironmentConfigs as shorthand; its detailed workflow and released implementation attribute retrieval and merging to the function.[3]

# Citations

[1] [Crossplane v2.3.3 EnvironmentConfig CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_environmentconfigs.yaml#L7-L62)
[2] [Crossplane v2.3.3 v1beta1 type](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1beta1/environment_config_types.go#L24-L44)
[3] [Crossplane v2.3 Environment Configs documentation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L1-L34)
[4] [Crossplane v1.17.3 EnvironmentConfig CRD](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/cluster/crds/apiextensions.crossplane.io_environmentconfigs.yaml#L7-L63)
[5] [Crossplane v1.18.0 multi-version EnvironmentConfig CRD](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/cluster/crds/apiextensions.crossplane.io_environmentconfigs.yaml#L20-L104)
