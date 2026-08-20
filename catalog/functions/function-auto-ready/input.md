---
type: functioninput
title: function-auto-ready Input v1beta1
description: Input fields for response caching and CEL readiness customizations in function-auto-ready v0.7.0.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, input, readiness]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: input-source-and-non-crd-note
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/input/v1beta1/input.go#L1-L38'
    title: 'Input source and non-CRD note'
  - id: generated-v1beta1-schema
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/package/input/autoready.fn.crossplane.io_inputs.yaml#L18-L60'
    title: 'Generated v1beta1 schema'
  - id: runtime-ttl-parsing
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L40-L54'
    title: 'Runtime TTL parsing'
  - id: readme-v1alpha1-examples
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L100-L129'
    title: 'README v1alpha1 examples'
  - id: runnable-v1beta1-example
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/composition.yaml#L42-L48'
    title: 'Runnable v1beta1 example'
  - id: alpha-feature-registration
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/features/features.go#L7-L18'
    title: 'Alpha feature registration'
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [input/v1beta1/input.go, package/input/autoready.fn.crossplane.io_inputs.yaml]
release: v0.7.0
feature_state: Beta
feature_state_basis: The selected generated schema serves and stores v1beta1, which sets a Beta ceiling.
---

# Schema

Use `apiVersion: autoready.fn.crossplane.io/v1beta1` and `kind: Input`. This KRM-like input is not installed as a Kubernetes CRD; the repository generates a CRD-shaped schema to describe it.[^input-source-and-non-crd-note]

| Field | Type | Behavior |
|---|---|---|
| `ttl` | string | Go duration for response caching; generated default is `1m0s`. |
| `celHealthCheckCustomization` | map of strings | Inline GVK-to-CEL rules for the Alpha CEL feature. |
| `celHealthCheckCustomizationFrom` | string | Field path to a CEL-rule map in Function request context. |

The `ttl` value overrides the runtime default. An invalid duration produces a fatal Function response.[^generated-v1beta1-schema][^runtime-ttl-parsing]

# Limitations

The selected README's inline CEL examples specify `v1alpha1`, but the selected source and generated schema define only `v1beta1`. Use `v1beta1`; the runnable CEL example also uses it.[^readme-v1alpha1-examples][^runnable-v1beta1-example]

The CEL fields belong to an explicitly Alpha, default-disabled feature even though the enclosing input API is Beta. See [CEL health checks](cel-health-checks.md).[^alpha-feature-registration]

[^input-source-and-non-crd-note]: [Input source and non-CRD note](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/input/v1beta1/input.go#L1-L38)
[^generated-v1beta1-schema]: [Generated v1beta1 schema](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/package/input/autoready.fn.crossplane.io_inputs.yaml#L18-L60)
[^runtime-ttl-parsing]: [Runtime TTL parsing](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L40-L54)
[^readme-v1alpha1-examples]: [README v1alpha1 examples](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L100-L129)
[^runnable-v1beta1-example]: [Runnable v1beta1 example](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/composition.yaml#L42-L48)
[^alpha-feature-registration]: [Alpha feature registration](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/features/features.go#L7-L18)
