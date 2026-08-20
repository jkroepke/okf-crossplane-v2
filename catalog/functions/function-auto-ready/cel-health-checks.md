---
type: function
title: function-auto-ready CEL health checks
description: Alpha, feature-gated readiness expressions evaluated against observed composed resources.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, cel, readiness, alpha]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: alpha-feature-gate
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/features/features.go#L7-L18'
    title: 'Alpha feature gate'
  - id: cel-key-type-and-readiness-mapping
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L23-L71'
    title: 'CEL key, type, and readiness mapping'
  - id: context-and-inline-merge-order
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L100'
    title: 'Context and inline merge order'
  - id: bundled-centralized-cel-example-and-v1beta1-pipeline-wiring
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/composition.yaml#L30-L48'
    title: 'Bundled centralized CEL example and v1beta1 pipeline wiring'
  - id: centralized-environmentconfig-rule-map
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/extra-resources.yaml#L1-L7'
    title: 'Centralized EnvironmentConfig rule map'
  - id: readme-error-and-precedence-description
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L85-L91'
    title: 'README error and precedence description'
  - id: runtime-error-fallthrough
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L119-L159'
    title: 'Runtime error fallthrough'
  - id: readme-v1alpha1-snippets
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L100-L129'
    title: 'README v1alpha1 snippets'
  - id: local-bracket-and-dot-path-parser
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L238-L255'
    title: 'Local bracket-and-dot path parser'
  - id: context-traversal-and-string-map-conversion
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L203-L235'
    title: 'Context traversal and string-map conversion'
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths:
  - README.md
  - features/features.go
  - cel/resolver.go
  - fn.go
  - example/cel-healthcheck/composition.yaml
  - example/cel-healthcheck/extra-resources.yaml
release: v0.7.0
feature_state: Alpha
feature_state_basis: CELHealthcheckCustomizations is explicitly registered as Alpha and disabled by default.
---

# Overview

Enable the `CELHealthcheckCustomizations` Alpha feature gate to define per-GVK readiness expressions. It is disabled by default.[^alpha-feature-gate]

Rule keys use `<group>_<version>_<kind>`, replacing dots in the group with underscores. Each expression receives the observed
resource as `object` and must return a Boolean. `true` sets explicit `Ready=True`; `false` sets explicit `Ready=False`.[^cel-key-type-and-readiness-mapping]

# Sources and precedence

Rules may come from the request context field path named by `celHealthCheckCustomizationFrom`, the inline `celHealthCheckCustomization` map, or both. Context rules load first; inline entries overwrite matching keys.[^context-and-inline-merge-order]

## Centralized rule map

The bundled example centralizes rules in an `EnvironmentConfig`. A preceding
`function-environment-configs` step loads its data beneath
`apiextensions.crossplane.io/environment`; auto-ready then points
`celHealthCheckCustomizationFrom` at that context field.[^bundled-centralized-cel-example-and-v1beta1-pipeline-wiring]

```yaml
data:
  celHealthCheckCustomizations:
    pkg.crossplane.io_v1_Configuration: >-
      object.status.conditions.exists(c, c.type == "Installed" && c.status == "True")
      && object.status.conditions.exists(c, c.type == "Healthy" && c.status == "True")
```

```yaml
input:
  apiVersion: autoready.fn.crossplane.io/v1beta1
  kind: Input
  celHealthCheckCustomizationFrom: >-
    [apiextensions.crossplane.io/environment].celHealthCheckCustomizations
```

These snippets are adapted from the Apache-2.0-licensed v0.7.0 example.[^bundled-centralized-cel-example-and-v1beta1-pipeline-wiring][^centralized-environmentconfig-rule-map] A
context map centralizes policy across Compositions, but it supplies expressions
only: each expression still receives its matched observed composed resource as
`object`. Inline rules remain useful for Composition-specific overrides because
they replace same-key context rules.[^cel-key-type-and-readiness-mapping][^context-and-inline-merge-order]

# Context path behavior

The local path parser preserves dots inside unquoted bracket segments, then
traverses dot-separated keys. A missing key or non-map intermediate silently
yields no context rules. At the terminal map, non-string values are silently
dropped.[^local-bracket-and-dot-path-parser][^context-traversal-and-string-map-conversion]

The parser reports an error only when it extracts no segments and does not
require the entire input to match. Use the documented bracket form exactly;
malformed punctuation may otherwise be partially ignored.[^local-bracket-and-dot-path-parser]

See the [three-function environment pipeline](../environment-config-pipeline.md) for ordering and adaptation guidance.

# Limitations

The README says an evaluation error is treated as not ready and that a customization takes precedence over a built-in check.
The implementation instead emits a Warning and leaves readiness unspecified after an error, allowing later built-in or generic
fallback stages to mark the resource ready. Runtime behavior here follows the implementation.[^readme-error-and-precedence-description][^runtime-error-fallthrough]

The README's CEL snippets use `v1alpha1`, conflicting with the selected [v1beta1 Input](input.md). Use the schema-backed `v1beta1` API.[^readme-v1alpha1-snippets]

[^alpha-feature-gate]: [Alpha feature gate](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/features/features.go#L7-L18)
[^cel-key-type-and-readiness-mapping]: [CEL key, type, and readiness mapping](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L23-L71)
[^context-and-inline-merge-order]: [Context and inline merge order](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L100)
[^bundled-centralized-cel-example-and-v1beta1-pipeline-wiring]: [Bundled centralized CEL example and v1beta1 pipeline wiring](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/composition.yaml#L30-L48)
[^centralized-environmentconfig-rule-map]: [Centralized EnvironmentConfig rule map](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/extra-resources.yaml#L1-L7)
[^readme-error-and-precedence-description]: [README error and precedence description](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L85-L91)
[^runtime-error-fallthrough]: [Runtime error fallthrough](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L119-L159)
[^readme-v1alpha1-snippets]: [README v1alpha1 snippets](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L100-L129)
[^local-bracket-and-dot-path-parser]: [Local bracket-and-dot path parser](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L238-L255)
[^context-traversal-and-string-map-conversion]: [Context traversal and string-map conversion](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L203-L235)
