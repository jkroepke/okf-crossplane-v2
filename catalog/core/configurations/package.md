---
type: Crossplane Core Concept
title: Crossplane Configuration packages
description: Portable OCI packages of Crossplane API definitions, Compositions, and declared package dependencies.
resource: https://docs.crossplane.io/v2.3/packages/configurations/
tags: [crossplane, core, configurations, packages, oci]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths: [content/v2.3/packages/configurations.md]
feature_state: Not stated by selected sources
---

# Overview

A Configuration is a portable OCI package of Crossplane control-plane configuration. It can contain [CompositeResourceDefinitions](../composite-resource-definition.md) and [Compositions](../composition.md), and can declare Provider, Function, or Configuration dependencies.[1][3] The package manager installs these parts so the same control-plane capabilities can be distributed across clusters.[2]

# Relationships

Users request installation through a [Configuration](configuration.md) object. Crossplane creates and manages [ConfigurationRevision](revision.md) objects as package versions change. Package dependency and metadata rules are covered in [Dependencies and authoring](dependencies-and-authoring.md).

# Limitations

Overall Configuration package maturity is not stated by the selected sources. The documentation initially summarizes installed content as Compositions, XRDs, and Providers, while its dependency section also permits Functions and nested Configurations; this catalog retains the broader, explicit dependency list.[3]

# Citations

[1] [Configuration package purpose and contents](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L8-L20)
[2] [Package manager portability](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/whats-crossplane/_index.md#L281-L292)
[3] [Configuration dependency kinds](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L354-L401)
