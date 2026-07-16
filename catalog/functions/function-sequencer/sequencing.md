---
type: Crossplane Function
title: Sequence composed-resource introduction
description: Gate successor desired resources on predecessor readiness, retain observed successors, and report blocked stages as XR Events.
resource: https://github.com/crossplane-contrib/function-sequencer
tags: [crossplane, composition-function, sequencing, readiness, events]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/function-sequencer
source_tag: v0.6.0
source_commit: 8ee29b46b7b9491fb307cf6caf339541a8d93422
feature_state: Beta
feature_state_basis: The selected Input API is served as sequencer.fn.crossplane.io/v1beta1.
---

# Overview

`function-sequencer` runs after a resource-producing Composition Function and
filters the desired-resource map according to rules over composition-resource
names. For an unobserved successor, every matched predecessor must be
`Ready=True` in accumulated desired state; otherwise the successor is removed
from desired state.[1]

Once a successor is observed, sequencer preserves it even if a predecessor
later becomes unready.[1] This supplies the observed-key retention that a
Go-template staged-introduction pattern otherwise implements manually.

# Bucket-stage mapping

For a Bucket, ownership controls, public-access block, and ACL, first render
all four resources with stable composition-resource names, then use rules that
express:

1. `bucket` precedes `ownership-controls`.
2. `bucket` precedes `public-access-block`.
3. `ownership-controls` precedes `public-acl`.
4. `public-access-block` precedes `public-acl`.

This is sequencing of **desired-resource introduction**, not a provider-side
transaction or a promise that Kubernetes applies the resource manifests in a
particular order. As inferred authoring guidance, it is a better fit than
manual template latches when the dependency graph is more than a small
exceptional case.

# Events and readiness

When a rule blocks a successor or a rule condition is false, the function
returns actionable Normal results.[1] Crossplane converts these nonfatal
function results into Kubernetes Events; the ordinary target is the composite
resource, so the stage wait is visible on the XR.[2]

Place `function-auto-ready` before sequencer when both are used. Auto-ready can
derive predecessor readiness from matched observation; a prior manual
readiness annotation can instead set it explicitly. Sequencer then determines
whether an unobserved successor remains in the desired set. Set
`resetCompositeReadiness: true` only when the XR must not report ready while
sequencer has withheld a successor.[3]

# Limitations

- Rules use composition-resource names, not `metadata.name`.[1]
- A missing required predecessor pattern blocks a successor; optional branches
  need a rule condition rather than an unconditional predecessor rule.[4]
- Creation sequencing and optional deletion sequencing are separate. Deletion
  sequencing uses v2 Usage or ClusterUsage relationships and has its own
  scope and foreground-deletion requirements.[5]
- Sequencer filters desired state; it cannot reverse an external action already
  taken by a provider.

# Relationships

For a small, custom condition or non-composed observed state, retain a
[manual readiness](../function-go-templating/patterns/manual-readiness.md)
override. For the lower-level template-latch alternative, see
[readiness-gated staging](../function-go-templating/patterns/readiness-gated-staging.md).

# Citations

[1] [Creation sequencing, observed-successor retention, and Normal results](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L169-L247)
[2] [Crossplane Function-result Event conversion and target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L449-L477) and [default composite target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L961-L967)
[3] [README pipeline order and composite readiness option](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L54-L91)
[4] [Rule conditions and missing predecessor behavior](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L196-L250)
[5] [Deletion sequencing and v2 Usage handling](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L93-L153)
