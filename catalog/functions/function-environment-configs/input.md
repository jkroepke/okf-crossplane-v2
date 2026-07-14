---
type: functioninput
title: function-environment-configs Input v1beta1
description: Default environment data, ordered EnvironmentConfig references or selectors, cardinality, sorting, and resolution.
resource: https://github.com/crossplane-contrib/function-environment-configs
tags: [crossplane, function, environment-config, schema, beta]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-environment-configs
source_tag: v0.7.2
source_commit: 5589092483aea1d65b9988f5116106585c4b516b
source_paths:
  - input/v1beta1/composition_environment.go
  - package/input/environmentconfigs.fn.crossplane.io_inputs.yaml
feature_state: Beta
feature_state_basis: The packaged schema serves and stores environmentconfigs.fn.crossplane.io/v1beta1.
---

# Schema

`spec.defaultData` is the initial schemaless environment. `spec.environmentConfigs` is an ordered list of sources whose selected data overrides defaults.[1]

| Field | Meaning |
|---|---|
| `environmentConfigs[].type` | `Reference` or `Selector`; defaults to `Reference`. |
| `ref.name` | Exact EnvironmentConfig name for a reference. |
| `selector.mode` | `Single` or `Multiple`; defaults to `Single`. |
| `selector.minMatch` | Minimum accepted matches in Multiple mode. |
| `selector.maxMatch` | Maximum retained matches after sorting in Multiple mode. |
| `selector.sortByFieldPath` | Ascending sort path; defaults to `metadata.name`. |
| `selector.matchLabels[]` | Label key plus literal `Value` or default `FromCompositeFieldPath` source. |
| `policy.resolution` | `Required` by default; `Optional` permits a missing named reference. |

A composite-field matcher is Required by default. With
`policy.resolution: Optional`, a missing XR field skips that matcher; if every
matcher is skipped, the source generates no resource request.[2][3][4]

The former native `policy.resolve` option is not exposed; the function resolves sources on every invocation.[5]

# Schema conflict: toFieldPath

Go input types and runtime tests support `environmentConfigs[].toFieldPath`, which groups selected data beneath a destination path. The distributed packaged schema omits this field.[6][7]

Do not rely on `toFieldPath` in package-validated input until that disagreement is resolved. Even where runtime decoding accepts it, Kubernetes or package schema validation may prune or reject it.

# Stale source comments

Some inherited comments say resolved references are written to
`spec.environmentConfigRefs` and consumed through environment patches. The
released function writes only pipeline context; it does not update XR spec.
Follow [selection and merge behavior](selection-and-merge.md), not those
historical comments.

# Citations

[1] [Default data and source list](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L24-L43)
[2] [Reference, selector, cardinality, and sorting types](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L87-L182)
[3] [Label value sources and field-resolution policy](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L184-L238)
[4] [Optional field-path matchers and all-skipped selector behavior](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L317-L360)
[5] [Resolution policy and unsupported resolve option](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L47-L84)
[6] [Runtime toFieldPath input](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L115-L118)
[7] [Packaged input schema source properties](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/input/environmentconfigs.fn.crossplane.io_inputs.yaml#L70-L165)
