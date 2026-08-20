---
type: concept
title: Real-time composition reconciliation
description: Beta composed-resource watches, function TTL requeues, and required-resource refresh boundaries in Crossplane v2.3.3.
resource: https://docs.crossplane.io/v2.3/guides/pods/
tags: [crossplane, core, composition, reconciliation, realtime, beta]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: v2-3-real-time-composition-behavior-and-beta-state
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L141-L175'
    title: 'v2.3 real-time composition behavior and Beta state'
  - id: v2-3-3-real-time-controller-setup
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L565-L583'
    title: 'v2.3.3 real-time controller setup'
  - id: v2-3-3-poll-and-ttl-result-selection
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/reconciler.go#L892-L908'
    title: 'v2.3.3 poll and TTL result selection'
  - id: v2-3-3-dynamic-required-resource-fetching
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L151'
    title: 'v2.3.3 dynamic required-resource fetching'
  - id: v2-3-3-composed-resource-watch-startup
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/reconciler.go#L795-L811'
    title: 'v2.3.3 composed-resource watch startup'
  - id: resource-reference-only-index
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/indexes.go#L34-L59'
    title: 'resource-reference-only index'
  - id: v2-3-3-composed-resource-event-mapper
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/handlers.go#L112-L137'
    title: 'v2.3.3 composed-resource event mapper'
  - id: v2-3-3-shortest-non-zero-pipeline-ttl
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L318-L416'
    title: 'v2.3.3 shortest non-zero pipeline TTL'
  - id: v2-3-xr-poll-and-explicit-reconciliation-controls
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L270-L309'
    title: 'v2.3 XR poll and explicit reconciliation controls'
  - id: v2-3-bootstrap-and-dynamic-required-resource-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L794-L812'
    title: 'v2.3 bootstrap and dynamic required-resource guidance'
  - id: v2-3-watch-circuit-breaker-and-troubleshooting
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/troubleshoot-crossplane.md#L198-L254'
    title: 'v2.3 watch circuit breaker and troubleshooting'
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
delete event to enqueue its XR.[^v2-3-real-time-composition-behavior-and-beta-state][^v2-3-3-real-time-controller-setup]

“Real-time” does not mean that every composition input is watched or that
reconciliation is timer-free. Function response TTLs can still schedule
reconciliation, and function-required resources are fetched during pipeline
execution but are not independently added to the composed-resource watch
index.[^v2-3-3-poll-and-ttl-result-selection][^v2-3-3-dynamic-required-resource-fetching]

# Behavior

## Composed-resource events

With the feature enabled, controller setup indexes each XR's `resourceRefs`,
installs the composed-resource mapper, and sets the normal controller poll
interval to zero.[^v2-3-3-real-time-controller-setup] After a successful composition, Crossplane starts a
deduplicated dynamic watch for every GVK in the XR's current composed-resource
references. Create, update, and delete events are mapped back to XRs by exact
API version, kind, namespace, and name.[^v2-3-3-composed-resource-watch-startup][^resource-reference-only-index][^v2-3-3-composed-resource-event-mapper]

The watch path is resource-reference based. It does not infer dependencies from arbitrary fields inside a composed resource.

## TTL and explicit reconciliation

A positive composition-pipeline TTL causes a jittered requeue even in real-time
mode. The pipeline TTL is the shortest non-zero TTL returned by any function
step; zero means no TTL-driven requeue.[^v2-3-3-poll-and-ttl-result-selection][^v2-3-3-shortest-non-zero-pipeline-ttl] This explains why enabling
real-time composition can coexist with periodic work.

Changing an XR's `crossplane.io/reconcile-requested-at` annotation requests
immediate reconciliation. The v2.3 documentation also describes a per-XR
poll-interval annotation, but in real-time controller setup the ordinary poll
interval is zero and a positive function TTL has its own requeue path.[^v2-3-3-poll-and-ttl-result-selection][^v2-3-xr-poll-and-explicit-reconciliation-controls]

## Required-resource refresh boundary

Composition-declared bootstrap requirements are fetched before a function runs.
A function may also request resources dynamically; Crossplane fetches them and
reruns the function until requirements stabilize, with a five-iteration
limit.[^v2-3-3-dynamic-required-resource-fetching][^v2-3-bootstrap-and-dynamic-required-resource-guidance]

In v2.3.3, required-resource fetches populate the function request but not the
XR `resourceRefs` watch index. A change to a required resource therefore does
not independently enqueue the XR unless that object is also a composed
resource. It becomes visible when another event, an explicit request, a TTL
requeue, or a broader controller resync causes the pipeline to run again.[^v2-3-3-dynamic-required-resource-fetching][^v2-3-3-composed-resource-watch-startup][^resource-reference-only-index]

# Operational safeguards

Crossplane's XR circuit breaker monitors watch-event reconciliation rates. The
v2.3 defaults allow a burst of 100 events, refill at one event per second, cool
down for five minutes, and admit a probe every 30 seconds while open. An
affected XR reports `Responsive=False` with reason `WatchCircuitOpen`.[^v2-3-watch-circuit-breaker-and-troubleshooting]

This safeguard limits feedback-loop impact; it does not identify the event
producer or remove periodic TTL work. Crossplane documentation recommends
investigating composition feedback loops, controllers fighting over fields,
and frequently changing connection details.[^v2-3-watch-circuit-breaker-and-troubleshooting]

# Limitations

- Real-time composition watches composed resources referenced by an XR, not every resource read by a function.
- A watch event indicates that Kubernetes delivered an object event; it does not prove a meaningful spec or status change.
- Server-side apply sends desired composed-resource state on reconciliation. The selected sources do not establish a general no-op suppression guarantee.
- Claims, deprecated XRD v1, legacy v1 XR semantics, and legacy provider-kubernetes `Object` behavior as current guidance are excluded.

# Relationships

This capability drives the event path for [Composition](composition.md).
Function pipelines and their TTL contract are described under
[composition functions](../functions/composition-functions.md).
Provider-managed polling and explicit requests remain separate
[managed-resource reconciliation controls](managed-resource-controls-and-conditions.md).
See [project history](realtime-composition-project-history.md) for selected-release
reports, a contained runtime fix, and the post-release GA proposal.

[^v2-3-real-time-composition-behavior-and-beta-state]: [v2.3 real-time composition behavior and Beta state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L141-L175)
[^v2-3-3-real-time-controller-setup]: [v2.3.3 real-time controller setup](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/reconciler.go#L565-L583)
[^v2-3-3-poll-and-ttl-result-selection]: [v2.3.3 poll and TTL result selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/reconciler.go#L892-L908)
[^v2-3-3-dynamic-required-resource-fetching]: [v2.3.3 dynamic required-resource fetching](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L151)
[^v2-3-3-composed-resource-watch-startup]: [v2.3.3 composed-resource watch startup](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/reconciler.go#L795-L811) and [resource-reference-only index](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/indexes.go#L34-L59)
[^resource-reference-only-index]: [resource-reference-only index](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/indexes.go#L34-L59)
[^v2-3-3-composed-resource-event-mapper]: [v2.3.3 composed-resource event mapper](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/definition/handlers.go#L112-L137)
[^v2-3-3-shortest-non-zero-pipeline-ttl]: [v2.3.3 shortest non-zero pipeline TTL](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L318-L416)
[^v2-3-xr-poll-and-explicit-reconciliation-controls]: [v2.3 XR poll and explicit reconciliation controls](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L270-L309)
[^v2-3-bootstrap-and-dynamic-required-resource-guidance]: [v2.3 bootstrap and dynamic required-resource guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L794-L812)
[^v2-3-watch-circuit-breaker-and-troubleshooting]: [v2.3 watch circuit breaker and troubleshooting](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/troubleshoot-crossplane.md#L198-L254)
