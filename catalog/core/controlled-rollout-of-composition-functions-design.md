---
type: Crossplane Core Concept
title: Controlled rollout design for Composition Functions
description: Historical accepted design whose proposed Function-revision rollout API is not established as selected-release behavior.
resource: https://github.com/crossplane/crossplane/blob/v2.3.3/design/one-pager-controlled-rollout-of-composition-functions.md
tags: [crossplane, composition-functions, historical-design]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: v2-3-3-design-title-reviewers-and-accepted-status
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L1-L6'
    title: 'v2.3.3 design title, reviewers, and Accepted status'
  - id: v2-3-3-design-proposal
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L46-L59'
    title: 'v2.3.3 design proposal'
  - id: v2-3-3-function-revision-fields
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L124-L139'
    title: 'v2.3.3 Function revision fields'
  - id: design-s-proposed-activerevisionlimit
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L71-L78'
    title: 'design''s proposed activeRevisionLimit'
  - id: v2-3-3-pipeline-function-reference-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L144-L152'
    title: 'v2.3.3 pipeline Function reference schema'
  - id: v2-3-3-controller-invocation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L403-L409'
    title: 'v2.3.3 controller invocation'
  - id: design-s-proposed-revision-fields
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L117-L123'
    title: 'design''s proposed revision fields'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
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
released, or remains accurate.[^v2-3-3-design-title-reviewers-and-accepted-status]

The design explicitly proposes a controlled rollout mechanism for Composition
Functions. It does not itself declare that mechanism current or working.[^v2-3-3-design-proposal]

The selected-release [Composition API](composition.md) and the related
[Composition functions](../functions/composition-functions.md) concept record
the current pipeline behavior separately from this historical proposal.

# Design proposal and selected-release evidence

| Subject | What the design declares | What v2.3.3 source proves |
|---|---|---|
| Active Function revisions | Proposed `activeRevisionLimit` so multiple revisions could serve requests. | The Function schema exposes `revisionActivationPolicy` and `revisionHistoryLimit`; it does not establish `activeRevisionLimit` as a v2.3.3 API.[^v2-3-3-function-revision-fields][^design-s-proposed-activerevisionlimit] |
| Pipeline revision choice | Proposed `functionRevisionRef` and `functionRevisionSelector` on each pipeline step. | The pipeline schema establishes `functionRef.name`, and the composition controller invokes that name. It does not establish either proposed revision field or revision-selection behavior.[^v2-3-3-pipeline-function-reference-schema][^v2-3-3-controller-invocation][^design-s-proposed-revision-fields] |

Accordingly, this catalog does **not** describe controlled Function-revision
rollout as current or working in Crossplane v2.3.3. A claim of current behavior
needs selected-release code, a generated schema, a test, or matching stable
documentation—not an accepted design alone.

# Limitations

The design is pinned to the requested Crossplane `v2.3.3` release. It contains
no prominent warning that it is partial, superseded, or inaccurate, but that
absence is not implementation evidence. This bounded review does not make a
roadmap claim or determine whether a later release has replaced the proposal.

[^v2-3-3-design-title-reviewers-and-accepted-status]: [v2.3.3 design title, reviewers, and Accepted status](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L1-L6)
[^v2-3-3-design-proposal]: [v2.3.3 design proposal](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L46-L59)
[^v2-3-3-function-revision-fields]: [v2.3.3 Function revision fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L124-L139) and [design's proposed activeRevisionLimit](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L71-L78)
[^design-s-proposed-activerevisionlimit]: [design's proposed activeRevisionLimit](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L71-L78)
[^v2-3-3-pipeline-function-reference-schema]: [v2.3.3 pipeline Function reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L144-L152), [v2.3.3 controller invocation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L403-L409), and [design's proposed revision fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L117-L123)
[^v2-3-3-controller-invocation]: [v2.3.3 controller invocation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L403-L409)
[^design-s-proposed-revision-fields]: [design's proposed revision fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/design/one-pager-controlled-rollout-of-composition-functions.md#L117-L123)
