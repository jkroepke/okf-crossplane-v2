---
type: functioninput
title: function-environment-configs Input v1beta1
description: Default environment data, ordered EnvironmentConfig references or selectors, cardinality, sorting, and resolution.
resource: https://github.com/crossplane-contrib/function-environment-configs
tags: [crossplane, function, environment-config, schema, beta]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: default-data-and-source-list
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L24-L43'
    title: 'Default data and source list'
  - id: reference-selector-cardinality-and-sorting-types
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L87-L182'
    title: 'Reference, selector, cardinality, and sorting types'
  - id: label-value-sources-and-field-resolution-policy
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L184-L238'
    title: 'Label value sources and field-resolution policy'
  - id: optional-field-path-matchers-and-all-skipped-selector-behavior
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L317-L360'
    title: 'Optional field-path matchers and all-skipped selector behavior'
  - id: resolution-policy-and-unsupported-resolve-option
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L47-L84'
    title: 'Resolution policy and unsupported resolve option'
  - id: runtime-tofieldpath-input
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L115-L118'
    title: 'Runtime toFieldPath input'
  - id: packaged-input-schema-source-properties
    resource: 'https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/input/environmentconfigs.fn.crossplane.io_inputs.yaml#L70-L165'
    title: 'Packaged input schema source properties'
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

`spec.defaultData` is the initial schemaless environment. `spec.environmentConfigs` is an ordered list of sources whose selected data overrides defaults.[^default-data-and-source-list]

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
matcher is skipped, the source generates no resource request.[^reference-selector-cardinality-and-sorting-types][^label-value-sources-and-field-resolution-policy][^optional-field-path-matchers-and-all-skipped-selector-behavior]

The former native `policy.resolve` option is not exposed; the function resolves sources on every invocation.[^resolution-policy-and-unsupported-resolve-option]

# Schema conflict: toFieldPath

Go input types and runtime tests support `environmentConfigs[].toFieldPath`, which groups selected data beneath a destination path. The distributed packaged schema omits this field.[^runtime-tofieldpath-input][^packaged-input-schema-source-properties]

Do not rely on `toFieldPath` in package-validated input until that disagreement is resolved. Even where runtime decoding accepts it, Kubernetes or package schema validation may prune or reject it.

# Stale source comments

Some inherited comments say resolved references are written to
`spec.environmentConfigRefs` and consumed through environment patches. The
released function writes only pipeline context; it does not update XR spec.
Follow [selection and merge behavior](selection-and-merge.md), not those
historical comments.

[^default-data-and-source-list]: [Default data and source list](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L24-L43)
[^reference-selector-cardinality-and-sorting-types]: [Reference, selector, cardinality, and sorting types](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L87-L182)
[^label-value-sources-and-field-resolution-policy]: [Label value sources and field-resolution policy](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L184-L238)
[^optional-field-path-matchers-and-all-skipped-selector-behavior]: [Optional field-path matchers and all-skipped selector behavior](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L317-L360)
[^resolution-policy-and-unsupported-resolve-option]: [Resolution policy and unsupported resolve option](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L47-L84)
[^runtime-tofieldpath-input]: [Runtime toFieldPath input](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/input/v1beta1/composition_environment.go#L115-L118)
[^packaged-input-schema-source-properties]: [Packaged input schema source properties](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/package/input/environmentconfigs.fn.crossplane.io_inputs.yaml#L70-L165)
