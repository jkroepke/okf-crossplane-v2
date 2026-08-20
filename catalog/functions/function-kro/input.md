---
type: Crossplane Function Input
title: function-kro ResourceGraph input
description: Author Alpha ResourceGraph inputs with templates, external references, collections, conditions, readiness, status, and CEL expressions.
resource: https://github.com/crossplane-contrib/function-kro
tags: [crossplane, function, kro, resource-graph, cel, alpha, preview]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T22:10:49Z" }
sources:
  - id: input-type
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/input/v1alpha1/input.go#L1-L30'
    title: ResourceGraph input type
  - id: packaged-schema
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/package/input/kro.fn.crossplane.io_resourcegraphs.yaml#L41-L210'
    title: Packaged ResourceGraph schema
  - id: readme-expressions
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/README.md#L20-L65'
    title: ResourceGraph and CEL example
  - id: kro-resource-basics
    resource: 'https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/02-resource-definitions/01-resource-basics.md#L10-L81'
    title: KRO v0.9.2 resource basics
  - id: kro-cel-expressions
    resource: 'https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/03-cel-expressions.md#L34-L114'
    title: KRO v0.9.2 CEL expressions
source_repository: crossplane-contrib/function-kro
source_tag: v0.3.0
source_commit: a0b4c088bd950cb407901d01ee29263e6d54d639
source_paths:
  - input/v1alpha1/input.go
  - package/input/kro.fn.crossplane.io_resourcegraphs.yaml
  - README.md
supporting_sources:
  - repository: kubernetes-sigs/kro
    tag: v0.9.2
    commit: 22f5645777c86ebd40b6143f248549f1dbe2923f
    paths: [website/docs/docs/concepts/rgd]
release_status: prerelease
selection_basis: User-approved preview revision
feature_state: Alpha
feature_state_basis: The Function input API is served as kro.fn.crossplane.io/v1alpha1.
---

# Overview

The function accepts a KRM-like `kro.fn.crossplane.io/v1alpha1` object with
kind `ResourceGraph`. Its generated CRD describes the input schema but is not
installed as a Kubernetes custom resource.[^input-type]

This input API is **Alpha** because its served version is `v1alpha1`. That
ceiling applies to the input and patterns that require it, not to the
[function package](package.md).

# Schema

The top-level `status` and `resources` fields are optional. `status` is an
arbitrary object of CEL projections; `resources` is an array of KRO resource
definitions.[^input-type][^packaged-schema]

| Resource field | Contract in the selected preview |
| --- | --- |
| `id` | Required identifier used by CEL references. |
| `template` | Kubernetes manifest to create; exactly one of `template` or `externalRef` is required. |
| `externalRef` | Existing resource to read; requires `apiVersion`, `kind`, and metadata with exactly one of `name` or `selector`. |
| `forEach` | Array of single-entry iterator maps; each expression produces an array and multiple entries form a Cartesian product. |
| `includeWhen` | Boolean CEL expressions; all must be true for inclusion. |
| `readyWhen` | Boolean CEL expressions used to determine readiness. |

These constraints come from the packaged schema at the selected function
commit.[^packaged-schema]

# CEL expressions

Resource templates and status use `${...}` CEL expressions, including
references to the XR through `schema` and to other graph resources by ID.[^readme-expressions]
The version-matched KRO documentation distinguishes whole-field expressions,
which preserve their CEL result type, from expressions embedded in strings,
which must produce strings.[^kro-cel-expressions]

KRO's documentation also describes resource IDs, Kubernetes templates, and
schema-backed checking.[^kro-resource-basics] Function-kro's packaged schema and
runtime remain authoritative for what this preview actually accepts and emits.

# External-reference namespace boundary

For a named reference, an omitted namespace defaults to the XR namespace. For
a selector collection, an empty namespace means an all-namespace list.[^packaged-schema]
The latter therefore has a wider read scope than a namespace-constrained selector.

# Relationships

See [graph evaluation](graph-evaluation.md) for how the function obtains schemas,
evaluates these fields, names desired resources, reports readiness, and projects
status.

[^input-type]: [ResourceGraph input type](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/input/v1alpha1/input.go#L1-L30)
[^packaged-schema]: [Packaged ResourceGraph schema](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/package/input/kro.fn.crossplane.io_resourcegraphs.yaml#L41-L210)
[^readme-expressions]: [ResourceGraph and CEL example](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/README.md#L20-L65)
[^kro-resource-basics]: [KRO v0.9.2 resource basics](https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/02-resource-definitions/01-resource-basics.md#L10-L81)
[^kro-cel-expressions]: [KRO v0.9.2 CEL expressions](https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/03-cel-expressions.md#L34-L114)
