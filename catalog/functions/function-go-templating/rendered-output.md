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
source_paths: [function_maps.go, fn.go, README.md]
supporting_source_repository: crossplane/crossplane-runtime
supporting_source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
supporting_source_paths: [pkg/xcrd/composite.go]
crossplane_source_repository: crossplane/crossplane
crossplane_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
crossplane_source_paths: [internal/controller/apiextensions/composite/composition_render.go]
feature_state: Not stated by selected sources
---

# Behavior

The annotation `gotemplating.fn.crossplane.io/composition-resource-name` identifies a rendered composed resource and selects its logical desired-map key inside function-go-templating; `setResourceNameAnnotation` emits it.[1][7] Crossplane Core later persists its separate `crossplane.io/composition-resource-name` annotation on the actual composed object. Both represent logical composition identity, but neither is Kubernetes `metadata.name`.[5][6] The `gotemplating.fn.crossplane.io/ready`
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
[5] [Core composition-resource annotation key and accessors](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)
[6] [Core persists the logical resource key on the rendered object](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100)
[7] [Function consumes the annotation as the desired resource-map key](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
