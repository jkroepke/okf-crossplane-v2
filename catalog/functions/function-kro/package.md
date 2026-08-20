---
type: Crossplane Function
title: function-kro
description: Run KRO-style YAML and CEL resource graphs as a Crossplane Composition pipeline step.
resource: https://github.com/crossplane-contrib/function-kro
tags: [crossplane, function, composition, kro, cel, preview]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T22:10:49Z" }
sources:
  - id: package-metadata
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/package/crossplane.yaml#L2-L6'
    title: Function package metadata
  - id: pipeline-usage
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/README.md#L11-L65'
    title: Embedded KRO and ResourceGraph pipeline usage
  - id: selected-dependencies
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/go.mod#L5-L14'
    title: Selected preview dependencies
  - id: kro-versioned-docs
    resource: 'https://github.com/kubernetes-sigs/kro/tree/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs'
    title: KRO v0.9.2 documentation tree
source_repository: crossplane-contrib/function-kro
source_tag: v0.3.0
source_commit: a0b4c088bd950cb407901d01ee29263e6d54d639
source_paths: [README.md, package/crossplane.yaml, go.mod]
release_status: prerelease
selection_basis: User-approved preview revision
feature_state: Not stated by selected sources
---

# Overview

`function-kro` is packaged as a Crossplane `Function` named `function-kro`.
The selected source shows it referenced from a Composition pipeline step with a
[`ResourceGraph` input](input.md).[^package-metadata][^pipeline-usage]

This concept describes the user-approved `v0.3.0` preview at
`a0b4c088bd950cb407901d01ee29263e6d54d639`. The GitHub release is a
prerelease; that source-selection status does not establish package maturity.
Package feature state is **Not stated by selected sources**.

# KRO dependency

The selected preview directly depends on `github.com/kubernetes-sigs/kro`
`v0.9.2`.[^selected-dependencies] KRO terminology and documented expression
semantics in this catalog use only the matching documentation at commit
`22f5645777c86ebd40b6143f248549f1dbe2923f`.[^kro-versioned-docs]

KRO is embedded as a dependency; composition authors do not need to install the
standalone KRO controller for this function's pipeline step.[^pipeline-usage]
The upstream controller's CRD generation, GraphRevision, permissions, and
controller lifecycle are therefore not attributed to function-kro.

# Pipeline placement

Place the function in `spec.pipeline` and reference the installed Function
object by name. The selected README demonstrates the input API
`kro.fn.crossplane.io/v1alpha1` and kind `ResourceGraph`.[^pipeline-usage]

The selected source does not provide an immutable package image reference or a
package-installation command, so this catalog does not invent one.

# Relationships

Use [ResourceGraph input](input.md) for the authoring schema. See
[graph evaluation](graph-evaluation.md) for schema acquisition, desired-resource
identity, readiness, external references, and XR status projection.

[^package-metadata]: [Function package metadata](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/package/crossplane.yaml#L2-L6)
[^pipeline-usage]: [Embedded KRO and ResourceGraph pipeline usage](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/README.md#L11-L65)
[^selected-dependencies]: [Selected preview dependencies](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/go.mod#L5-L14)
[^kro-versioned-docs]: [KRO v0.9.2 documentation tree](https://github.com/kubernetes-sigs/kro/tree/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs)
