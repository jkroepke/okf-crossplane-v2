---
type: function
title: EnvironmentConfig selection and merge behavior
description: Iterative resource requests, selector cardinality, sorting, deep-merge precedence, context output, and failure behavior.
resource: https://github.com/crossplane-contrib/function-environment-configs
tags: [crossplane, function, environment-config, context, merge]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-environment-configs
source_tag: v0.7.2
source_commit: 5589092483aea1d65b9988f5116106585c4b516b
source_paths: [fn.go, fn_test.go]
feature_state: Beta
feature_state_basis: The function input and selected EnvironmentConfig API are v1beta1.
---

# Function iterations

Each configured source becomes a required-resource request named
`environment-config-<input-index>` for
`apiextensions.crossplane.io/v1beta1`, kind `EnvironmentConfig`, matched by name
or labels. The function returns requirements on every invocation; when results
are not yet present, it returns without writing environment context.[1]

Reference mode accepts exactly one object. A required zero match or more than one returned object is fatal; an Optional zero match is skipped.[2]

Selector behavior is:

- `Single` requires exactly one returned object.
- `Multiple` validates `minMatch`, sorts ascending, then truncates to `maxMatch`.
- Sorting accepts consistently typed strings, integers, or floating-point values. Mixed or unsupported types error. Missing paths use the chosen type's zero value; if all paths are absent, incoming order remains.[3]

# Merge precedence

The function recursively merges maps and replaces conflicting non-map values. Higher-precedence values are:

1. later selected EnvironmentConfigs over earlier selected EnvironmentConfigs;
2. selected EnvironmentConfig data over `defaultData`;
3. `defaultData` over an incoming environment already present in request context.[4]

The result is written at `apiextensions.crossplane.io/environment`. When the merged map has no GVK fields, the function adds `apiVersion: internal.crossplane.io/v1alpha1` and `kind: Environment` inside the context value.[5]

For sources sharing one `toFieldPath`, source and sorted match order are
retained. Across distinct overlapping destination buckets, the implementation
iterates a Go map, so relative overwrite order is unspecified. This is another
reason not to depend on the currently schema-conflicted field.[6]

# Failure behavior

Invalid input, observed XR decoding, selector construction, returned-resource
decoding, selection, sorting, merging, or protobuf conversion produces a fatal
function result. Missing required resources during the normal requirements
iteration are not fatal until a returned result establishes a zero-match case
subject to the selected policy.[1][2][3]

# Relationships

Later steps can consume the output through [function-go-templating](../function-go-templating/environment-source.md) or the Alpha [function-auto-ready CEL context source](../function-auto-ready/cel-health-checks.md).

# Citations

[1] [Requirement construction and iteration return](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L64-L77)
[2] [Reference and selector cardinality](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L178-L218)
[3] [Sorting implementation](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L221-L315)
[4] [Merge inputs and precedence](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L101-L120)
[5] [Context key and output GVK](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L122-L134)
[6] [Destination grouping and map iteration](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L138-L175)
