---
type: concept
title: Usage and ClusterUsage deletion protection
description: Beta Core APIs that block deletion of used resources and model deletion ordering across supported Kubernetes scopes.
resource: https://docs.crossplane.io/v2.3/managed-resources/usages/
tags: [crossplane, core, usage, deletion-protection, beta]
timestamp: 2026-07-14T00:00:00Z
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
feature_state: Beta
---

# Overview

`Usage` and `ClusterUsage` describe a relationship in which a resource identified by `spec.by` uses the resource identified by `spec.of`.
Crossplane blocks deletion of the `of` resource while the relationship exists. This supports accidental-deletion protection and deletion ordering:
a dependent can be deleted before the resource it needs.[1]

The APIs do not schedule creation or wait for the `of` resource to become ready. Their ordering guarantee is limited to deletion protection.

Both APIs are **Beta**, served and stored as `protection.crossplane.io/v1beta1`. Usages are enabled by default and can be disabled with `--enable-usages=false`.[2][3][4]

# Schema

| Field | Purpose |
|---|---|
| `spec.of` | Required identity of the protected or used resource. |
| `spec.by` | Optional identity of the using or dependent resource. |
| `spec.reason` | Optional human-readable reason for protection when no dependent resource is needed. |
| `spec.replayDeletion` | Replays a previously blocked deletion after the Usage is removed. Defaults to `false`. |

At least one of `spec.by` or `spec.reason` is required. Each present `of` or `by` endpoint uses either `resourceRef` or `resourceSelector`;
a reference takes precedence if both are supplied. Selector resolution persists the chosen name into the reference and does not continuously retarget the Usage.[5][17]

# Behavior

After resolving the endpoints, the controller:

1. adds `crossplane.io/in-use: "true"` to the `of` resource;
2. adds the `by` resource as an owner of the Usage when present;
3. reports the Usage as available and periodically rechecks it.[7]

A fail-closed validating webhook intercepts deletion of labelled resources. It finds matching Usages, records the attempted propagation policy, and denies deletion with HTTP 409 Conflict while at least one Usage remains.[8][9]

When a Usage is deleted, Crossplane removes the in-use label only after the last protecting Usage is gone. With `replayDeletion: true`, it retries an earlier blocked deletion
using the recorded propagation policy.[10] Official guidance recommends replay for composed-resource deletion ordering because it avoids waiting for a later deletion retry.[11]

# Scope model

`Usage` is namespaced. `ClusterUsage` is cluster-scoped.[3][4]

| `by` endpoint | `of` endpoint | Model and boundary |
|---|---|---|
| Namespaced | Same namespace | A `Usage` in that namespace is the normal model. |
| Namespaced | Different namespace | `Usage` supports an explicit namespace only on `of`; `by` must be present and remains in the Usage namespace.[12] |
| Cluster-scoped | Cluster-scoped | `ClusterUsage` is the documented model.[13] |
| Namespaced | Cluster-scoped | The `Usage` type can express this shape, but released v2.3.3 deletion lookup is silently ineffective; do not rely on it.[14][15] |
| Cluster-scoped | Namespaced | API comments permit the shape, but docs and E2E tests do not establish it as supported; issue #7123 tracks the gap.[5][14] |

`ClusterUsage` endpoints have no namespace field. Its finder index always uses an empty namespace, so it matches cluster-scoped deletion requests rather than namespaced objects.[6][15]

# Composition relationships

In a Composition, selectors may use `matchControllerRef` to constrain both endpoints to resources controlled by the same composite resource.
When a Composition produces multiple resources of the same kind, labels can disambiguate the selected endpoint.[16]

This concept is distinct from provider-defined `ProviderConfigUsage` tracking described in
[References and ProviderConfig](managed-resource-references-and-provider-config.md). `Usage` and `ClusterUsage` are generic Core deletion-protection APIs for arbitrary Kubernetes resources.

# Limitations and project history

Research timestamp: **2026-07-14**.

- [Issue #7123](https://github.com/crossplane/crossplane/issues/7123), opened by a human author on 2026-02-06 and still open at the research timestamp,
  reports the inability to reliably model dependencies between namespaced and cluster-scoped resources. It proposes expanding `ClusterUsage`, allowing selected
  cross-scope `Usage` relationships, or adding an explicit consent mechanism. These are proposals, not released behavior.
- [Issue #7249](https://github.com/crossplane/crossplane/issues/7249), opened by a human maintainer and still open at the research timestamp,
  reports that a namespaced `Usage` protecting a cluster-scoped `of` resource receives the in-use label but does not block deletion.
  The released v2.3.3 finder retains the reported namespace-key mismatch.[15]
- [Issue #6336](https://github.com/crossplane/crossplane/issues/6336), opened by a human maintainer and still open at the research timestamp,
  tracks promotion of the `protection.crossplane.io` Usage APIs to GA. It is an enhancement and roadmap-tracking issue, not evidence that GA promotion
  is released or committed to a particular release; the selected v2.3.3 APIs remain Beta.[2][3][4][21]
- [function-sequencer issue #114](https://github.com/crossplane-contrib/function-sequencer/issues/114), opened by a human author and still open at the research timestamp,
  reports a downstream manifestation in function-sequencer v0.5.0. A cluster-scoped Composition sequencing a namespaced resource produces a `ClusterUsage`
  that cannot encode the resource namespace and remains unready indefinitely.[20] This report illustrates the Core scope gap but does not independently establish Core behavior.
- [PR #6345](https://github.com/crossplane/crossplane/pull/6345) is human-authored historical context for introducing the v2 Usage APIs on the former `v2` branch.
  Its discussion describes mixed-scope cases as intentionally unresolved rather than a supported contract.[18]
  Its merge commit is not an ancestor of the selected v2.3.3 commit, so current claims rely on the pinned v2.3.3 sources instead.[19]
- Bot-authored stale notices and other automation activity were excluded from project-history evidence.

The in-use label alone is therefore not proof that mixed-scope deletion protection works. For v2.3.3, use `Usage` for documented namespaced relationships and `ClusterUsage` when both endpoints are cluster-scoped.

# Citations

[1] [Official purposes and terminology](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L10-L19)
[2] [Beta maturity and feature flag](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L21-L30)
[3] [Usage CRD scope and served version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/protection.crossplane.io_usages.yaml#L7-L29)
[4] [ClusterUsage CRD scope and served version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/protection.crossplane.io_clusterusages.yaml#L7-L29)
[5] [Usage endpoint types and validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/usage_types.go#L25-L140)
[6] [ClusterUsage endpoint schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/protection/v1beta1/clusterusage_types.go#L25-L67)
[7] [Reconciled label, ownership, and availability](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L475-L545)
[8] [Deletion webhook configuration](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/webhookconfigurations/usage.yaml#L5-L31)
[9] [Deletion denial behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/webhook/protection/usage/handler.go#L93-L157)
[10] [Cleanup and deletion replay](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/protection/usage/reconciler.go#L359-L429)
[11] [Replay guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L186-L220)
[12] [Namespaced and cross-namespace relationships](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L242-L271)
[13] [ClusterUsage guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L273-L291)
[14] [Open cross-scope enhancement report #7123](https://github.com/crossplane/crossplane/issues/7123)
[15] [Released namespace-sensitive finder](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/protection/usage/finder.go#L72-L133)
[16] [Composition selector guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L222-L240)
[17] [One-time selector resolution](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/usages.md#L148-L159)
[18] [PR #6345 scope discussion](https://github.com/crossplane/crossplane/pull/6345)
[19] [Diverged PR merge and v2.3.3 commits](https://github.com/crossplane/crossplane/compare/b90c89203554e2a4a0d5af0eecd72846a4b48c6d...09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d)
[20] [function-sequencer report #114](https://github.com/crossplane-contrib/function-sequencer/issues/114)
[21] [Open GA promotion tracker #6336](https://github.com/crossplane/crossplane/issues/6336)
