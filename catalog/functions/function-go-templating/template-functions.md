---
type: Reference
title: function-go-templating template functions
description: Project-specific template helpers and the boundary of exposed Sprig functions.
resource: https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go
tags: [crossplane, composition-function, template-functions]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Functions

The selected release adds these project-specific functions:[1]

`randomChoice`, `toYaml`, `fromYaml`, `getResourceCondition`, `setResourceNameAnnotation`, `getComposedResource`, `getCompositeResource`, `getExtraResources`, `getExtraResourcesFromContext`, `getCredentialData`, and `include`.

`include` executes a named template and returns its output as a string. It rejects nesting beyond its recursion bound.[2]

# Sprig boundary

The release depends on Sprig `v3.3.0`.[3] It starts with Sprig's general function map and deletes `env` and `expandenv` because the source identifies an information-leakage risk.[4] See the versioned [Sprig reference](sprig.md) for the retained capability groups.

Feature maturity is **Not stated by selected sources**.

# Citations

[1] [Project-specific function map](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L55)
[2] [include recursion handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L105-L121)
[3] [Pinned Sprig dependency](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L10)
[4] [Removed environment functions](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62)
