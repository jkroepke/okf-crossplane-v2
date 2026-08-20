---
type: concept
title: Usage and ClusterUsage deletion protection
description: Beta Core APIs that block deletion of used resources and model deletion ordering across supported Kubernetes scopes.
resource: https://docs.crossplane.io/v2.3/managed-resources/usages/
tags: [crossplane, core, usage, deletion-protection, beta]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: official-purposes-and-terminology
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L10-L19'
    title: 'Official purposes and terminology'
  - id: beta-maturity-and-feature-flag
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L21-L30'
    title: 'Beta maturity and feature flag'
  - id: usage-crd-scope-and-served-version
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/protection.crossplane.io_usages.yaml#L7-L29'
    title: 'Usage CRD scope and served version'
  - id: clusterusage-crd-scope-and-served-version
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/protection.crossplane.io_clusterusages.yaml#L7-L29'
    title: 'ClusterUsage CRD scope and served version'
  - id: usage-endpoint-types-and-validation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/usage_types.go#L25-L140'
    title: 'Usage endpoint types and validation'
  - id: clusterusage-endpoint-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/clusterusage_types.go#L25-L67'
    title: 'ClusterUsage endpoint schema'
  - id: reconciled-label-ownership-and-availability
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L475-L545'
    title: 'Reconciled label, ownership, and availability'
  - id: deletion-webhook-configuration
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/webhookconfigurations/usage.yaml#L5-L31'
    title: 'Deletion webhook configuration'
  - id: deletion-denial-behavior
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/webhook/protection/usage/handler.go#L93-L157'
    title: 'Deletion denial behavior'
  - id: cleanup-and-deletion-replay
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L359-L429'
    title: 'Cleanup and deletion replay'
  - id: replay-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L186-L220'
    title: 'Replay guidance'
  - id: namespaced-and-cross-namespace-relationships
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L242-L271'
    title: 'Namespaced and cross-namespace relationships'
  - id: clusterusage-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L273-L291'
    title: 'ClusterUsage guidance'
  - id: open-cross-scope-enhancement-report-7123
    resource: 'https://github.com/crossplane/crossplane/issues/7123'
    title: 'Open cross-scope enhancement report #7123'
  - id: released-namespace-sensitive-finder
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/protection/usage/finder.go#L72-L133'
    title: 'Released namespace-sensitive finder'
  - id: composition-selector-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L222-L240'
    title: 'Composition selector guidance'
  - id: one-time-selector-resolution
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L148-L159'
    title: 'One-time selector resolution'
  - id: pr-6345-scope-discussion
    resource: 'https://github.com/crossplane/crossplane/pull/6345'
    title: 'PR #6345 scope discussion'
  - id: diverged-pr-merge-and-v2-3-3-commits
    resource: 'https://github.com/crossplane/crossplane/compare/b90c89203554e2a4a0d5af0eecd72846a4b48c6d...09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d'
    title: 'Diverged PR merge and v2.3.3 commits'
  - id: function-sequencer-report-114
    resource: 'https://github.com/crossplane-contrib/function-sequencer/issues/114'
    title: 'function-sequencer report #114'
  - id: open-ga-promotion-tracker-6336
    resource: 'https://github.com/crossplane/crossplane/issues/6336'
    title: 'Open GA promotion tracker #6336'
  - id: function-sequencer-v0-6-0-usage-generation
    resource: 'https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L310-L387'
    title: 'function-sequencer v0.6.0 Usage generation'
  - id: function-pipelines-do-not-run-during-xr-deletion
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L143-L148'
    title: 'Function pipelines do not run during XR deletion'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/protection.crossplane.io_usages.yaml
  - cluster/crds/protection.crossplane.io_clusterusages.yaml
  - apis/protection/v1beta1/usage_types.go
  - apis/protection/v1beta1/clusterusage_types.go
  - internal/controller/protection/usage/reconciler.go
  - internal/protection/usage/finder.go
  - internal/webhook/protection/usage/handler.go
documentation_repository: crossplane/docs
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths:
  - content/v2.3/managed-resources/usages.md
  - content/v2.3/composition/compositions.md
supporting_source_repository: crossplane-contrib/function-sequencer
supporting_source_commit: 8ee29b46b7b9491fb307cf6caf339541a8d93422
supporting_source_paths: [fn.go]
feature_state: Beta
---

# Overview

`Usage` and `ClusterUsage` describe a relationship in which a resource identified by `spec.by` uses the resource identified by `spec.of`.
Crossplane blocks deletion of the `of` resource while the relationship exists. This supports accidental-deletion protection and deletion ordering:
a dependent can be deleted before the resource it needs.[^official-purposes-and-terminology]

The APIs do not schedule creation or wait for the `of` resource to become ready. Their ordering guarantee is limited to deletion protection.
This differs from [function-sequencer creation gating](../functions/function-sequencer/sequencing.md),
which filters unobserved desired successors. When sequencer also generates
deletion relationships, those Usage objects must already exist because
Composition Functions do not run during XR deletion.[^function-pipelines-do-not-run-during-xr-deletion]

Both APIs are **Beta**, served and stored as `protection.crossplane.io/v1beta1`. Usages are enabled by default and can be disabled with `--enable-usages=false`.[^beta-maturity-and-feature-flag][^usage-crd-scope-and-served-version][^clusterusage-crd-scope-and-served-version]

# Schema

| Field | Purpose |
|---|---|
| `spec.of` | Required identity of the protected or used resource. |
| `spec.by` | Optional identity of the using or dependent resource. |
| `spec.reason` | Optional human-readable reason for protection when no dependent resource is needed. |
| `spec.replayDeletion` | Replays a previously blocked deletion after the Usage is removed. Defaults to `false`. |

At least one of `spec.by` or `spec.reason` is required. Each present `of` or `by` endpoint uses either `resourceRef` or `resourceSelector`;
a reference takes precedence if both are supplied. Selector resolution persists the chosen name into the reference and does not continuously retarget the Usage.[^usage-endpoint-types-and-validation][^one-time-selector-resolution]

# Behavior

After resolving the endpoints, the controller:

1. adds `crossplane.io/in-use: "true"` to the `of` resource;
2. adds the `by` resource as an owner of the Usage when present;
3. reports the Usage as available and periodically rechecks it.[^reconciled-label-ownership-and-availability]

A fail-closed validating webhook intercepts deletion of labelled resources. It finds matching Usages, records the attempted propagation policy, and denies deletion with HTTP 409 Conflict while at least one Usage remains.[^deletion-webhook-configuration][^deletion-denial-behavior]

When a Usage is deleted, Crossplane removes the in-use label only after the last protecting Usage is gone. With `replayDeletion: true`, it retries an earlier blocked deletion
using the recorded propagation policy.[^cleanup-and-deletion-replay] Official guidance recommends replay for composed-resource deletion ordering because it avoids waiting for a later deletion retry.[^replay-guidance]

# Scope model

`Usage` is namespaced. `ClusterUsage` is cluster-scoped.[^usage-crd-scope-and-served-version][^clusterusage-crd-scope-and-served-version]

| `by` endpoint | `of` endpoint | Model and boundary |
|---|---|---|
| Namespaced | Same namespace | A `Usage` in that namespace is the normal model. |
| Namespaced | Different namespace | `Usage` supports an explicit namespace only on `of`; `by` must be present and remains in the Usage namespace.[^namespaced-and-cross-namespace-relationships] |
| Cluster-scoped | Cluster-scoped | `ClusterUsage` is the documented model.[^clusterusage-guidance] |
| Namespaced | Cluster-scoped | The `Usage` type can express this shape, but released v2.3.3 deletion lookup is silently ineffective; do not rely on it.[^open-cross-scope-enhancement-report-7123][^released-namespace-sensitive-finder] |
| Cluster-scoped | Namespaced | API comments permit the shape, but docs and E2E tests do not establish it as supported; issue #7123 tracks the gap.[^usage-endpoint-types-and-validation][^open-cross-scope-enhancement-report-7123] |

`ClusterUsage` endpoints have no namespace field. Its finder index always uses an empty namespace, so it matches cluster-scoped deletion requests rather than namespaced objects.[^clusterusage-endpoint-schema][^released-namespace-sensitive-finder]

# Composition relationships

In a Composition, selectors may use `matchControllerRef` to constrain both endpoints to resources controlled by the same composite resource.
When a Composition produces multiple resources of the same kind, labels can disambiguate the selected endpoint.[^composition-selector-guidance]

This concept is distinct from provider-defined `ProviderConfigUsage` tracking described in
[References and ProviderConfig](managed-resource-references-and-provider-config.md). `Usage` and `ClusterUsage` are generic Core deletion-protection APIs for arbitrary Kubernetes resources.

# Limitations and project history

Research timestamp: **2026-07-16**. Core evidence remains selected at v2.3.3;
the function-sequencer cross-reference was researched on this date.

- [Issue #7123](https://github.com/crossplane/crossplane/issues/7123), opened by a human author on 2026-02-06 and still open at the research timestamp,
  reports the inability to reliably model dependencies between namespaced and cluster-scoped resources. It proposes expanding `ClusterUsage`, allowing selected
  cross-scope `Usage` relationships, or adding an explicit consent mechanism. These are proposals, not released behavior.
- [Issue #7249](https://github.com/crossplane/crossplane/issues/7249), opened by a human maintainer and still open at the research timestamp,
  reports that a namespaced `Usage` protecting a cluster-scoped `of` resource receives the in-use label but does not block deletion.
  The released v2.3.3 finder retains the reported namespace-key mismatch.[^released-namespace-sensitive-finder]
- [Issue #6336](https://github.com/crossplane/crossplane/issues/6336), opened by a human maintainer and still open at the research timestamp,
  tracks promotion of the `protection.crossplane.io` Usage APIs to GA. It is an enhancement and roadmap-tracking issue, not evidence that GA promotion
  is released or committed to a particular release; the selected v2.3.3 APIs remain Beta.[^beta-maturity-and-feature-flag][^usage-crd-scope-and-served-version][^clusterusage-crd-scope-and-served-version][^open-ga-promotion-tracker-6336]
- [function-sequencer issue #114](https://github.com/crossplane-contrib/function-sequencer/issues/114), opened by human author `@jkroepke` on 2026-03-09, updated 2026-03-10, and still open at the 2026-07-16 research timestamp,
  reports a downstream manifestation in function-sequencer v0.5.0. A cluster-scoped Composition sequencing a namespaced resource produces a `ClusterUsage`
  that cannot encode the resource namespace and remains unready indefinitely.[^function-sequencer-report-114] This report illustrates the Core scope gap but does not independently establish Core behavior.
- [PR #6345](https://github.com/crossplane/crossplane/pull/6345) is human-authored historical context for introducing the v2 Usage APIs on the former `v2` branch.
  Its discussion describes mixed-scope cases as intentionally unresolved rather than a supported contract.[^pr-6345-scope-discussion]
  Its merge commit is not an ancestor of the selected v2.3.3 commit, so current claims rely on the pinned v2.3.3 sources instead.[^diverged-pr-merge-and-v2-3-3-commits]
- Bot-authored stale notices and other automation activity were excluded from project-history evidence.

The in-use label alone is therefore not proof that mixed-scope deletion protection works. For v2.3.3, use `Usage` for documented namespaced relationships and `ClusterUsage` when both endpoints are cluster-scoped.

Composition Functions that generate Usage resources need an additional scope
guard. In function-sequencer v0.6.0, `usageVersion: v2` chooses `ClusterUsage`
when the predecessor (`of`) has no namespace. Do not enable deletion sequencing
for a cluster-scoped predecessor to a namespaced successor: `ClusterUsage` has
no namespace fields and Core cannot resolve that mixed-scope relationship.
This is a function-specific authoring rule derived from the selected function
implementation and the Core scope model, not a general claim that every
function generates Usage resources.[^function-sequencer-v0-6-0-usage-generation]

[^official-purposes-and-terminology]: [Official purposes and terminology](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L10-L19)
[^beta-maturity-and-feature-flag]: [Beta maturity and feature flag](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L21-L30)
[^usage-crd-scope-and-served-version]: [Usage CRD scope and served version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/protection.crossplane.io_usages.yaml#L7-L29)
[^clusterusage-crd-scope-and-served-version]: [ClusterUsage CRD scope and served version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/protection.crossplane.io_clusterusages.yaml#L7-L29)
[^usage-endpoint-types-and-validation]: [Usage endpoint types and validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/usage_types.go#L25-L140)
[^clusterusage-endpoint-schema]: [ClusterUsage endpoint schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/clusterusage_types.go#L25-L67)
[^reconciled-label-ownership-and-availability]: [Reconciled label, ownership, and availability](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L475-L545)
[^deletion-webhook-configuration]: [Deletion webhook configuration](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/webhookconfigurations/usage.yaml#L5-L31)
[^deletion-denial-behavior]: [Deletion denial behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/webhook/protection/usage/handler.go#L93-L157)
[^cleanup-and-deletion-replay]: [Cleanup and deletion replay](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L359-L429)
[^replay-guidance]: [Replay guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L186-L220)
[^namespaced-and-cross-namespace-relationships]: [Namespaced and cross-namespace relationships](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L242-L271)
[^clusterusage-guidance]: [ClusterUsage guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L273-L291)
[^open-cross-scope-enhancement-report-7123]: [Open cross-scope enhancement report #7123](https://github.com/crossplane/crossplane/issues/7123)
[^released-namespace-sensitive-finder]: [Released namespace-sensitive finder](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/protection/usage/finder.go#L72-L133)
[^composition-selector-guidance]: [Composition selector guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L222-L240)
[^one-time-selector-resolution]: [One-time selector resolution](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L148-L159)
[^pr-6345-scope-discussion]: [PR #6345 scope discussion](https://github.com/crossplane/crossplane/pull/6345)
[^diverged-pr-merge-and-v2-3-3-commits]: [Diverged PR merge and v2.3.3 commits](https://github.com/crossplane/crossplane/compare/b90c89203554e2a4a0d5af0eecd72846a4b48c6d...09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d)
[^function-sequencer-report-114]: [function-sequencer report #114](https://github.com/crossplane-contrib/function-sequencer/issues/114)
[^open-ga-promotion-tracker-6336]: [Open GA promotion tracker #6336](https://github.com/crossplane/crossplane/issues/6336)
[^function-sequencer-v0-6-0-usage-generation]: [function-sequencer v0.6.0 Usage generation](https://github.com/crossplane-contrib/function-sequencer/blob/8ee29b46b7b9491fb307cf6caf339541a8d93422/fn.go#L310-L387)
[^function-pipelines-do-not-run-during-xr-deletion]: [Function pipelines do not run during XR deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L143-L148)
