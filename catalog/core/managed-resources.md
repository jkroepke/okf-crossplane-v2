---
type: concept
title: Managed resources
description: Provider-defined Kubernetes APIs that continuously manage external resources through a shared Crossplane runtime contract.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, providers]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths: [content/v2.3/managed-resources/managed-resources.md]
feature_state: Stable by repository default
---

# Overview

A managed resource (MR) is the Kubernetes representation of an external resource. Its Provider defines the concrete group, version, kind, desired fields, observed fields,
references, credentials, and external API behavior.[1]

Crossplane Core publishes reusable MR contracts, but no single generic concrete `ManagedResource` CRD. The common runtime requires conditions, management policies, and a typed
ProviderConfig reference, then delegates external `Observe`, `Create`, `Update`, and `Delete` behavior to the Provider.[2][3]

Provider-agnostic MR behavior is **Stable by repository default** because the selected common contracts and runtime have no non-stable label or served alpha/beta API. This does
not raise the maturity of provider-specific resources or the separately Beta and Alpha features below.

# Relationships

- [Anatomy and desired state](managed-resource-anatomy.md) explains common spec/status fields and provider-defined boundaries.
- [Reconciliation lifecycle](managed-resource-lifecycle.md) follows observation, create, update, late initialization, deletion, and polling.
- [Management policies](managed-resource-management-policies.md) gates the allowed lifecycle actions.
- [External identity and creation safety](managed-resource-external-identity.md) covers external names, import boundaries, and leak protection.
- [References and ProviderConfig](managed-resource-references-and-provider-config.md) covers generated references, configuration selection, usages, and connection details.
- [Controls and conditions](managed-resource-controls-and-conditions.md) covers pause, polling, immediate reconcile requests, and status signals.
- Core provides the Alpha [ManagedResourceDefinition](managed-resource-definition.md) and
  [ManagedResourceActivationPolicy](managed-resource-activation-policy.md) APIs for exposing provider-defined MR APIs.

# Limitations

`managementPolicies` and `initProvider` are explicitly Beta. MRD and MRAP are Alpha. Provider support varies, and concrete schemas or behavior require separately pinned provider
sources.[4] Legacy managed-resource interfaces, deletion-policy compatibility paths, Claims, and legacy v1 XR semantics are excluded.

# Citations

[1] [Managed resource model](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L7-L47)
[2] [Modern managed-resource runtime contract](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L200-L219)
[3] [External client operations and observation result](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L383-L410)
[4] [Management policies maturity and provider support](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L285-L305)
