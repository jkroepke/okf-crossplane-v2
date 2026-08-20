---
type: concept
title: Managed resource reconciliation lifecycle
description: The provider-agnostic observe-first state machine for creating, updating, late-initializing, deleting, and polling external resources.
resource: https://github.com/crossplane/crossplane-runtime
tags: [crossplane, core, managed-resources, reconciliation, lifecycle]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: pause-and-reconcile-request-handling
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L965-L1006'
    title: 'Pause and reconcile-request handling'
  - id: observe-and-deletion-branches
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1174-L1306'
    title: 'Observe and deletion branches'
  - id: finalizer-and-create-branch
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1327-L1373'
    title: 'Finalizer and create branch'
  - id: late-initialization-and-update-branch
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1473-L1569'
    title: 'Late initialization and update branch'
  - id: external-observation-contract
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L383-L410'
    title: 'External observation contract'
  - id: documented-finalizer-deletion-lifecycle
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L826-L840'
    title: 'Documented finalizer deletion lifecycle'
  - id: post-create-eventual-consistency-guard
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1210-L1225'
    title: 'Post-create eventual-consistency guard'
  - id: incomplete-create-deterministic-name-exception
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1100-L1116'
    title: 'Incomplete-create deterministic-name exception'
crossplane_release: v2.3.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/reconciler/managed/reconciler.go]
feature_state: Not stated by selected sources
---

# Lifecycle

The modern reconciler follows a provider-agnostic state machine:

1. Stop when paused by annotation or by an enabled empty management-policy set.
2. Record a new explicit reconcile-request token.
3. Resolve references, select ProviderConfig, connect, and observe the external resource.
4. If the MR is deleting, call external deletion only when the resource exists and policy permits; otherwise remove the finalizer when safe.
5. For an active MR, establish the finalizer before creating a missing external resource.
6. Persist provider-reported late initialization only when allowed.
7. Update drift only when allowed, then poll again.[^pause-and-reconcile-request-handling][^observe-and-deletion-branches][^finalizer-and-create-branch][^late-initialization-and-update-branch]

Observation reports whether the external resource exists, whether it is up to date, and whether observation late-initialized the MR. Provider implementations define comparison logic,
external calls, asynchronous behavior, and which fields may be initialized.[^external-observation-contract]

# Deletion and orphaning

The finalizer normally keeps the Kubernetes MR until the Provider confirms the external resource is gone. In the modern runtime, omitting `Delete` from management policies prevents the
external delete call and allows finalizer removal when safe, producing orphan-like behavior.[^observe-and-deletion-branches][^documented-finalizer-deletion-lifecycle]

The older deletion-policy compatibility resolver is deprecated and excluded. A cluster common spec may still expose `deletionPolicy`, but it is not part of the modern runtime interface.

# Polling and eventual consistency

Up-to-date or update-disallowed resources return success and requeue for polling. Immediately after a successful create, an observation that reports absence is treated as likely eventual
consistency and is requeued instead of creating again.[^late-initialization-and-update-branch][^post-create-eventual-consistency-guard]

An incomplete-create annotation normally blocks another create to prevent leaks, except when the controller uses deterministic external names and can safely retry the same identity.[^incomplete-create-deterministic-name-exception]

[^pause-and-reconcile-request-handling]: [Pause and reconcile-request handling](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L965-L1006)
[^observe-and-deletion-branches]: [Observe and deletion branches](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1174-L1306)
[^finalizer-and-create-branch]: [Finalizer and create branch](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1327-L1373)
[^late-initialization-and-update-branch]: [Late initialization and update branch](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1473-L1569)
[^external-observation-contract]: [External observation contract](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L383-L410)
[^documented-finalizer-deletion-lifecycle]: [Documented finalizer deletion lifecycle](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L826-L840)
[^post-create-eventual-consistency-guard]: [Post-create eventual-consistency guard](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1210-L1225)
[^incomplete-create-deterministic-name-exception]: [Incomplete-create deterministic-name exception](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1100-L1116)
