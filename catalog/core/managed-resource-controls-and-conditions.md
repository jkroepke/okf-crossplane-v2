---
type: reference
title: Managed resource reconciliation controls and conditions
description: Standard pause, poll, reconcile-request, Ready, and Synced signals for provider-agnostic managed-resource operation.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, annotations, conditions]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: pause-and-poll-annotations
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L712-L781'
    title: 'Pause and poll annotations'
  - id: explicit-reconciliation-request
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L783-L824'
    title: 'Explicit reconciliation request'
  - id: runtime-pause-gating
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L965-L979'
    title: 'Runtime pause gating'
  - id: documented-mr-conditions
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L842-L948'
    title: 'Documented MR conditions'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/meta/meta.go, pkg/reconciler/managed/reconciler.go]
feature_state: Not stated by selected sources; managementPolicies discussed separately are Beta
---

# Reconciliation controls

- `crossplane.io/paused: "true"` stops external reconciliation and sets `ReconcilePaused`; removing it resumes. A paused MR cannot finish deletion.
- `crossplane.io/poll-interval` overrides the resource poll interval, subject to the controller minimum. Invalid values fall back.
- Changing `crossplane.io/reconcile-requested-at` requests immediate reconciliation. The handled token is recorded in `status.lastHandledReconcileAt`; reusing it does not retrigger.[^pause-and-poll-annotations][^explicit-reconciliation-request]

An enabled empty management-policy list also pauses reconciliation, independently of the pause annotation.[^runtime-pause-gating]

# Conditions

Standard Ready and Synced conditions communicate availability and reconciliation progress. Documented reasons include `Available`, `Creating`, `Deleting`, `ReconcilePaused`,
`ReconcileError`, `ReconcileSuccess`, `Unavailable`, and `Unknown`; Providers may add their own conditions.[^documented-mr-conditions]

Provider-tool-specific asynchronous condition types are outside this provider-agnostic concept. The documentation's `Unknown` example is not treated as proof of a standard condition type;
it is retained only as a documented reason until separately verified against common condition types.

[^pause-and-poll-annotations]: [Pause and poll annotations](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L712-L781)
[^explicit-reconciliation-request]: [Explicit reconciliation request](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L783-L824)
[^runtime-pause-gating]: [Runtime pause gating](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L965-L979)
[^documented-mr-conditions]: [Documented MR conditions](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L842-L948)
