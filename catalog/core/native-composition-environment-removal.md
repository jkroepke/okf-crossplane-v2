---
type: concept
title: Native Composition environment removal
description: The v1.18 boundary that removed Alpha native environment integration while retaining EnvironmentConfig resources.
resource: https://github.com/crossplane/crossplane/releases/tag/v1.18.0
tags: [crossplane, composition, environment-config, migration, removed]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: v1-17-3-explicit-alpha-composition-field
    resource: 'https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_types.go#L62-L68'
    title: 'v1.17.3 explicit Alpha Composition field'
  - id: v1-17-3-native-environment-schema
    resource: 'https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_environment.go#L29-L60'
    title: 'v1.17.3 native environment schema'
  - id: v1-17-3-environment-patch-types
    resource: 'https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_patches.go#L29-L42'
    title: 'v1.17.3 environment patch types'
  - id: v1-18-0-compositionspec-without-native-environment
    resource: 'https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/apis/apiextensions/v1/composition_types.go#L23-L62'
    title: 'v1.18.0 CompositionSpec without native environment'
  - id: v1-18-0-native-patch-types-after-removal
    resource: 'https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/apis/apiextensions/v1/composition_patches.go#L29-L105'
    title: 'v1.18.0 native patch types after removal'
  - id: v1-18-0-rejected-legacy-feature-flag
    resource: 'https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/cmd/crossplane/core/core.go#L220-L224'
    title: 'v1.18.0 rejected legacy feature flag'
  - id: v2-3-3-pipeline-only-compositionspec
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_types.go#L23-L60'
    title: 'v2.3.3 pipeline-only CompositionSpec'
  - id: official-v2-3-removal-and-migration-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L78-L144'
    title: 'Official v2.3 removal and migration guidance'
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
policy.[^v1-17-3-explicit-alpha-composition-field][^v1-17-3-native-environment-schema] Patch-and-Transform also exposed four environment patch types.[^v1-17-3-environment-patch-types]

Crossplane v1.18 removed that native Composition integration:

- `spec.environment` and its native selectors disappeared;[^v1-18-0-compositionspec-without-native-environment]
- `FromEnvironmentFieldPath`, `ToEnvironmentFieldPath`,
  `CombineFromEnvironment`, and `CombineToEnvironment` disappeared from native
  Composition patches;[^v1-18-0-native-patch-types-after-removal]
- the old `--enable-environment-configs` flag became an error directing users
  to `function-environment-configs`.[^v1-18-0-rejected-legacy-feature-flag]

The [EnvironmentConfig resource](environment-config.md) was retained and
promoted to a `v1beta1` storage API. Crossplane v2.3.3 continues this boundary:
Composition is pipeline-only and has no native environment field or
environment patch types.[^v2-3-3-pipeline-only-compositionspec]

# Migration

Official guidance converts Resource-mode Compositions to function pipelines.
Environment selection fields map to `function-environment-configs`; former
environment patching moves to a downstream function such as
`function-patch-and-transform`.[^official-v2-3-removal-and-migration-guidance]

The selected current `function-environment-configs` release requires Crossplane 2.x. This catalog therefore documents the v1.18 change as historical migration context, not as a claim that function v0.7.2 runs on Crossplane 1.x.

# Exclusions

Claims, deprecated XRD v1 schema, legacy v1 XR semantics, and old Resource-mode manifests are not reproduced. The removed field and patch names appear only so migration tooling and historical configurations can be recognized.

[^v1-17-3-explicit-alpha-composition-field]: [v1.17.3 explicit Alpha Composition field](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_types.go#L62-L68)
[^v1-17-3-native-environment-schema]: [v1.17.3 native environment schema](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_environment.go#L29-L60)
[^v1-17-3-environment-patch-types]: [v1.17.3 environment patch types](https://github.com/crossplane/crossplane/blob/481d3ca7193c89708b9a40375381862d25d64006/apis/apiextensions/v1/composition_patches.go#L29-L42)
[^v1-18-0-compositionspec-without-native-environment]: [v1.18.0 CompositionSpec without native environment](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/apis/apiextensions/v1/composition_types.go#L23-L62)
[^v1-18-0-native-patch-types-after-removal]: [v1.18.0 native patch types after removal](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/apis/apiextensions/v1/composition_patches.go#L29-L105)
[^v1-18-0-rejected-legacy-feature-flag]: [v1.18.0 rejected legacy feature flag](https://github.com/crossplane/crossplane/blob/e663a43ece850e93fe5cdebb2e478e2fb9762ad1/cmd/crossplane/core/core.go#L220-L224)
[^v2-3-3-pipeline-only-compositionspec]: [v2.3.3 pipeline-only CompositionSpec](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_types.go#L23-L60)
[^official-v2-3-removal-and-migration-guidance]: [Official v2.3 removal and migration guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L78-L144)
