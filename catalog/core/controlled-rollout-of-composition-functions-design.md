---
type: Crossplane Core Concept
title: Controlled rollout design for Composition Functions
description: Historical accepted design whose proposed Function-revision rollout API is not established as selected-release behavior.
resource: https://github.com/crossplane/crossplane/blob/v2.3.3/design/one-pager-controlled-rollout-of-composition-functions.md
tags: [crossplane, composition-functions, historical-design]
timestamp: 2026-07-15T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 231dd83a48fe7a4b9c06c8c94735c365f3da40b6
source_paths:
  - design/one-pager-controlled-rollout-of-composition-functions.md
selected_core_release: v2.3.3
selected_core_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
design_status: Accepted
---

# Overview

This is **historical design context**, not a record of current behavior. The
document is marked `Accepted`, which shows that its proposal was accepted by
the listed reviewers; it does not show that the proposal was implemented,
released, or remains accurate.[1]

The design explicitly proposes a controlled rollout mechanism for Composition
Functions. It does not itself declare that mechanism current or working.[2]

The selected-release [Composition API](composition.md) and the related
[Composition functions](../functions/composition-functions.md) concept record
the current pipeline behavior separately from this historical proposal.

# Design proposal and selected-release evidence

| Subject | What the design declares | What v2.3.3 source proves |
|---|---|---|
| Active Function revisions | Proposed `activeRevisionLimit` so multiple revisions could serve requests. | The Function schema exposes `revisionActivationPolicy` and `revisionHistoryLimit`; it does not establish `activeRevisionLimit` as a v2.3.3 API.[3] |
| Pipeline revision choice | Proposed `functionRevisionRef` and `functionRevisionSelector` on each pipeline step. | The pipeline schema establishes `functionRef.name`, and the composition controller invokes that name. It does not establish either proposed revision field or revision-selection behavior.[4] |

Accordingly, this catalog does **not** describe controlled Function-revision
rollout as current or working in Crossplane v2.3.3. A claim of current behavior
needs selected-release code, a generated schema, a test, or matching stable
documentation—not an accepted design alone.

# Limitations

The design was pinned from Crossplane `main` for historical context on
2026-07-15. It contains no prominent warning that it is partial, superseded, or
inaccurate, but that absence is not implementation evidence. This bounded
review does not make a roadmap claim or determine whether a later release has
replaced the proposal.

# Citations

[1] [Pinned design title, reviewers, and Accepted status](https://github.com/crossplane/crossplane/blob/231dd83a48fe7a4b9c06c8c94735c365f3da40b6/design/one-pager-controlled-rollout-of-composition-functions.md#L1-L6)

[2] [Pinned design proposal](https://github.com/crossplane/crossplane/blob/231dd83a48fe7a4b9c06c8c94735c365f3da40b6/design/one-pager-controlled-rollout-of-composition-functions.md#L46-L59)

[3] [v2.3.3 Function revision fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L124-L139) and [design's proposed activeRevisionLimit](https://github.com/crossplane/crossplane/blob/231dd83a48fe7a4b9c06c8c94735c365f3da40b6/design/one-pager-controlled-rollout-of-composition-functions.md#L71-L78)

[4] [v2.3.3 pipeline Function reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L144-L152), [v2.3.3 controller invocation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L403-L409), and [design's proposed revision fields](https://github.com/crossplane/crossplane/blob/231dd83a48fe7a4b9c06c8c94735c365f3da40b6/design/one-pager-controlled-rollout-of-composition-functions.md#L117-L123)
