---
type: pattern
title: Derive readiness from a non-composed resource
description: Fetch a controller-created object with ExtraResources and use its status to set composed-resource readiness.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, extra-resources, readiness]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: extraresources-selector-and-namespace-conversion
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62'
    title: 'ExtraResources selector and namespace conversion'
  - id: getextraresources-lookup
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L154'
    title: 'getExtraResources lookup'
  - id: named-resource-readiness-handling
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350'
    title: 'Named-resource readiness handling'
  - id: function-auto-ready-cel-evaluates-only-the-observed-object
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71'
    title: 'function-auto-ready CEL evaluates only the observed object'
  - id: core-required-resource-fetcher
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L227'
    title: 'Core required-resource fetcher'
  - id: core-client-wiring
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481'
    title: 'Core client wiring'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths: [extraresources.go, function_maps.go, fn.go]
supporting_source_repository: crossplane/crossplane
supporting_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
supporting_source_paths: [internal/xfn/required_resources.go, cmd/crossplane/core/core.go]
feature_state: Alpha
feature_state_basis: ExtraResources uses meta.gotemplating.fn.crossplane.io/v1alpha1.
---

# Pattern

When a composed resource causes another controller to create a separate status
object, that object is absent from `.observed.resources`. Use an Alpha
`ExtraResources` directive to request it, read returned items with
`getExtraResources`, calculate readiness, and emit explicit `"True"` or
`"False"` readiness on the complete desired composed resource.[^extraresources-selector-and-namespace-conversion][^getextraresources-lookup][^named-resource-readiness-handling]

```gotemplate
{{- $knownName := .observed.composite.resource.spec.externalStatus.name }}
{{- $knownNamespace := .observed.composite.resource.spec.externalStatus.namespace }}
---
apiVersion: meta.gotemplating.fn.crossplane.io/v1alpha1
kind: ExtraResources
requirements:
  external-status:
    apiVersion: plattform.example.com/v1beta1
    kind: ExternalStatus
    matchName: {{ $knownName }}
    namespace: {{ $knownNamespace }}
---
{{- $ready := false }}
{{- $items := getExtraResources . "external-status" | default (list) }}
{{- if eq (len $items) 1 }}
  {{- $status := index $items 0 }}
  {{- if eq ($status | getResourceCondition "Ready").Status "True" }}
    {{- $ready = true }}
  {{- end }}
{{- end }}
# Render the complete desired composed resource.
apiVersion: plattform.example.com/v1beta1
kind: Parent
metadata:
  annotations:
    {{ setResourceNameAnnotation "parent" }}
    gotemplating.fn.crossplane.io/ready: {{ ternary "True" "False" $ready | quote }}
spec: {}
```

Replace the placeholder APIs and determine readiness from the external
resource's actual schema. The example is a generic skeleton, not a claim that
`ExternalStatus` or `Parent` APIs exist.

# Selection rules

- Prefer exact `matchName` when the object's deterministic name is known.
- In function-go-templating v0.12.2, exact-name conversion copies `namespace`,
  but label conversion returns without it. Do not use `matchLabels` for a
  namespaced status object in this release.[^extraresources-selector-and-namespace-conversion]
- Treat zero or multiple results as not ready unless the external controller's
  contract explicitly supports another interpretation.
- Ensure the Crossplane Core Deployment service account can read the requested
  API in the target namespace. Core performs the required-resource fetch; the
  Function pod does not.[^core-required-resource-fetcher][^core-client-wiring]

# Relationships

The [Sveltos ClusterSummary pattern](sveltos-clustersummary-readiness.md) applies
this flow using Sveltos's deterministic summary name and feature-status model.
See [manual readiness](manual-readiness.md) for annotation semantics and
[ExtraResources](../extra-resources.md) for fetch stabilization and no-match
behavior.
See [composed-resource RBAC](../../../core/composed-resource-rbac.md) for the
principal and grant boundary.

# Limitations

function-auto-ready cannot directly evaluate the fetched object because its
CEL activation contains only the matched observed composed resource.[^function-auto-ready-cel-evaluates-only-the-observed-object] An
earlier function-go-templating step must therefore translate external status
into explicit composed-resource readiness.

[^extraresources-selector-and-namespace-conversion]: [ExtraResources selector and namespace conversion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62)
[^getextraresources-lookup]: [`getExtraResources` lookup](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L154)
[^named-resource-readiness-handling]: [Named-resource readiness handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
[^function-auto-ready-cel-evaluates-only-the-observed-object]: [function-auto-ready CEL evaluates only the observed object](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71)
[^core-required-resource-fetcher]: [Core required-resource fetcher](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L227) and [Core client wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
[^core-client-wiring]: [Core client wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
