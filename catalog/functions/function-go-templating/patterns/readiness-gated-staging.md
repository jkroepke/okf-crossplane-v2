---
type: Crossplane Example
title: Readiness-gated staged resource introduction
description: Introduce dependent composed resources after an observed prerequisite is Ready, then retain them to prevent deletion on later reconciliations.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, readiness, staged-rendering, desired-state]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
crossplane_release: v2.3.3
documentation_series: v2.3
feature_state: Beta
feature_state_basis: The containing GoTemplate input API serves gotemplating.fn.crossplane.io/v1beta1.
---

# Overview

A condition such as `{{ if or $bucketReady $prerequisitesIntroduced }}` is a
useful **readiness-gated staged-introduction** pattern. It does not order the
provider's application of composed resources. Instead, it decides when a
resource first enters the final desired state returned for a reconciliation.

Stable composition-resource names let later requests identify observed
resources by key.[1] A function must reproduce a desired resource on later
reconciliations; omitting one causes Crossplane to delete it.[3] The observed
key in the second operand is therefore a retention latch, not redundant
defensive code.

# Three-stage example

| Stage | First-emission gate | Retention gate | Meaning |
| --- | --- | --- | --- |
| Bucket | Always emit | Always emit | Establish the prerequisite. |
| Ownership controls and public-access block | Bucket observed `Ready=True` | Either child resource key is observed | Do not introduce controls prematurely; keep both desired after either has appeared. |
| ACL | Both controls observed `Ready=True` | ACL resource key is observed | Do not introduce the ACL prematurely; keep it desired after first observation. |

```gotemplate
{{- $controlsIntroduced := or
      (hasKey $observed "ownership-controls")
      (hasKey $observed "public-access-block") -}}
{{- $aclIntroduced := hasKey $observed "public-acl" -}}

{{ if or $bucketReady $controlsIntroduced }}
# Render both control resources with stable composition-resource names.
{{ end }}

{{ if or (and $ownershipReady $publicAccessReady) $aclIntroduced }}
# Render the ACL with a stable composition-resource name.
{{ end }}
```

This is an adapted, provider-neutral rendering pattern. The Bucket sequence is
user-supplied; it was not independently executed against the pinned releases.

# What it guarantees—and what it does not

Crossplane observes the composite and composed resources before the pipeline
runs. Pipeline steps execute in order and receive accumulated desired state,
but the final desired resource map is applied only after the pipeline
completes.[2][4] This pattern therefore guarantees **first-emission order
across reconciliation rounds**, not ordered or transactional provider-side
application within a round.

An observed-key latch also does not provide durable workflow state. If a
resource is actually absent from a future observed snapshot, the latch no
longer retains it. Use this pattern to avoid accidental deletion, not to model
rollback, retries, or a long-running transaction.

# Ready-regression proof and first-observation boundary

For the ACL gate, let `P` be `ownershipReady && publicAccessReady` and `A` be
`aclIntroduced`. The emitted condition is `P || A`. Once the ACL has appeared
in observed state, `A` is true, so `P || true` is true even if the Bucket or
either control later reports not ready. A readiness regression alone therefore
does **not** de-provision an observed ACL.

The controls use the same retention idea: once either control has an observed
key, `$bucketReady || $controlsIntroduced` remains true even if the Bucket
later becomes not ready.

There is a narrower first-observation boundary. A resource can be emitted in
one reconciliation but not yet appear in the next observed snapshot. If the
prerequisite simultaneously becomes not ready, its observed-key latch is still
false and the template stops emitting that resource. Crossplane garbage
collects observed resources that are absent from final desired state; it cannot
delete that resource from a snapshot in which the resource is itself absent.[6]
This is a liveness/retry concern, not the claimed de-provision of an already
observed resource. Test it during initial creation and with a temporarily
absent composed-resource observation snapshot.

# Complexity boundary (inferred authoring guidance)

For a linear three-stage, four-resource graph, two readiness checks plus two
observed-key latches are moderate and auditable complexity. Keep the pattern
only when a downstream API must not be created until a prerequisite reaches a
specific observed condition.

It becomes high-complexity and fragile when stages branch, duplicate latches
across many resources, or rely on cross-controller convergence. Prefer
provider-native references and ordinary readiness when they express the
dependency. If staging is necessary, use one named gate per stage and state the
retention rule explicitly: once introduced, keep rendering the named resource
unless deletion is intentional.

For a declared or branching creation-introduction graph, prefer
[function-sequencer](../../function-sequencer/sequencing.md): it performs the
same unobserved-successor gating and observed-successor retention without
duplicating latches in the template, and reports blocked stages as XR Events.[7]
It does not provide rollback or a provider-side transaction; use provider
lifecycle capabilities or a separate workflow for those requirements.

# Verification matrix

Render and inspect at least these states:

1. Initial: only the prerequisite resource is emitted.
2. Prerequisite ready: the next stage is first emitted.
3. Partially observed: introduced resources remain in desired state.
4. All prerequisites ready: the final stage is first emitted.
5. Temporarily not ready after introduction: previously introduced resources
   remain in desired state.

Keep `function-auto-ready` after the rendering step. It can mark matched
desired/observed resources ready, but it neither decides whether this template
emits a resource nor overrides an explicit readiness decision.[5]

# Relationships

See [manual readiness](manual-readiness.md) for explicit readiness annotations
and [rendered resources](../rendered-output.md) for resource-name and
status-update behavior.

# Citations

[1] [Resource-name and observed-resource helpers](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103) and [observed lookup](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L141)
[2] [Observed snapshot and ordered function pipeline](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L601-L631)
[3] [Desired-state preservation and deletion on omission](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L698-L709)
[4] [Final desired-state application](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L482-L570)
[5] [function-auto-ready matching](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L102-L119) and [explicit-readiness preservation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[6] [Observed-resource garbage collection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L882-L930)
[7] [function-sequencer gating, retention, and Normal results](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L169-L247) and [Core Event conversion](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L449-L477)
