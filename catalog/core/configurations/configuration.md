---
type: api
title: Install and manage Configuration packages
description: The cluster-scoped API that requests installation of an OCI-compatible Crossplane Configuration package.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, configurations, packages, api]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/pkg.crossplane.io_configurations.yaml
  - apis/pkg/v1/configuration_types.go
  - apis/pkg/v1/package_types.go
feature_state: Not stated by selected sources
---

# Overview

`Configuration` is a cluster-scoped `pkg.crossplane.io/v1` API, served and stored without deprecation metadata.
It requests installation of an OCI-compatible package containing XRDs and Compositions.[1] Installation is registry-based; local registries can support offline environments, but direct installation from Kubernetes volumes is unsupported.[2]

# Schema

`spec.package` is the only required spec field and must be a fully qualified registry and repository reference with a tag or digest.[3] Digest references provide deterministic, repeatable installation.[4]

Package controls include:

- `packagePullPolicy`, default `IfNotPresent`
- `revisionActivationPolicy`, default `Automatic`; `Manual` is also defined
- `revisionHistoryLimit`, default one; zero disables inactive-revision retention
- `packagePullSecrets` for registry authentication
- `ignoreCrossplaneConstraints`, default `false`
- `skipDependencyResolution`, default `false`[5]

The Go types in `apis/pkg/v1/configuration_types.go` and `package_types.go` are the source types for the generated CRD and its defaults and validation markers.[6][10]

# Behavior

By default, Crossplane activates the newest revision and enforces the package's Crossplane version constraint.
Manual activation prevents automatic activation; bypassing constraints or dependency resolution removes those protections.[7] A healthy installation reports `Installed` and `Healthy` as true.
Dependency or constraint failures may leave installation true while health is false; revision conditions and events provide diagnostics.[8]

Status also records conditions, the current identifier, newest revision, resolved package reference, and applied image configuration references.[9]

# Relationships

Changes to a Configuration produce controller-managed [ConfigurationRevisions](revision.md). Dependencies and their optional resolution behavior are described in [Dependencies and authoring](dependencies-and-authoring.md).

# Limitations

Feature maturity is not stated. Pull-policy values are documented but are not encoded as an OpenAPI enum in the generated CRD. There is no rollback field; rollback behavior is not claimed from this schema.

# Citations

[1] [Configuration CRD identity and purpose](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L7-L42)
[2] [Registry installation boundary](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L87-L94)
[3] [Required package reference](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L89-L100)
[4] [Installation and digest references](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L28-L62)
[5] [Configuration package controls](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L82-L149)
[6] [Configuration source types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/configuration_types.go#L25-L60)
[7] [Activation and constraint guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L144-L208)
[8] [Configuration health diagnostics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L341-L401)
[9] [Configuration status schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L153-L243)
[10] [Shared package fields, defaults, and validation markers](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/package_types.go#L21-L84)
