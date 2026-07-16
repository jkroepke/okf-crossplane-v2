---
type: Crossplane Function Input
title: function-sequencer Input
description: Configure v1beta1 sequencing rules, optional CEL conditions, cache behavior, and deletion sequencing.
resource: https://github.com/crossplane-contrib/function-sequencer
tags: [crossplane, composition-function, sequencing, schema]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/function-sequencer
source_tag: v0.6.0
source_commit: 8ee29b46b7b9491fb307cf6caf339541a8d93422
feature_state: Beta
feature_state_basis: The generated Input CRD serves sequencer.fn.crossplane.io/v1beta1.
---

# Schema

The selected package serves `sequencer.fn.crossplane.io/v1beta1` Input. Its
required `rules` describe predecessor-to-successor sequences by
composition-resource name patterns.[1][2]

| Field | Purpose |
| --- | --- |
| `rules` | Required ordered sequence rules. |
| `rules[].sequence` | Resource-name patterns that define the dependency chain. |
| `rules[].condition` | Optional CEL condition for an optional or conditional rule. |
| `rules[].deleteOnly` | Apply the rule only during deletion sequencing. |
| `cacheTTL` | Response-cache TTL; default is one minute and depends on the Alpha runtime cache feature. |
| `enableDeletionSequencing` | Opt in to Usage-based deletion sequencing; default false. |
| `replayDeletion` | Replay deletion sequencing; default true. |
| `usageVersion` | Usage API version; default v2. |
| `resetCompositeReadiness` | Reset composite readiness while successors are withheld; default false. |

# Matching boundary

Rules match composition-resource names, which are normally set by the
resource-name annotation. Patterns without explicit boundaries are strict; use
the documented pattern syntax rather than assuming Kubernetes metadata-name
matching.[3]

# Citations

[1] [Generated Input CRD](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/package/input/sequencer.fn.crossplane.io_inputs.yaml)
[2] [Input types and defaults](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/input/v1beta1/input.go#L16-L79)
[3] [Rule-pattern guidance](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/README.md#L28-L52)
