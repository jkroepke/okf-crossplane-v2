---
type: reference
title: Managed resource reconciliation controls and conditions
description: Standard pause, poll, reconcile-request, Ready, and Synced signals for provider-agnostic managed-resource operation.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, annotations, conditions]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/meta/meta.go, pkg/reconciler/managed/reconciler.go]
feature_state: Stable by repository default
---

# Reconciliation controls

- `crossplane.io/paused: "true"` stops external reconciliation and sets `ReconcilePaused`; removing it resumes. A paused MR cannot finish deletion.
- `crossplane.io/poll-interval` overrides the resource poll interval, subject to the controller minimum. Invalid values fall back.
- Changing `crossplane.io/reconcile-requested-at` requests immediate reconciliation. The handled token is recorded in `status.lastHandledReconcileAt`; reusing it does not retrigger.[1][2]

An enabled empty management-policy list also pauses reconciliation, independently of the pause annotation.[3]

# Conditions

Standard Ready and Synced conditions communicate availability and reconciliation progress. Documented reasons include `Available`, `Creating`, `Deleting`, `ReconcilePaused`,
`ReconcileError`, `ReconcileSuccess`, `Unavailable`, and `Unknown`; Providers may add their own conditions.[4]

Provider-tool-specific asynchronous condition types are outside this provider-agnostic concept. The documentation's `Unknown` example is not treated as proof of a standard condition type;
it is retained only as a documented reason until separately verified against common condition types.

# Citations

[1] [Pause and poll annotations](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L712-L781)
[2] [Explicit reconciliation request](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L783-L824)
[3] [Runtime pause gating](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L965-L979)
[4] [Documented MR conditions](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L842-L948)
