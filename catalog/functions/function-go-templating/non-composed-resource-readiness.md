---
type: pattern
title: Derive readiness from a non-composed resource
description: Fetch a controller-created object with ExtraResources and use its status to set composed-resource readiness.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, extra-resources, readiness]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths: [extraresources.go, function_maps.go, fn.go]
feature_state: Alpha
feature_state_basis: ExtraResources uses meta.gotemplating.fn.crossplane.io/v1alpha1.
---

# Pattern

When a composed resource causes another controller to create a separate status
object, that object is absent from `.observed.resources`. Use an Alpha
`ExtraResources` directive to request it, read returned items with
`getExtraResources`, calculate readiness, and emit explicit `"True"` or
`"False"` readiness on the complete desired composed resource.[1][2][3]

```gotemplate
{{- $knownName := .observed.composite.resource.spec.externalStatus.name }}
{{- $knownNamespace := .observed.composite.resource.spec.externalStatus.namespace }}
---
apiVersion: meta.gotemplating.fn.crossplane.io/v1alpha1
kind: ExtraResources
requirements:
  external-status:
    apiVersion: example.org/v1beta1
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
apiVersion: example.org/v1beta1
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
  namespaced status object in this release.[1]
- Treat zero or multiple results as not ready unless the external controller's
  contract explicitly supports another interpretation.
- Ensure the function service account can read the requested API in the target
  namespace.

# Relationships

The [Sveltos ClusterSummary pattern](external-resource-readiness.md) applies
this flow using Sveltos's deterministic summary name and feature-status model.
See [manual readiness](manual-readiness.md) for annotation semantics and
[ExtraResources](extra-resources.md) for fetch stabilization and no-match
behavior.

# Limitations

function-auto-ready cannot directly evaluate the fetched object because its
CEL activation contains only the matched observed composed resource.[4] An
earlier function-go-templating step must therefore translate external status
into explicit composed-resource readiness.

# Citations

[1] [ExtraResources selector and namespace conversion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62)
[2] [`getExtraResources` lookup](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L154)
[3] [Named-resource readiness handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
[4] [function-auto-ready CEL evaluates only the observed object](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71)
