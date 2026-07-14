---
type: concept
title: Native Composition environment removal
description: The v1.18 boundary that removed Alpha native environment integration while retaining EnvironmentConfig resources.
resource: https://github.com/crossplane/crossplane/releases/tag/v1.18.0
tags: [crossplane, composition, environment-config, migration, removed]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane/crossplane
source_tag: v1.18.0
source_commit: e663a43ece850e93fe5cdebb2e478e2fb9762ad1
source_paths:
  - apis/apiextensions/v1/composition_types.go
  - apis/apiextensions/v1/composition_patches.go
  - cmd/crossplane/core/core.go
supporting_source_tag: v1.17.3
supporting_source_commit: 481d3ca7193c89708b9a40375381862d25d64006
documentation_repository: crossplane/docs
documentation_series: v2.3
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
feature_state: Removed
feature_state_basis: Crossplane v1.17.3 explicitly marked Composition.spec.environment Alpha; released v1.18 source removed the field and rejects its former feature flag.
---

# Removal boundary

Crossplane v1.17.3 exposed an explicitly Alpha, feature-gated
`Composition.spec.environment`. It supported `defaultData`, ordered reference
or selector sources, pre-render environment patches, and a resolution
policy.[1][2] Patch-and-Transform also exposed four environment patch types.[3]

Crossplane v1.18 removed that native Composition integration:

- `spec.environment` and its native selectors disappeared;[4]
- `FromEnvironmentFieldPath`, `ToEnvironmentFieldPath`,
  `CombineFromEnvironment`, and `CombineToEnvironment` disappeared from native
  Composition patches;[5]
- the old `--enable-environment-configs` flag became an error directing users
  to `function-environment-configs`.[6]

The [EnvironmentConfig resource](environment-config.md) was retained and
promoted to a `v1beta1` storage API. Crossplane v2.3.3 continues this boundary:
Composition is pipeline-only and has no native environment field or
environment patch types.[7]

# Migration

Official guidance converts Resource-mode Compositions to function pipelines.
Environment selection fields map to `function-environment-configs`; former
environment patching moves to a downstream function such as
`function-patch-and-transform`.[8]

The selected current `function-environment-configs` release requires Crossplane 2.x. This catalog therefore documents the v1.18 change as historical migration context, not as a claim that function v0.7.2 runs on Crossplane 1.x.

# Exclusions

Claims, deprecated XRD v1 schema, legacy v1 XR semantics, and old Resource-mode manifests are not reproduced. The removed field and patch names appear only so migration tooling and historical configurations can be recognized.

# Citations

[1] [v1.17.3 explicit Alpha Composition field](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_types.go#L62-L68)
[2] [v1.17.3 native environment schema](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_environment.go#L29-L60)
[3] [v1.17.3 environment patch types](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_patches.go#L29-L42)
[4] [v1.18.0 CompositionSpec without native environment](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/apis/apiextensions/v1/composition_types.go#L23-L62)
[5] [v1.18.0 native patch types after removal](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/apis/apiextensions/v1/composition_patches.go#L29-L105)
[6] [v1.18.0 rejected legacy feature flag](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/cmd/crossplane/core/core.go#L220-L224)
[7] [v2.3.3 pipeline-only CompositionSpec](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_types.go#L23-L60)
[8] [Official v2.3 removal and migration guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L78-L144)
