---
type: concept
title: Managed resource reconciliation lifecycle
description: The stable provider-agnostic observe-first state machine for creating, updating, late-initializing, deleting, and polling external resources.
resource: https://github.com/crossplane/crossplane-runtime
tags: [crossplane, core, managed-resources, reconciliation, lifecycle]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/reconciler/managed/reconciler.go]
feature_state: Stable by repository default
---

# Lifecycle

The modern reconciler follows a provider-agnostic state machine:

1. Stop when paused by annotation or by an enabled empty management-policy set.
2. Record a new explicit reconcile-request token.
3. Resolve references, select ProviderConfig, connect, and observe the external resource.
4. If the MR is deleting, call external deletion only when the resource exists and policy permits; otherwise remove the finalizer when safe.
5. For an active MR, establish the finalizer before creating a missing external resource.
6. Persist provider-reported late initialization only when allowed.
7. Update drift only when allowed, then poll again.[1][2][3][4]

Observation reports whether the external resource exists, whether it is up to date, and whether observation late-initialized the MR. Provider implementations define comparison logic,
external calls, asynchronous behavior, and which fields may be initialized.[5]

# Deletion and orphaning

The finalizer normally keeps the Kubernetes MR until the Provider confirms the external resource is gone. In the modern runtime, omitting `Delete` from management policies prevents the
external delete call and allows finalizer removal when safe, producing orphan-like behavior.[2][6]

The older deletion-policy compatibility resolver is deprecated and excluded. A cluster common spec may still expose `deletionPolicy`, but it is not part of the modern runtime interface.

# Polling and eventual consistency

Up-to-date or update-disallowed resources return success and requeue for polling. Immediately after a successful create, an observation that reports absence is treated as likely eventual
consistency and is requeued instead of creating again.[4][7]

An incomplete-create annotation normally blocks another create to prevent leaks, except when the controller uses deterministic external names and can safely retry the same identity.[8]

# Citations

[1] [Pause and reconcile-request handling](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L965-L1006)
[2] [Observe and deletion branches](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1174-L1306)
[3] [Finalizer and create branch](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1327-L1373)
[4] [Late initialization and update branch](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1473-L1569)
[5] [External observation contract](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L383-L410)
[6] [Documented finalizer deletion lifecycle](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L826-L840)
[7] [Post-create eventual-consistency guard](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1210-L1225)
[8] [Incomplete-create deterministic-name exception](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1100-L1116)
