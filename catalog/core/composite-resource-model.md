---
type: concept
title: Crossplane v2 composite resource model
description: An XR exposes a custom API whose schema is defined by an XRD and whose composed resources are selected by a Composition.
resource: https://docs.crossplane.io/v2.3/composition/composite-resources/
tags: [crossplane, core, composition, v2]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: crossplane-v2-3-composite-resource-model
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L7-L35'
    title: 'Crossplane v2.3 composite resource model'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths: [content/v2.3/composition/composite-resources.md]
feature_state: Not stated by selected sources
---

# Overview

A composite resource (XR) is a custom Kubernetes API and a single object that represents a set of Kubernetes resources.
A [CompositeResourceDefinition](composite-resource-definition.md) defines the XR API and schema.
A [Composition](composition.md) defines how Crossplane composes resources for that XR type.[^crossplane-v2-3-composite-resource-model]

# Relationships

Compositions may produce provider-defined [managed resources](managed-resources.md), other Kubernetes resources, or further composite resources. This catalog keeps the Crossplane CLI outside Core.

# Limitations

The selected v2.3 documentation does not state a feature maturity for the overall XR model.

[^crossplane-v2-3-composite-resource-model]: [Crossplane v2.3 composite resource model](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L7-L35)
