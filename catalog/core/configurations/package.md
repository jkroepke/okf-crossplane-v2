---
type: concept
title: Crossplane Configuration packages
description: Portable OCI packages of Crossplane API definitions, Compositions, and declared package dependencies.
resource: https://docs.crossplane.io/v2.3/packages/configurations/
tags: [crossplane, core, configurations, packages, oci]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: configuration-package-purpose-and-contents
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L8-L20'
    title: 'Configuration package purpose and contents'
  - id: package-manager-portability
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/whats-crossplane/_index.md#L281-L292'
    title: 'Package manager portability'
  - id: configuration-dependency-kinds
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L354-L401'
    title: 'Configuration dependency kinds'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths: [content/v2.3/packages/configurations.md]
feature_state: Not stated by selected sources
---

# Overview

A Configuration is a portable OCI package of Crossplane control-plane configuration.
It can contain [CompositeResourceDefinitions](../composite-resource-definition.md) and [Compositions](../composition.md), and can declare Provider, Function, or Configuration dependencies.[^configuration-package-purpose-and-contents][^configuration-dependency-kinds] The
package manager installs these parts so the same control-plane capabilities can be distributed across clusters.[^package-manager-portability]

# Relationships

Users request installation through a [Configuration](configuration.md) object.
Crossplane creates and manages [ConfigurationRevision](revision.md) objects as package versions change.
Package dependency and metadata rules are covered in [Dependencies and authoring](dependencies-and-authoring.md).

# Limitations

Overall Configuration package maturity is not stated by the selected sources.
The documentation initially summarizes installed content as Compositions, XRDs, and Providers, while its dependency section also permits Functions and nested Configurations; this catalog retains the broader, explicit dependency list.[^configuration-dependency-kinds]

[^configuration-package-purpose-and-contents]: [Configuration package purpose and contents](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L8-L20)
[^package-manager-portability]: [Package manager portability](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/whats-crossplane/_index.md#L281-L292)
[^configuration-dependency-kinds]: [Configuration dependency kinds](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L354-L401)
