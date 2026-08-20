---
type: api
title: ManagedResourceActivationPolicy
description: The Alpha API that irreversibly activates ManagedResourceDefinitions matched by glob patterns.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resource-activation-policies/
tags: [crossplane, core, managed-resources, api, alpha]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: mrap-identity-and-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml#L7-L75'
    title: 'MRAP identity and schema'
  - id: glob-matching-api-types
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_policy_types.go#L28-L68'
    title: 'Glob matching API types'
  - id: activation-reconciliation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L106-L147'
    title: 'Activation reconciliation'
  - id: mrap-deletion-reconciliation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L70-L98'
    title: 'MRAP deletion reconciliation'
  - id: mrap-deletion-path-test
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler_test.go#L183-L219'
    title: 'MRAP deletion-path test'
  - id: irreversible-mrd-state
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L262-L272'
    title: 'Irreversible MRD state'
  - id: irreversible-activation-in-v2-3-documentation
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L98-L105'
    title: 'Irreversible activation in v2.3 documentation'
  - id: mrap-status-reconstruction
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L117-L147'
    title: 'MRAP status reconstruction'
  - id: additive-mrap-behavior
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L446-L450'
    title: 'Additive MRAP behavior'
  - id: open-issue-6984-and-maintainer-context
    resource: 'https://github.com/crossplane/crossplane/issues/6984#issuecomment-4917762377'
    title: 'Open issue #6984 and maintainer context'
  - id: overlapping-policy-e2e-behavior
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_activation_policy_test.go#L191-L256'
    title: 'Overlapping-policy E2E behavior'
  - id: default-helm-activation-and-disable-override
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L166-L191'
    title: 'Default Helm activation and disable override'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml
  - apis/apiextensions/v1alpha1/mrd_policy_types.go
  - internal/controller/apiextensions/activationpolicy/reconciler.go
  - internal/controller/apiextensions/activationpolicy/reconciler_test.go
  - test/e2e/apiextensions_activation_policy_test.go
  - content/v2.3/managed-resources/managed-resource-activation-policies.md
feature_state: Alpha
project_history_researched_at: 2026-07-14T17:23:20Z
---

# Overview

`ManagedResourceActivationPolicy` (MRAP) is the cluster-scoped, served and stored `apiextensions.crossplane.io/v1alpha1` API for activating groups of
[ManagedResourceDefinitions](managed-resource-definition.md). The served alpha API sets an **Alpha** maturity ceiling.[^mrap-identity-and-schema]

# Behavior

Required `spec.activate` entries use filepath-style glob patterns, not regular expressions. The controller lists MRDs, patches matching inactive definitions to `Active`, and records sorted
matching names in status.[^glob-matching-api-types][^activation-reconciliation]

Activation is one-way. After an MRD becomes `Active`, API validation prevents it from returning to `Inactive`. Deleting an MRAP, removing a pattern, or changing a pattern so that an MRD no
longer matches does not deactivate the MRD or remove its derived CRD. MRAP deletion returns without touching MRDs, while normal reconciliation only activates current matches and rebuilds the
policy's observational `status.activated` list.[^activation-reconciliation][^mrap-deletion-reconciliation][^mrap-deletion-path-test][^irreversible-mrd-state][^irreversible-activation-in-v2-3-documentation][^mrap-status-reconstruction]

# Default activation and overlap

The Helm chart creates a `default` MRAP with `activate: ["*"]`, activating all
**MRDs**. This is MRD activation, not proof that every provider CRD is already
installed. Set `provider.defaultActivations={}` at chart installation to omit
the default activations.[^default-helm-activation-and-disable-override]

Policies are additive: any matching policy activates the MRD, and overlaps are
supported. E2E coverage confirms that specific and wildcard policies can both
report the same MRD as activated; deleting all matching policies leaves it
Active.[^overlapping-policy-e2e-behavior] A policy can therefore be configuration- or composition-scoped, but
it cannot be used later to shrink an already activated API surface.

# Limitations

The v2.3 MRD documentation explicitly describes activation as irreversible and explains the CRD-safety rationale. The dedicated MRAP page describes policies as additive, but it does not
explicitly warn that deleting a policy or removing one of its patterns cannot undo an earlier activation.[^irreversible-mrd-state][^irreversible-activation-in-v2-3-documentation][^additive-mrap-behavior]

Open issue #6984 reports this consequence on Crossplane v2.0.6. A maintainer states that deactivation was intentionally excluded from the Alpha implementation and requires additional safety and
controller-lifecycle design. The issue remains an open report, not evidence of a released deactivation path or fix.[^open-issue-6984-and-maintainer-context]

Legacy v1-style activation examples are excluded. MRAP controls API activation, not reconciliation policies on individual managed resources. Crossplane Core does not establish how an unqualified `kubectl get buckets` resolves when different API groups expose `buckets`; use fully qualified resources while evaluating a migration.

[^mrap-identity-and-schema]: [MRAP identity and schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml#L7-L75)
[^glob-matching-api-types]: [Glob matching API types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_policy_types.go#L28-L68)
[^activation-reconciliation]: [Activation reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L106-L147)
[^mrap-deletion-reconciliation]: [MRAP deletion reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L70-L98)
[^mrap-deletion-path-test]: [MRAP deletion-path test](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler_test.go#L183-L219)
[^irreversible-mrd-state]: [Irreversible MRD state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L262-L272)
[^irreversible-activation-in-v2-3-documentation]: [Irreversible activation in v2.3 documentation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L98-L105)
[^mrap-status-reconstruction]: [MRAP status reconstruction](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L117-L147)
[^additive-mrap-behavior]: [Additive MRAP behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L446-L450)
[^open-issue-6984-and-maintainer-context]: [Open issue #6984 and maintainer context](https://github.com/crossplane/crossplane/issues/6984#issuecomment-4917762377), researched 2026-07-14
[^overlapping-policy-e2e-behavior]: [Overlapping-policy E2E behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_activation_policy_test.go#L191-L256)
[^default-helm-activation-and-disable-override]: [Default Helm activation and disable override](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L166-L191)
