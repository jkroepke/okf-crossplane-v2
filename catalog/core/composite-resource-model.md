---
type: Crossplane Core Concept
title: Crossplane v2 composite resource model
description: An XR exposes a custom API whose schema is defined by an XRD and whose composed resources are selected by a Composition.
resource: https://docs.crossplane.io/v2.3/composition/composite-resources/
tags: [crossplane, core, composition, v2]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths: [content/v2.3/composition/composite-resources.md]
feature_state: Not stated by selected sources
---

# Overview

A composite resource (XR) is a custom Kubernetes API and a single object that represents a set of Kubernetes resources. A [CompositeResourceDefinition](composite-resource-definition.md) defines the XR API and schema. A [Composition](composition.md) defines how Crossplane composes resources for that XR type.[1]

# Relationships

Compositions may produce provider-defined [managed resources](managed-resources.md), other Kubernetes resources, or further composite resources. This catalog keeps the Crossplane CLI outside Core.

# Limitations

The selected v2.3 documentation does not state a feature maturity for the overall XR model.

# Citations

[1] [Crossplane v2.3 composite resource model](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L7-L35)
