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
source_paths: [fn.go, README.md]
supporting_sources:
  - repository: crossplane/crossplane
    commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
    paths: [internal/controller/apiextensions/composite/composition_functions.go]
  - repository: crossplane/docs
    commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
    paths: [content/v2.3/composition/compositions.md]
  - repository: crossplane-contrib/function-auto-ready
    commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
    paths: [fn.go]
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
later becomes unready.[1]

# Pipeline order and minimal Input

Run the resource-producing function first, then a readiness-producing step,
then sequencer:

```text
resource-producing function (including any manual readiness annotation)
  -> optional function-auto-ready
  -> function-sequencer
```

# Events and readiness

When a rule blocks a successor or a rule condition is false, the function
returns actionable Normal results.[1] Crossplane converts these nonfatal
function results into Kubernetes Events; the ordinary target is the composite
resource, so the stage wait is visible on the XR.[2]

Sequencer then determines whether an unobserved successor remains in the
desired set. Set
`resetCompositeReadiness: true` only when the XR must not report ready while
sequencer has withheld a successor.[3]

# Limitations

- Rules use composition-resource names, not `metadata.name`.[1]
- A missing required predecessor pattern blocks a successor; optional branches
  need a rule condition rather than an unconditional predecessor rule.[4]
- Creation sequencing and optional deletion sequencing are separate. Deletion
  sequencing uses v2 Usage or ClusterUsage relationships and has its own
  scope and foreground-deletion requirements.[5] Composition Functions do not
  run during XR deletion, so deletion relationships must already exist before
  deletion begins.[6]

# Relationships

For the Core deletion-protection contract, see
[Usage and ClusterUsage](../../core/usages-and-clusterusages.md).
The [Input reference](input.md) documents defaults, CEL conditions, cache TTL,
and the mixed-scope deletion-sequencing guard.

# Citations

[1] [Creation sequencing, observed-successor retention, and Normal results](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L169-L247)
[2] [Crossplane Function-result Event conversion and target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L449-L477) and [default composite target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L961-L967)
[3] [README pipeline order and composite readiness option](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L54-L91)
[4] [Rule conditions and missing predecessor behavior](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L196-L250)
[5] [Deletion sequencing and v2 Usage handling](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L93-L153)
[6] [Function pipelines do not run during XR deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L143-L148)
