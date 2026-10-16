---
type: pattern
title: Mark composed resources ready from observed state
description: Set explicit composed-resource readiness from a condition or guarded field check in a Go template.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, readiness, go-template]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T20:00:00Z" }
sources:
  - id: readiness-value-parsing
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L203-L218'
    title: 'Readiness value parsing'
  - id: named-resource-readiness-handling-and-annotation-removal
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350'
    title: 'Named-resource readiness handling and annotation removal'
  - id: getresourcecondition-behavior-and-bundled-example
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L89-L99'
    title: 'getResourceCondition behavior and bundled example'
  - id: getcomposedresource-behavior
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L132'
    title: 'getComposedResource behavior'
  - id: function-auto-ready-preserves-explicit-readiness
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179'
    title: 'function-auto-ready preserves explicit readiness'
  - id: function-auto-ready-cel-activation-contains-the-observed-object
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71'
    title: 'function-auto-ready CEL activation contains the observed object'
  - id: v0-13-0-unknown-ready-alias
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L238-L258'
    title: 'v0.13.0 Unknown ready-annotation alias'
  - id: v0-13-0-unknown-alias-test
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1439-L1470'
    title: 'v0.13.0 CompositeResourceReadyUnknownAlias test'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths:
  - README.md
  - fn.go
  - fn_test.go
  - function_maps.go
  - example/functions/getComposedResource/composition.yaml
  - example/functions/getResourceCondition/composition.yaml
feature_state: Beta
feature_state_basis: The containing GoTemplate input serves v1beta1, which sets a Beta ceiling.
---

# Overview

A Go template can set `gotemplating.fn.crossplane.io/ready` on a complete
rendered composed resource. In v0.12.2 the annotation accepts exactly `"True"`,
`"False"`, or `"Unspecified"`; another value produces a fatal function result.
From v0.13.0 it also accepts `"Unknown"`, an exact case-sensitive match treated
as `"Unspecified"`, so a Kubernetes condition status from `getResourceCondition`
can be passed through unchanged. The fatal error text still lists only `True`,
`False`, or `Unspecified`.[^v0-13-0-unknown-ready-alias][^v0-13-0-unknown-alias-test] The
function copies the parsed value to the desired-resource readiness field and
removes the control annotation from the Kubernetes manifest.[^readiness-value-parsing][^named-resource-readiness-handling-and-annotation-removal]

The rendered object must also have a composition resource name. A readiness
annotation by itself is not a standalone instruction; render the complete
desired object on every reconciliation.[^named-resource-readiness-handling-and-annotation-removal]

# Condition example

`getResourceCondition` accepts the request wrapper stored in
`.observed.resources` and returns an `Unknown` condition when the condition or
status path is absent.[^getresourcecondition-behavior-and-bundled-example] This adapted fragment keeps a Deployment explicitly
not ready until its `Available` condition becomes true:

```gotemplate
{{- $deployment := index .observed.resources "deployment" }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example
  annotations:
    {{ setResourceNameAnnotation "deployment" }}
    {{- if eq ($deployment | getResourceCondition "Available").Status "True" }}
    gotemplating.fn.crossplane.io/ready: "True"
    {{- else }}
    gotemplating.fn.crossplane.io/ready: "False"
    {{- end }}
spec:
  # Render the complete desired Deployment spec here.
```

# Field examples

`getComposedResource . "name"` returns the unwrapped observed object or `nil`.
Guard the result before traversing it.[^getcomposedresource-behavior]

```gotemplate
{{- $serviceReady := false }}
{{- with (getComposedResource . "service") }}
  {{- if get .spec "clusterIP" }}
    {{- $serviceReady = true }}
  {{- end }}
{{- end }}
metadata:
  annotations:
    {{ setResourceNameAnnotation "service" }}
    gotemplating.fn.crossplane.io/ready: {{ ternary "True" "False" $serviceReady | quote }}
```

For an Ingress, similarly guard the observed object and require at least one
entry under `status.loadBalancer.ingress`; do not index element zero before
checking the list length.

# Choosing manual or automatic readiness

Use a manual annotation when readiness depends on an application-specific
condition, field, or
[non-composed resource](non-composed-resource-readiness.md).
Use [function-auto-ready](../../function-auto-ready/readiness.md) when its built-in
Kubernetes checks, generic `Ready=True` fallback, or Alpha CEL customization
matches the observed composed resource.

A later function-auto-ready step preserves explicit `True` and `False`
decisions made by this template.[^function-auto-ready-preserves-explicit-readiness] Its CEL expression receives only the
matched observed composed object, so CEL does not directly evaluate a separate
`ExtraResources` result.[^function-auto-ready-cel-activation-contains-the-observed-object]

# Limitations

- Explicit `False` is authoritative to a later auto-ready step. Use
  `Unspecified` only when a later step should decide readiness.
- Passing a condition status straight through on v0.13.0 or later turns an
  absent or `Unknown` condition into `Unspecified`, which hands the decision to
  a later step instead of forcing not ready.[^getresourcecondition-behavior-and-bundled-example][^v0-13-0-unknown-ready-alias]
- Guard field paths that may be absent during initial reconciliation.
- The examples are adapted integration fragments under the source project's
  Apache-2.0 license; replace abbreviated specs with complete desired objects.

[^readiness-value-parsing]: [Readiness value parsing](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L203-L218)
[^named-resource-readiness-handling-and-annotation-removal]: [Named-resource readiness handling and annotation removal](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
[^getresourcecondition-behavior-and-bundled-example]: [`getResourceCondition` behavior and bundled example](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L89-L99)
[^getcomposedresource-behavior]: [`getComposedResource` behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L132)
[^function-auto-ready-preserves-explicit-readiness]: [function-auto-ready preserves explicit readiness](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[^function-auto-ready-cel-activation-contains-the-observed-object]: [function-auto-ready CEL activation contains the observed object](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71)
[^v0-13-0-unknown-ready-alias]: [v0.13.0 `Unknown` ready-annotation alias](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L238-L258)
[^v0-13-0-unknown-alias-test]: [v0.13.0 `CompositeResourceReadyUnknownAlias` test](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1439-L1470)
