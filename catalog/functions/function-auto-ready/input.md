---
type: functioninput
title: function-auto-ready Input v1beta1
description: Input fields for response caching and CEL readiness customizations in function-auto-ready v0.7.0.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, input, readiness]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [input/v1beta1/input.go, package/input/autoready.fn.crossplane.io_inputs.yaml]
release: v0.7.0
feature_state: Beta
feature_state_basis: The selected generated schema serves and stores v1beta1, which sets a Beta ceiling.
---

# Schema

Use `apiVersion: autoready.fn.crossplane.io/v1beta1` and `kind: Input`. This KRM-like input is not installed as a Kubernetes CRD; the repository generates a CRD-shaped schema to describe it.[1]

| Field | Type | Behavior |
|---|---|---|
| `ttl` | string | Go duration for response caching; generated default is `1m0s`. |
| `celHealthCheckCustomization` | map of strings | Inline GVK-to-CEL rules for the Alpha CEL feature. |
| `celHealthCheckCustomizationFrom` | string | Field path to a CEL-rule map in Function request context. |

The `ttl` value overrides the runtime default. An invalid duration produces a fatal Function response.[2][3]

# Limitations

The selected README's inline CEL examples specify `v1alpha1`, but the selected source and generated schema define only `v1beta1`. Use `v1beta1`; the runnable CEL example also uses it.[4][5]

The CEL fields belong to an explicitly Alpha, default-disabled feature even though the enclosing input API is Beta. See [CEL health checks](cel-health-checks.md).[6]

# Citations

[1] [Input source and non-CRD note](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/input/v1beta1/input.go#L1-L38)
[2] [Generated v1beta1 schema](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/package/input/autoready.fn.crossplane.io_inputs.yaml#L18-L60)
[3] [Runtime TTL parsing](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L40-L54)
[4] [README v1alpha1 examples](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L100-L129)
[5] [Runnable v1beta1 example](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/composition.yaml#L42-L48)
[6] [Alpha feature registration](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/features/features.go#L7-L18)
