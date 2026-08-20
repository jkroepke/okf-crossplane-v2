---
type: api
title: Managed resource management policies
description: Beta action gates for external-resource lifecycle operations.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, management-policies, beta]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: beta-maturity-and-provider-support
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L285-L305'
    title: 'Beta maturity and provider support'
  - id: supported-policy-combinations
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/policies.go#L45-L171'
    title: 'Supported policy combinations'
  - id: action-gates-and-observe-only-detection
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/policies.go#L174-L234'
    title: 'Action gates and observe-only detection'
  - id: deletion-gating
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1228-L1306'
    title: 'Deletion gating'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/reconciler/managed/policies.go]
feature_state: Beta
---

# Actions

`spec.managementPolicies` is explicitly **Beta**, enabled by default, and not supported uniformly by every Provider.[^beta-maturity-and-provider-support]

| Action | Permission |
|---|---|
| `Observe` | Inspect external existence and drift |
| `Create` | Create a missing external resource |
| `Update` | Correct external drift |
| `LateInitialize` | Persist eligible provider-assigned values into the MR |
| `Delete` | Delete the external resource when deleting the MR |
| `*` | Full lifecycle control |

The modern resolver validates explicit supported combinations. Each mutating decision accepts either its named action or `*`; an empty enabled list pauses reconciliation, while
`[Observe]` is observe-only.[^supported-policy-combinations][^action-gates-and-observe-only-detection]

# Effects

- Without `Create`, Crossplane does not create a missing external resource. Observing an existing resource still depends on provider identity and import support.
- Without `Update`, drift may be reported but is not corrected.
- Without `LateInitialize`, provider-observed values are not persisted into desired state.
- Without `Delete`, Kubernetes deletion does not call external deletion and the external resource is orphaned when the finalizer can safely be removed.[^deletion-gating]

# Boundaries

The docs' “import settings” wording refers to late initialization in a policy table, not a universal import protocol. External identity and adoption are provider-specific. The deprecated
legacy resolver that mixes `deletionPolicy` and management policies is excluded from this modern v2 contract.

# Relationships

See [Management Policies project history](managed-resource-management-policies-project-history.md)
for GA tracking, known reports, proposals, and selected-release containment.

[^beta-maturity-and-provider-support]: [Beta maturity and provider support](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L285-L305)
[^supported-policy-combinations]: [Supported policy combinations](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/policies.go#L45-L171)
[^action-gates-and-observe-only-detection]: [Action gates and observe-only detection](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/policies.go#L174-L234)
[^deletion-gating]: [Deletion gating](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1228-L1306)
