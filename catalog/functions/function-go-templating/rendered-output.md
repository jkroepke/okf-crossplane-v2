---
type: function
title: Rendered resources, readiness, status, and recursion
description: Control desired resources and v2 composite output produced by Go templates.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, readiness, recursion]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T20:00:00Z" }
sources:
  - id: resource-name-helper
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103'
    title: 'Resource-name helper'
  - id: readiness-annotation
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L124-L147'
    title: 'Readiness annotation'
  - id: v2-connection-details
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L101-L122'
    title: 'v2 connection details'
  - id: status-same-type-resources-and-recursion
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L279-L350'
    title: 'Status, same-type resources, and recursion'
  - id: core-composition-resource-annotation-key-and-accessors
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40'
    title: 'Core composition-resource annotation key and accessors'
  - id: core-persists-the-logical-resource-key-on-the-rendered-object
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100'
    title: 'Core persists the logical resource key on the rendered object'
  - id: function-consumes-the-annotation-as-the-desired-resource-map-key
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350'
    title: 'Function consumes the annotation as the desired resource-map key'
  - id: v0-13-0-unknown-ready-alias
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L238-L258'
    title: 'v0.13.0 Unknown ready-annotation alias'
  - id: v0-13-0-ready-applied-composite
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L302-L305'
    title: 'v0.13.0 ready value applied to the composite resource'
  - id: v0-13-0-ready-applied-composed
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L377-L380'
    title: 'v0.13.0 ready value applied to composed resources'
  - id: v0-13-0-unknown-alias-test
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1439-L1470'
    title: 'v0.13.0 CompositeResourceReadyUnknownAlias test'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths: [function_maps.go, fn.go, fn_test.go, README.md]
supporting_source_repository: crossplane/crossplane-runtime
supporting_source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
supporting_source_paths: [pkg/xcrd/composite.go]
crossplane_source_repository: crossplane/crossplane
crossplane_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
crossplane_source_paths: [internal/controller/apiextensions/composite/composition_render.go]
feature_state: Not stated by selected sources
---

# Behavior

The annotation `gotemplating.fn.crossplane.io/composition-resource-name` identifies a rendered composed resource and selects its logical desired-map key inside function-go-templating; `setResourceNameAnnotation` emits it.[^resource-name-helper][^function-consumes-the-annotation-as-the-desired-resource-map-key] Crossplane Core later persists its separate `crossplane.io/composition-resource-name` annotation on the actual composed object. Both represent logical composition identity, but neither is Kubernetes `metadata.name`.[^core-composition-resource-annotation-key-and-accessors][^core-persists-the-logical-resource-key-on-the-rendered-object] The `gotemplating.fn.crossplane.io/ready`
annotation marks a rendered composed or composite resource ready or not ready.[^readiness-annotation] It accepts `True`, `False`, and `Unspecified`; from v0.13.0 `Unknown` is an alias for `Unspecified` on both composed and composite resources.[^v0-13-0-unknown-ready-alias][^v0-13-0-ready-applied-composite][^v0-13-0-ready-applied-composed][^v0-13-0-unknown-alias-test]

For v2 composite resources, render a composed Kubernetes `Secret` for connection details.[^v2-connection-details]

Rendering the composite's own type without a composition-resource-name annotation updates composite status. Adding the annotation instead creates a composed resource of that type.[^status-same-type-resources-and-recursion]

# Recursion

A template can create a composite resource of the same type. Its `compositionRef` must eventually select a different composition that terminates recursion; otherwise reconciliation can loop indefinitely.[^status-same-type-resources-and-recursion]

Feature maturity is **Not stated by selected sources**. Claim-targeted condition material and legacy v1 XR connection behavior were excluded.

[^resource-name-helper]: [Resource-name helper](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103)
[^readiness-annotation]: [Readiness annotation](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L124-L147)
[^v2-connection-details]: [v2 connection details](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L101-L122)
[^status-same-type-resources-and-recursion]: [Status, same-type resources, and recursion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L279-L350)
[^core-composition-resource-annotation-key-and-accessors]: [Core composition-resource annotation key and accessors](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)
[^core-persists-the-logical-resource-key-on-the-rendered-object]: [Core persists the logical resource key on the rendered object](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100)
[^function-consumes-the-annotation-as-the-desired-resource-map-key]: [Function consumes the annotation as the desired resource-map key](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
[^v0-13-0-unknown-ready-alias]: [v0.13.0 `Unknown` ready-annotation alias](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L238-L258)
[^v0-13-0-ready-applied-composite]: [v0.13.0 ready value applied to the composite resource](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L302-L305)
[^v0-13-0-ready-applied-composed]: [v0.13.0 ready value applied to composed resources](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L377-L380)
[^v0-13-0-unknown-alias-test]: [v0.13.0 `CompositeResourceReadyUnknownAlias` test](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1439-L1470)
