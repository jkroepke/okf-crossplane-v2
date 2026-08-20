---
type: Crossplane Function
title: function-kro graph evaluation
description: Build a schema-aware graph, evaluate desired resources topologically, preserve stable identities, report readiness, and project declared XR status.
resource: https://github.com/crossplane-contrib/function-kro
tags: [crossplane, function, kro, graph, desired-state, readiness, status, alpha, preview]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T22:10:49Z" }
sources:
  - id: schema-request-flow
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L81-L116'
    title: Schema request and graph construction flow
  - id: schema-capability-paths
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L277-L375'
    title: Required-schema and CRD fallback paths
  - id: external-reference-flow
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L117-L173'
    title: External-reference required-resource flow
  - id: desired-evaluation
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L614-L689'
    title: Desired-resource evaluation, identity, and readiness
  - id: status-projection
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L692-L720'
    title: Minimal desired XR status projection
  - id: fatal-results
    resource: 'https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L62-L79'
    title: Input and observed-XR fatal results
  - id: kro-dependencies
    resource: 'https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/04-dependencies-ordering.md#L5-L43'
    title: KRO v0.9.2 dependency inference
  - id: kro-external-references
    resource: 'https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/02-resource-definitions/05-external-references.md#L5-L89'
    title: KRO v0.9.2 external-reference semantics
source_repository: crossplane-contrib/function-kro
source_tag: v0.3.0
source_commit: a0b4c088bd950cb407901d01ee29263e6d54d639
source_paths: [fn.go]
supporting_sources:
  - repository: kubernetes-sigs/kro
    tag: v0.9.2
    commit: 22f5645777c86ebd40b6143f248549f1dbe2923f
    paths: [website/docs/docs/concepts/rgd]
release_status: prerelease
selection_basis: User-approved preview revision
feature_state: Alpha
feature_state_basis: This behavior requires the kro.fn.crossplane.io/v1alpha1 ResourceGraph input.
---

# Behavior

On each invocation, function-kro:

1. Reads the Alpha [`ResourceGraph` input](input.md) and observed XR.
2. Collects the XR and graph resource GVKs and requests their schemas.
3. Builds the resource graph and supplies external and composed observed state.
4. Evaluates runtime nodes in topological order into desired composed resources.
5. Returns the accumulated desired resources and only declared, resolved XR
   status paths.[^schema-request-flow][^desired-evaluation][^status-projection]

This behavior is **Alpha** because it requires the function's `v1alpha1` input.
It does not assign Alpha maturity to the package itself.

# Schema acquisition

When Crossplane advertises `required_schemas`, the function requests schemas for
the XR and every graph GVK. The selected source identifies this as the Crossplane
2.2-and-later path. Otherwise, it requests matching CRDs as required resources.[^schema-capability-paths]

Schema acquisition can require multiple function invocations. While required
schemas are unavailable, the function returns requirements without a fatal
result and waits for Crossplane to call it again.[^schema-request-flow]

# Dependency and desired-state evaluation

The matching KRO `v0.9.2` documentation defines CEL references as dependency
edges and describes topological ordering.[^kro-dependencies] Function-kro's
runtime walks graph nodes in that order. It excludes read-only external
references, resources whose `includeWhen` evaluates false, and resources whose
expression data is still pending.[^desired-evaluation]

Desired objects come from evaluated templates rather than observed objects, so
provider-defaulted observed fields are not copied into the function's desired
SSA ownership.[^desired-evaluation]

# Identity and readiness

A single resource uses its graph node ID as the Crossplane desired-resource
name. A `forEach` collection member uses `{id}-{metadata.name}`, avoiding list
position as its cross-reconcile identity.[^desired-evaluation]

When `readyWhen` is present, the function reports explicit ready or not-ready
state from its evaluation. Without `readyWhen`, it leaves readiness unspecified
so a later pipeline function such as function-auto-ready can decide it.[^desired-evaluation]

# External references

The function turns external references into Crossplane required-resource
selectors, supplies returned objects to the graph runtime, and never includes
them in desired composed output.[^external-reference-flow][^desired-evaluation]
The version-matched KRO documentation defines them as read-only references and
distinguishes name from selector modes.[^kro-external-references]

# XR status ownership

The desired XR contains only ResourceGraph-declared status paths whose CEL
values have resolved. This bounds the function's desired XR status ownership;
unresolved paths are omitted until a later invocation.[^status-projection]

# Errors and limitations

Invalid input and observed-XR retrieval or decoding errors become fatal Function
results.[^fatal-results] Graph construction, runtime evaluation, and desired
resource conversion errors also stop that invocation; pending schemas and pending
expression data are deferrals rather than equivalent fatal errors.

KRO controller installation, generated CRDs, GraphRevisions, controller
permissions, and standalone reconciliation behavior are outside this concept.

[^schema-request-flow]: [Schema request and graph construction flow](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L81-L116)
[^schema-capability-paths]: [Required-schema and CRD fallback paths](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L277-L375)
[^external-reference-flow]: [External-reference required-resource flow](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L117-L173)
[^desired-evaluation]: [Desired-resource evaluation, identity, and readiness](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L614-L689)
[^status-projection]: [Minimal desired XR status projection](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L692-L720)
[^fatal-results]: [Input and observed-XR fatal results](https://github.com/crossplane-contrib/function-kro/blob/a0b4c088bd950cb407901d01ee29263e6d54d639/fn.go#L62-L79)
[^kro-dependencies]: [KRO v0.9.2 dependency inference](https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/04-dependencies-ordering.md#L5-L43)
[^kro-external-references]: [KRO v0.9.2 external-reference semantics](https://github.com/kubernetes-sigs/kro/blob/22f5645777c86ebd40b6143f248549f1dbe2923f/website/docs/docs/concepts/rgd/02-resource-definitions/05-external-references.md#L5-L89)
