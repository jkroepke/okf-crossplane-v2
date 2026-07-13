---
type: api
title: ManagedResourceActivationPolicy
description: The Alpha API that irreversibly activates ManagedResourceDefinitions matched by glob patterns.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resource-activation-policies/
tags: [crossplane, core, managed-resources, api, alpha]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml, apis/apiextensions/v1alpha1/mrd_policy_types.go]
feature_state: Alpha
---

# Overview

`ManagedResourceActivationPolicy` (MRAP) is the cluster-scoped, served and stored `apiextensions.crossplane.io/v1alpha1` API for activating groups of
[ManagedResourceDefinitions](managed-resource-definition.md). The served alpha API sets an **Alpha** maturity ceiling.[1]

# Behavior

Required `spec.activate` entries use filepath-style glob patterns, not regular expressions. The controller lists MRDs, patches matching inactive definitions to `Active`, and records sorted
matching names in status. It never deactivates MRDs because activation is irreversible.[2][3]

# Limitations

Legacy v1-style activation examples are excluded. MRAP controls API activation, not reconciliation policies on individual managed resources.

# Citations

[1] [MRAP identity and schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourceactivationpolicies.yaml#L7-L75)
[2] [Glob matching API types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_policy_types.go#L28-L68)
[3] [Activation reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L106-L147)
