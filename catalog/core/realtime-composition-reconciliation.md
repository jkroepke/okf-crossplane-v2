---
type: concept
title: Real-time composition reconciliation
description: Beta composed-resource watches, function TTL requeues, required-resource refresh boundaries, and related reconciliation-churn reports in Crossplane v2.3.3.
resource: https://docs.crossplane.io/v2.3/guides/pods/
tags: [crossplane, core, composition, reconciliation, realtime, beta]
timestamp: 2026-07-14T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - internal/controller/apiextensions/definition/reconciler.go
  - internal/controller/apiextensions/definition/handlers.go
  - internal/controller/apiextensions/definition/indexes.go
  - internal/controller/apiextensions/composite/reconciler.go
  - internal/controller/apiextensions/composite/composition_functions.go
  - internal/xfn/required_resources.go
feature_state: Beta
---

# Overview

Crossplane v2.3.3 real-time compositions are **Beta** and enabled by default.
They replace the normal composition poll interval with Kubernetes watches for
composed resources, allowing a referenced composed-resource create, update, or
delete event to enqueue its XR.[1][2]

“Real-time” does not mean that every composition input is watched or that
reconciliation is timer-free. Function response TTLs can still schedule
reconciliation, and function-required resources are fetched during pipeline
execution but are not independently added to the composed-resource watch
index.[3][4]

# Behavior

## Composed-resource events

With the feature enabled, controller setup indexes each XR's `resourceRefs`,
installs the composed-resource mapper, and sets the normal controller poll
interval to zero.[2] After a successful composition, Crossplane starts a
deduplicated dynamic watch for every GVK in the XR's current composed-resource
references. Create, update, and delete events are mapped back to XRs by exact
API version, kind, namespace, and name.[5][6]

The watch path is resource-reference based. It does not infer dependencies from arbitrary fields inside a composed resource.

## TTL and explicit reconciliation

A positive composition-pipeline TTL causes a jittered requeue even in real-time
mode. The pipeline TTL is the shortest non-zero TTL returned by any function
step; zero means no TTL-driven requeue.[3][7] This explains why enabling
real-time composition can coexist with periodic work.

Changing an XR's `crossplane.io/reconcile-requested-at` annotation requests
immediate reconciliation. The v2.3 documentation also describes a per-XR
poll-interval annotation, but in real-time controller setup the ordinary poll
interval is zero and a positive function TTL has its own requeue path.[3][8]

## Required-resource refresh boundary

Composition-declared bootstrap requirements are fetched before a function runs.
A function may also request resources dynamically; Crossplane fetches them and
reruns the function until requirements stabilize, with a five-iteration
limit.[4][9]

In v2.3.3, required-resource fetches populate the function request but not the
XR `resourceRefs` watch index. A change to a required resource therefore does
not independently enqueue the XR unless that object is also a composed
resource. It becomes visible when another event, an explicit request, a TTL
requeue, or a broader controller resync causes the pipeline to run again.[4][5]

# Operational safeguards

Crossplane's XR circuit breaker monitors watch-event reconciliation rates. The
v2.3 defaults allow a burst of 100 events, refill at one event per second, cool
down for five minutes, and admit a probe every 30 seconds while open. An
affected XR reports `Responsive=False` with reason `WatchCircuitOpen`.[10]

This safeguard limits feedback-loop impact; it does not identify the event
producer or remove periodic TTL work. Crossplane documentation recommends
investigating composition feedback loops, controllers fighting over fields,
and frequently changing connection details.[10]

# Project history

Research timestamp: **2026-07-14**. The following are human-authored reports or proposals. Bot and app activity was excluded, and issue closure alone is not treated as proof of a released fix.

## Known reports for the selected release model

- **crossplane/crossplane #6898 (open):** reports repeated no-op
  composed-resource patches and high API/audit traffic. Maintainer analysis
  distinguishes XR changes, CompositionRevision changes, composed-resource
  watch events, periodic reconciliation without real-time mode, and informer
  resync. Later reports identify short function TTLs and unwatched external
  inputs as additional churn and freshness tradeoffs. No released fix is
  established.[11]
- **crossplane/crossplane #6824 (closed by stale automation, not fixed):**
  reports increased CPU and audit traffic after the feature became
  default-enabled Beta. Maintainers point to field fights or flapping and the
  XR circuit breaker as areas to inspect. The report was not closed by a
  verified fix.[12]
- **crossplane/crossplane #7024 (reporter-closed):** reports a high-CPU loop
  associated with an empty metadata label; the reporter says assigning a value
  stopped the reproduction. This is an environment-specific outcome, not
  evidence of a released Core fix.[13]
- **provider-kubernetes #421 (open):** reports no-change `Object` status and
  apply events feeding a reconciliation cycle. The reporter says it persisted
  with real-time compositions disabled and later narrowed the reproduction to
  legacy `v1alpha1 Object`, not `v1alpha2`. It is retained as a version-bounded
  report, not current API guidance.[14]

## Included in selected release

- **crossplane-runtime #902 / PR #906:** issue #902 reported that a
  provider-supplied `Synced` condition without `observedGeneration` compared
  unequal on every poll, changing transition time and producing watch events.
  PR #906 defensively ignores generation when either side is zero; its merge
  commit is contained in crossplane-runtime v2.3.3. The released equality
  behavior is also present in selected Crossplane v2.3.3 source. The
  provider-kubernetes #421 reporter explicitly considered that issue a
  different cause.[15][16]

## Post-release proposal or development

- **crossplane/crossplane #6453 (open):** tracks promotion of real-time
  compositions from Beta to GA and proposes removing the disable switch only
  after implementation bugs are addressed. It does not establish GA maturity
  or a committed release.[17]

# Limitations

- Real-time composition watches composed resources referenced by an XR, not every resource read by a function.
- A watch event indicates that Kubernetes delivered an object event; it does not prove a meaningful spec or status change.
- Server-side apply sends desired composed-resource state on reconciliation. The selected sources do not establish a general no-op suppression guarantee.
- The linked issues have distinct or unresolved causes. They do not establish that real-time composition alone causes every reported loop.
- Claims, deprecated XRD v1, legacy v1 XR semantics, and legacy provider-kubernetes `Object` behavior as current guidance are excluded.

# Relationships

This capability drives the event path for [Composition](composition.md).
Function pipelines and their TTL contract are described under
[composition functions](../functions/composition-functions.md).
Provider-managed polling and explicit requests remain separate
[managed-resource reconciliation controls](managed-resource-controls-and-conditions.md).

# Citations

[1] [v2.3 real-time composition behavior and Beta state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L141-L175)
[2] [v2.3.3 real-time controller setup](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L565-L583)
[3] [v2.3.3 poll and TTL result selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/reconciler.go#L892-L908)
[4] [v2.3.3 dynamic required-resource fetching](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L151)
[5] [v2.3.3 composed-resource watch startup](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/reconciler.go#L795-L811)
and [resource-reference-only index](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/indexes.go#L34-L59)
[6] [v2.3.3 composed-resource event mapper](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/handlers.go#L112-L137)
[7] [v2.3.3 shortest non-zero pipeline TTL](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L318-L416)
[8] [v2.3 XR poll and explicit reconciliation controls](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L270-L309)
[9] [v2.3 bootstrap and dynamic required-resource guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L794-L812)
[10] [v2.3 watch circuit breaker and troubleshooting](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/troubleshoot-crossplane.md#L198-L254)
[11] [Issue #6898](https://github.com/crossplane/crossplane/issues/6898) and [maintainer trigger analysis](https://github.com/crossplane/crossplane/issues/6898#issuecomment-3518376485)
[12] [Issue #6824](https://github.com/crossplane/crossplane/issues/6824)
[13] [Issue #7024](https://github.com/crossplane/crossplane/issues/7024) and [reporter outcome](https://github.com/crossplane/crossplane/issues/7024#issuecomment-3793358748)
[14] [provider-kubernetes issue #421](https://github.com/crossplane-contrib/provider-kubernetes/issues/421) and [reported version boundary](https://github.com/crossplane-contrib/provider-kubernetes/issues/421#issuecomment-3894626461)
[15] [crossplane-runtime issue #902](https://github.com/crossplane/crossplane-runtime/issues/902) and [maintainer analysis](https://github.com/crossplane/crossplane-runtime/issues/902#issuecomment-3792053064)
[16] [Released defensive condition equality in Crossplane v2.3.3](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/condition.go#L105-L124)
and [PR #906 merge containment in runtime v2.3.3](https://github.com/crossplane/crossplane-runtime/compare/311ca76bbd30f86e196438771062091a39e39e0d...fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827)
[17] [GA promotion proposal #6453](https://github.com/crossplane/crossplane/issues/6453)
