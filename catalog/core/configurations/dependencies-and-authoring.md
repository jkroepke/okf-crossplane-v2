---
type: Crossplane Development Guide
title: Configuration dependencies and authoring
description: Package metadata, contents, dependency constraints, and dependency-resolution behavior for Crossplane Configurations.
resource: https://docs.crossplane.io/v2.3/packages/configurations/
tags: [crossplane, core, configurations, dependencies, authoring]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths:
  - content/v2.3/packages/configurations.md
  - content/v2.3/get-started/install.md
feature_state: Not stated by selected sources
---

# Package contents

A Configuration package is a fully OCI-compliant image containing one or more YAML files. It requires `crossplane.yaml` metadata and may include XRD and Composition files.[1]

Metadata uses `meta.pkg.crossplane.io/v1` kind `Configuration`. `spec.dependsOn` may declare Configuration, Function, or Provider requirements with optional package-version constraints; `spec.crossplane.version` may constrain the Crossplane version.[2]

# Dependencies

Crossplane resolves and installs dependencies by default. Setting `skipDependencyResolution` disables that behavior and makes the user responsible for installing required packages.[3] Missing or incompatible dependencies make the Configuration unhealthy and appear in ConfigurationRevision conditions and events.[4]

Automatic dependency version upgrades and downgrades are separate Alpha features, disabled behind feature flags. Downgrades may risk orphaned managed resources, data loss, or CRD storage-version problems.[5] Alpha applies only to these automatic version-change features; maturity for base dependency resolution and package authoring is not stated.

# Relationships

Dependencies are resolved as part of installing a [Configuration](configuration.md), with counts and health visible on its [ConfigurationRevision](revision.md).

# Limitations

The selected v2.3 documentation disagrees on downgrade enablement: the Configuration page names Helm value `packageManager.enableAutomaticDependencyDowngrade=true` and also requires automatic upgrades, while the installation page names the distinct flag `--enable-dependency-version-downgrades`.[5][6] This catalog therefore does not prescribe one activation mechanism.

This Core page documents package input and metadata, not Crossplane CLI command syntax. Building and publishing commands belong to the separate CLI catalog domain. The selected documentation links to a moving package specification; no claims here rely on that unpinned link.

# Citations

[1] [Configuration package files](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L403-L423)
[2] [Configuration metadata and dependency declarations](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L425-L472)
[3] [Dependency resolution control](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L244-L270)
[4] [Dependency health and diagnostics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L354-L401)
[5] [Alpha dependency upgrade and downgrade features](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/get-started/install.md#L96-L120)
[6] [Configuration-page downgrade enablement](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L272-L311)
