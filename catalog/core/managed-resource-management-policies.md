---
type: api
title: Managed resource management policies
description: Beta action gates for external-resource lifecycle operations, with GA tracking and known limitation reports.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, management-policies, beta]
timestamp: 2026-07-14T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/reconciler/managed/policies.go]
feature_state: Beta
project_history_researched_at: 2026-07-14
---

# Actions

`spec.managementPolicies` is explicitly **Beta**, enabled by default, and not supported uniformly by every Provider.[1]

| Action | Permission |
|---|---|
| `Observe` | Inspect external existence and drift |
| `Create` | Create a missing external resource |
| `Update` | Correct external drift |
| `LateInitialize` | Persist eligible provider-assigned values into the MR |
| `Delete` | Delete the external resource when deleting the MR |
| `*` | Full lifecycle control |

The modern resolver validates explicit supported combinations. Each mutating decision accepts either its named action or `*`; an empty enabled list pauses reconciliation, while
`[Observe]` is observe-only.[2][3]

# Effects

- Without `Create`, Crossplane does not create a missing external resource. Observing an existing resource still depends on provider identity and import support.
- Without `Update`, drift may be reported but is not corrected.
- Without `LateInitialize`, provider-observed values are not persisted into desired state.
- Without `Delete`, Kubernetes deletion does not call external deletion and the external resource is orphaned when the finalizer can safely be removed.[4]

# Boundaries

The docs' “import settings” wording refers to late initialization in a policy table, not a universal import protocol. External identity and adoption are provider-specific. The deprecated
legacy resolver that mixes `deletionPolicy` and management policies is excluded from this modern v2 contract.

# GA tracking and known reports

Crossplane issue #4952 is the open tracker for promoting Management Policies
from Beta to GA. Its checklist still leaves the API-version update and several
linked limitations unchecked. It is a proposal and work tracker, not evidence
that GA is scheduled or released; the selected v2.3 documentation continues to
label the feature Beta.[1][5]

As of the project-history research timestamp, the tracker links these open
user-facing themes:

## Known reports and proposals for the selected release

- **`initProvider` and Upjet reconciliation:** reports cover changes leaking
  from `initProvider` after creation, malformed Terraform `ignore_changes`
  paths for nested lists, update loops when set fields appear in both
  `initProvider` and `forProvider`, and a proposal to remove immutable fields
  from generated `initProvider` schemas. A Crossplane report also describes a
  provider restart losing external identity when `LateInitialize` is omitted.
  These items remain reports or proposals, not general behavior established by
  Crossplane Core.[6][7][8][9][10]
- **Observe-only adoption:** an open proposal would populate required
  `forProvider` fields from observed state when moving an existing resource
  from observe-only toward active management.[11]
- **Policy semantics:** an open runtime proposal discusses stronger
  “must-create” semantics and an orphan shorthand. The current selected-release
  action set remains the one documented above.[2][12]
- **Deletion migration:** an open proposal asks when and how to remove the
  deprecated `deletionPolicy` field while preserving a migration path to
  Management Policies.[13]

## Included in the selected release

One linked request is implemented in the selected release dependency graph:
runtime PR #788 added the `Observe + LateInitialize` and
`Observe + Update + LateInitialize` combinations. Its merge commit is an
ancestor of runtime v2.3.3, which Crossplane v2.3.3 requires.[14][15][16] This resolves
that bounded combination request; it does not complete the GA checklist.

## Release relationship unresolved

Upjet PR #315 implemented generated references and resolvers for
`initProvider`, but Upjet is a provider generator rather than a dependency
whose feature inclusion can be inferred from the Crossplane v2.3.3 commit.
Specific generated Provider releases require separate containment evidence.[17][18]

Bot-authored stale activity was excluded. Open issues are retained only as
reports or proposals, and closed items are not treated as fixed without linked
implementation and selected-release containment.

# Citations

[1] [Beta maturity and provider support](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L285-L305)
[2] [Supported policy combinations](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/policies.go#L45-L171)
[3] [Action gates and observe-only detection](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/policies.go#L174-L234)
[4] [Deletion gating](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1228-L1306)
[5] [Open Management Policies GA tracker](https://github.com/crossplane/crossplane/issues/4952)
[6] [`initProvider` change report: Upjet #298](https://github.com/crossplane/upjet/issues/298)
[7] [Nested-list `ignore_changes` report: Upjet #295](https://github.com/crossplane/upjet/issues/295)
[8] [Set-field update-loop report: Upjet #299](https://github.com/crossplane/upjet/issues/299)
[9] [Immutable `initProvider` field proposal: Upjet #384](https://github.com/crossplane/upjet/issues/384)
[10] [Provider-restart identity report: Crossplane #5918](https://github.com/crossplane/crossplane/issues/5918)
[11] [Observe-only adoption proposal #3999](https://github.com/crossplane/crossplane/issues/3999)
[12] [Runtime policy-semantics proposal #930](https://github.com/crossplane/crossplane-runtime/issues/930)
[13] [`deletionPolicy` migration proposal #5283](https://github.com/crossplane/crossplane/issues/5283)
[14] [Runtime PR #788](https://github.com/crossplane/crossplane-runtime/pull/788)
[15] [PR #788 containment in runtime v2.3.3](https://github.com/crossplane/crossplane-runtime/compare/5faceb9d8a2cf6d839ab193d91a503dd619f8f2c...fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827)
[16] [Crossplane v2.3.3 runtime dependency](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/go.mod#L7-L13)
[17] [Upjet reference request #307](https://github.com/crossplane/upjet/issues/307)
[18] [Merged Upjet PR #315](https://github.com/crossplane/upjet/pull/315)
