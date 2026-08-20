---
type: api
title: Install and manage Configuration packages
description: The cluster-scoped API that requests installation of an OCI-compatible Crossplane Configuration package.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, configurations, packages, api]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: configuration-crd-identity-and-purpose
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L7-L42'
    title: 'Configuration CRD identity and purpose'
  - id: registry-installation-boundary
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L87-L94'
    title: 'Registry installation boundary'
  - id: required-package-reference
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L89-L100'
    title: 'Required package reference'
  - id: installation-and-digest-references
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L28-L62'
    title: 'Installation and digest references'
  - id: configuration-package-controls
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L82-L149'
    title: 'Configuration package controls'
  - id: configuration-source-types
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/configuration_types.go#L25-L60'
    title: 'Configuration source types'
  - id: activation-and-constraint-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L144-L208'
    title: 'Activation and constraint guidance'
  - id: configuration-health-diagnostics
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L341-L401'
    title: 'Configuration health diagnostics'
  - id: configuration-status-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L153-L243'
    title: 'Configuration status schema'
  - id: shared-package-fields-defaults-and-validation-markers
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/package_types.go#L21-L84'
    title: 'Shared package fields, defaults, and validation markers'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/pkg.crossplane.io_configurations.yaml
  - apis/pkg/v1/configuration_types.go
  - apis/pkg/v1/package_types.go
documentation_repository: crossplane/docs
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths:
  - content/v2.3/packages/configurations.md
feature_state: Stable by repository default
feature_state_basis: Configuration serves only v1 in the selected release, with no explicit non-stable label or deprecation metadata; v1 alone is not used as proof.
---

# Overview

`Configuration` is a cluster-scoped `pkg.crossplane.io/v1` API, served and stored without deprecation metadata.
It requests installation of an OCI-compatible package containing XRDs and Compositions.[^configuration-crd-identity-and-purpose] Installation is registry-based; local registries can support offline environments, but direct installation from Kubernetes volumes is unsupported.[^registry-installation-boundary]

# Schema

`spec.package` is the only required spec field and must be a fully qualified registry and repository reference with a tag or digest.[^required-package-reference] Digest references provide deterministic, repeatable installation.[^installation-and-digest-references]

Package controls include:

- `packagePullPolicy`, default `IfNotPresent`
- `revisionActivationPolicy`, default `Automatic`; `Manual` is also defined
- `revisionHistoryLimit`, default one; zero disables inactive-revision retention
- `packagePullSecrets` for registry authentication
- `ignoreCrossplaneConstraints`, default `false`
- `skipDependencyResolution`, default `false`[^configuration-package-controls]

The Go types in `apis/pkg/v1/configuration_types.go` and `package_types.go` are the source types for the generated CRD and its defaults and validation markers.[^configuration-source-types][^shared-package-fields-defaults-and-validation-markers]

# Behavior

By default, Crossplane activates the newest revision and enforces the package's Crossplane version constraint.
Manual activation prevents automatic activation; bypassing constraints or dependency resolution removes those protections.[^activation-and-constraint-guidance] A healthy installation reports `Installed` and `Healthy` as true.
Dependency or constraint failures may leave installation true while health is false; revision conditions and events provide diagnostics.[^configuration-health-diagnostics]

Status also records conditions, the current identifier, newest revision, resolved package reference, and applied image configuration references.[^configuration-status-schema]

# Relationships

Changes to a Configuration produce controller-managed [ConfigurationRevisions](revision.md). Dependencies and their optional resolution behavior are described in [Dependencies and authoring](dependencies-and-authoring.md).

# Limitations

The Configuration API is Stable by repository default; unlabelled installation
workflow behavior has no separate maturity statement. Pull-policy values are
documented but are not encoded as an OpenAPI enum in the generated CRD. There
is no rollback field; rollback behavior is not claimed from this schema.

[^configuration-crd-identity-and-purpose]: [Configuration CRD identity and purpose](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L7-L42)
[^registry-installation-boundary]: [Registry installation boundary](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L87-L94)
[^required-package-reference]: [Required package reference](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L89-L100)
[^installation-and-digest-references]: [Installation and digest references](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L28-L62)
[^configuration-package-controls]: [Configuration package controls](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L82-L149)
[^configuration-source-types]: [Configuration source types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/configuration_types.go#L25-L60)
[^activation-and-constraint-guidance]: [Activation and constraint guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L144-L208)
[^configuration-health-diagnostics]: [Configuration health diagnostics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L341-L401)
[^configuration-status-schema]: [Configuration status schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L153-L243)
[^shared-package-fields-defaults-and-validation-markers]: [Shared package fields, defaults, and validation markers](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/package_types.go#L21-L84)
