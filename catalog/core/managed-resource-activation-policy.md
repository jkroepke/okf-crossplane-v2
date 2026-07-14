---
type: api
title: ManagedResourceActivationPolicy
description: The Alpha API that irreversibly activates ManagedResourceDefinitions matched by glob patterns.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resource-activation-policies/
tags: [crossplane, core, managed-resources, api, alpha]
timestamp: 2026-07-14T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml
  - apis/apiextensions/v1alpha1/mrd_policy_types.go
  - internal/controller/apiextensions/activationpolicy/reconciler.go
  - internal/controller/apiextensions/activationpolicy/reconciler_test.go
feature_state: Alpha
project_history_researched_at: 2026-07-14T17:23:20Z
---

# Overview

`ManagedResourceActivationPolicy` (MRAP) is the cluster-scoped, served and stored `apiextensions.crossplane.io/v1alpha1` API for activating groups of
[ManagedResourceDefinitions](managed-resource-definition.md). The served alpha API sets an **Alpha** maturity ceiling.[1]

# Behavior

Required `spec.activate` entries use filepath-style glob patterns, not regular expressions. The controller lists MRDs, patches matching inactive definitions to `Active`, and records sorted
matching names in status.[2][3]

Activation is one-way. After an MRD becomes `Active`, API validation prevents it from returning to `Inactive`. Deleting an MRAP, removing a pattern, or changing a pattern so that an MRD no
longer matches does not deactivate the MRD or remove its derived CRD. MRAP deletion returns without touching MRDs, while normal reconciliation only activates current matches and rebuilds the
policy's observational `status.activated` list.[3][4][5][6][7][8]

# Limitations

The v2.3 MRD documentation explicitly describes activation as irreversible and explains the CRD-safety rationale. The dedicated MRAP page describes policies as additive, but it does not
explicitly warn that deleting a policy or removing one of its patterns cannot undo an earlier activation.[6][7][9]

Open issue #6984 reports this consequence on Crossplane v2.0.6. A maintainer states that deactivation was intentionally excluded from the Alpha implementation and requires additional safety and
controller-lifecycle design. The issue remains an open report, not evidence of a released deactivation path or fix.[10]

Legacy v1-style activation examples are excluded. MRAP controls API activation, not reconciliation policies on individual managed resources.

# Citations

[1] [MRAP identity and schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml#L7-L75)
[2] [Glob matching API types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_policy_types.go#L28-L68)
[3] [Activation reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L106-L147)
[4] [MRAP deletion reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L70-L98)
[5] [MRAP deletion-path test](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler_test.go#L183-L219)
[6] [Irreversible MRD state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L262-L272)
[7] [Irreversible activation in v2.3 documentation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L98-L105)
[8] [MRAP status reconstruction](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L117-L147)
[9] [Additive MRAP behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L446-L450)
[10] [Open issue #6984 and maintainer context](https://github.com/crossplane/crossplane/issues/6984#issuecomment-4917762377), researched 2026-07-14
