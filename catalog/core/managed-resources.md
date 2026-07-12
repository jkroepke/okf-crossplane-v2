---
type: concept
title: Managed resources
description: Kubernetes representations of external services managed by Crossplane Providers.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, providers]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths: [content/v2.3/managed-resources/managed-resources.md]
feature_state: Not stated by selected sources
---

# Overview

A managed resource (MR) is the Kubernetes representation of an external service managed by a Provider.
Creating an MR asks its Provider to create and manage the corresponding external resource.
Providers define each MR's group, version, kind, settings, and `spec.forProvider` mapping.[1]

# Relationships

Concrete MR APIs and behavior are provider-defined; Crossplane Core does not expose one generic MR CRD.
Core provides the [ManagedResourceDefinition](managed-resource-definition.md) API that represents and activates provider-defined MR APIs.

# Limitations

Feature maturity for managed resources generally is not stated by the selected sources.
`managementPolicies` is separately documented as Beta and provider support varies; that maturity does not apply to all managed-resource behavior.[2] Concrete resource schemas require separately pinned provider sources.

# Citations

[1] [Managed resource model](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L7-L47)
[2] [Management policies maturity](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L286-L305)
