---
type: function
title: Rendered resources, readiness, status, and recursion
description: Control desired resources and v2 composite output produced by Go templates.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, readiness, recursion]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Behavior

The annotation `gotemplating.fn.crossplane.io/composition-resource-name` identifies a rendered composed resource; `setResourceNameAnnotation` emits it.[1] The `gotemplating.fn.crossplane.io/ready`
annotation marks a rendered composed or composite resource ready or not ready.[2]

For v2 composite resources, render a composed Kubernetes `Secret` for connection details.[3]

Rendering the composite's own type without a composition-resource-name annotation updates composite status. Adding the annotation instead creates a composed resource of that type.[4]

# Recursion

A template can create a composite resource of the same type. Its `compositionRef` must eventually select a different composition that terminates recursion; otherwise reconciliation can loop indefinitely.[4]

Feature maturity is **Not stated by selected sources**. Claim-targeted condition material and legacy v1 XR connection behavior were excluded.

# Citations

[1] [Resource-name helper](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103)
[2] [Readiness annotation](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L124-L147)
[3] [v2 connection details](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L101-L122)
[4] [Status, same-type resources, and recursion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L279-L350)
