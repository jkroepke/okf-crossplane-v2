---
type: Crossplane Function Input
title: function-sequencer Input properties and scope safety
description: Configure v1beta1 sequencing, readiness, caching, and optional Usage deletion ordering with explicit mixed-scope safeguards.
resource: https://github.com/crossplane-contrib/function-sequencer
tags: [crossplane, composition-function, sequencing, readiness, deletion, usages]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/function-sequencer
source_tag: v0.6.0
source_commit: 8ee29b46b7b9491fb307cf6caf339541a8d93422
source_paths:
  - input/v1beta1/input.go
  - package/input/sequencer.fn.crossplane.io_inputs.yaml
  - fn.go
  - fn_test.go
feature_state: Beta
feature_state_basis: The Input API is served as sequencer.fn.crossplane.io/v1beta1.
---

# Overview

The function accepts a KRM-like `sequencer.fn.crossplane.io/v1beta1` `Input`.
It generates an Input CRD for description, but never installs that CRD; the
function receives this object as pipeline input.[1] `rules` is the only
required field in the generated definition. The runtime does not validate an
enum for `usageVersion`, a minimum sequence length, or other rule constraints.

# Top-level properties

| Property | Runtime behavior and default | Safety boundary |
| --- | --- | --- |
| `apiVersion`, `kind`, `metadata` | Kubernetes object envelope; `apiVersion` and `kind` identify the Input. | Use `sequencer.fn.crossplane.io/v1beta1` and `Input`. These are not sequencing controls. |
| `cacheTTL` | Empty preserves the SDK response default. A non-empty value is parsed as a Go duration; invalid text returns a fatal result. The generated definition documents `1m`, but this is not a server-applied default. | Set it explicitly when response-cache behavior matters; caching is an Alpha Crossplane runtime feature. |
| `enableDeletionSequencing` | Defaults to Go `false`. When true, generates Usage or ClusterUsage resources for already-observed dependency pairs. | This enables deletion relationships in addition to creation sequencing; audit scope before enabling. |
| `replayDeletion` | Go zero value is `false` and is copied into generated Usage objects. A source annotation says `true`, but the function does not apply that default at runtime. | Set it explicitly; do not rely on the annotation. `true` can replay a previously blocked deletion after the protecting Usage is removed. |
| `usageVersion` | Exact value `v1` selects the legacy `apiextensions.crossplane.io/v1beta1` Usage generator. Empty, `v2`, and any other value select the v2 `protection.crossplane.io/v1beta1` generator. | Set `v2` explicitly. Never use `v1` for namespaced resources; its generator supports cluster-scoped resources only. Unknown values silently take the v2 branch. |
| `resetCompositeReadiness` | Defaults to `false`. When true, sets XR desired readiness false when an unobserved successor is removed because a predecessor is absent or not ready. | It does not remove observed successors and does not itself sequence resources. |
| `rules` | Required by the generated definition; runtime iterates the list and an empty or absent list is effectively a no-op. | Each rule must use composition-resource names, not composed object `metadata.name`. |

# Rule properties

| Property | Runtime behavior and default | Safety boundary |
| --- | --- | --- |
| `sequence` | Ordered resource-name or regex patterns. Matching is strict by default (`^pattern$`). Every matched predecessor must be present in accumulated desired state and `Ready=True` before an unobserved successor remains desired. | Invalid regex is fatal. The function removes only unobserved successors; observed successors are retained. |
| `condition` | Optional CEL over `observed`, `desired`, and `context`. False skips creation gating and emits a Normal result; compile, evaluation, or non-boolean errors are fatal. | With deletion sequencing enabled, observed Usage generation occurs before the condition is applied. A false condition therefore does not remove existing deletion relationships. |
| `deleteOnly` | Defaults to false. Skips creation blocking and readiness reset for that rule, but still permits Usage generation when deletion sequencing is enabled. | It is deletion-ordering policy, not a general “ignore this rule” switch. |

# Mixed-scope Usage safety

Treat `enableDeletionSequencing` and `usageVersion` as a separate risk surface
from creation ordering. In v0.6.0, v2 generation chooses `Usage` versus
`ClusterUsage` from the predecessor (`spec.of`) namespace: a non-empty
predecessor namespace creates namespaced `Usage`; an empty predecessor
namespace creates cluster-scoped `ClusterUsage`.[2]

`ClusterUsage` has no namespace fields for either endpoint. A cluster-scoped XR
that sequences a cluster-scoped predecessor to a namespaced successor can
therefore generate a `ClusterUsage` whose `by` reference cannot identify the
successor namespace. Core resolves ClusterUsage endpoints in the empty
namespace, so the generated relationship cannot become ready or reliably
protect the namespaced resource.[3] Do not enable deletion sequencing for this
mixed-scope relationship. Restructure the dependency, disable deletion
sequencing, or use a released fix that explicitly supports the scope pair.

Issue #114 is an open report by human author `@jkroepke` (created 2026-03-09,
updated 2026-03-10; researched 2026-07-16) of this failure in
function-sequencer v0.5.0; it is not proof that every deployment becomes
undeletable.
The selected v0.6.0 implementation retains the structural risk because its
generated references contain names but no namespace and its scope choice is
based on the predecessor.[4]

`UsageVersion: v1` is an additional hazard: the v1 generator emits the legacy
cluster-scoped Usage kind and documents support only for cluster-scoped
resources. Do not select it for a namespaced relationship.[2]

# Post-release boundary

The user-supplied commit `e277a4070f65fc50dfb08b03d2acdcbdbfe1350b` is after
v0.6.0 and is not a selected stable release. It adds `rules[].createOnly` and
mutual exclusion with `deleteOnly`; do not use that field unless a released
function package containing it has been selected and verified.[5]

# Relationships

See [sequencing behavior](sequencing.md) for the creation-gating outcome and
recommended pipeline position. Core
[Usage and ClusterUsage](../../core/usages-and-clusterusages.md) establish the
separate deletion-protection scope model.

# Citations

[1] [Input type and generated-definition comments](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/input/v1beta1/input.go#L1-L79) and [generated Input definition](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/package/input/sequencer.fn.crossplane.io_inputs.yaml#L17-L95)
[2] [Input parsing, rule processing, Usage generation, and scope discriminator](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L105-L185), [creation gating](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L218-L250), and [Usage generators](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L268-L405)
[3] [Core Usage/ClusterUsage scope and endpoint resolution](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/clusterusage_types.go#L25-L67), [reconciler lookups](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L305-L312), and [namespace-sensitive finder](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/protection/usage/finder.go#L72-L144)
[4] [Issue #114 report](https://github.com/crossplane-contrib/function-sequencer/issues/114), researched 2026-07-16, and [selected v0.6.0 generation path](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L268-L387)
[5] [Post-v0.6.0 `createOnly` change](https://github.com/crossplane-contrib/function-sequencer/blob/e277a4070f65fc50dfb08b03d2acdcbdbfe1350b/input/v1beta1/input.go#L18-L36)
