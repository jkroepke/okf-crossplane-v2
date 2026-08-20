---
type: Crossplane Function
title: Sequence composed-resource introduction
description: Gate successor desired resources on predecessor readiness, retain observed successors, and report blocked stages as XR Events.
resource: https://github.com/crossplane-contrib/function-sequencer
tags: [crossplane, composition-function, sequencing, readiness, events]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: creation-sequencing-observed-successor-retention-and-normal-results
    resource: 'https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L169-L247'
    title: 'Creation sequencing, observed-successor retention, and Normal results'
  - id: crossplane-function-result-event-conversion-and-target
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L449-L477'
    title: 'Crossplane Function-result Event conversion and target'
  - id: default-composite-target
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L961-L967'
    title: 'default composite target'
  - id: readme-pipeline-order-and-composite-readiness-option
    resource: 'https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L54-L91'
    title: 'README pipeline order and composite readiness option'
  - id: rule-conditions-and-missing-predecessor-behavior
    resource: 'https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L196-L250'
    title: 'Rule conditions and missing predecessor behavior'
  - id: deletion-sequencing-and-v2-usage-handling
    resource: 'https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L93-L153'
    title: 'Deletion sequencing and v2 Usage handling'
  - id: function-pipelines-do-not-run-during-xr-deletion
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L143-L148'
    title: 'Function pipelines do not run during XR deletion'
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
from desired state.[^creation-sequencing-observed-successor-retention-and-normal-results]

Once a successor is observed, sequencer preserves it even if a predecessor
later becomes unready.[^creation-sequencing-observed-successor-retention-and-normal-results]

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
returns actionable Normal results.[^creation-sequencing-observed-successor-retention-and-normal-results] Crossplane converts these nonfatal
function results into Kubernetes Events; the ordinary target is the composite
resource, so the stage wait is visible on the XR.[^crossplane-function-result-event-conversion-and-target][^default-composite-target]

Sequencer then determines whether an unobserved successor remains in the
desired set. Set
`resetCompositeReadiness: true` only when the XR must not report ready while
sequencer has withheld a successor.[^readme-pipeline-order-and-composite-readiness-option]

# Limitations

- Rules use composition-resource names, not `metadata.name`.[^creation-sequencing-observed-successor-retention-and-normal-results]
- A missing required predecessor pattern blocks a successor; optional branches
  need a rule condition rather than an unconditional predecessor rule.[^rule-conditions-and-missing-predecessor-behavior]
- Creation sequencing and optional deletion sequencing are separate. Deletion
  sequencing uses v2 Usage or ClusterUsage relationships and has its own
  scope and foreground-deletion requirements.[^deletion-sequencing-and-v2-usage-handling] Composition Functions do not
  run during XR deletion, so deletion relationships must already exist before
  deletion begins.[^function-pipelines-do-not-run-during-xr-deletion]

# Relationships

For the Core deletion-protection contract, see
[Usage and ClusterUsage](../../core/usages-and-clusterusages.md).
The [Input reference](input.md) documents defaults, CEL conditions, cache TTL,
and the mixed-scope deletion-sequencing guard.

[^creation-sequencing-observed-successor-retention-and-normal-results]: [Creation sequencing, observed-successor retention, and Normal results](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L169-L247)
[^crossplane-function-result-event-conversion-and-target]: [Crossplane Function-result Event conversion and target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L449-L477) and [default composite target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L961-L967)
[^default-composite-target]: [default composite target](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L961-L967)
[^readme-pipeline-order-and-composite-readiness-option]: [README pipeline order and composite readiness option](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L54-L91)
[^rule-conditions-and-missing-predecessor-behavior]: [Rule conditions and missing predecessor behavior](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L196-L250)
[^deletion-sequencing-and-v2-usage-handling]: [Deletion sequencing and v2 Usage handling](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L93-L153)
[^function-pipelines-do-not-run-during-xr-deletion]: [Function pipelines do not run during XR deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L143-L148)
