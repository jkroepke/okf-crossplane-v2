---
type: index
title: crossplane-core-index
description: Progressive index for Crossplane Core concepts and APIs.
timestamp: 2026-07-12T00:00:00Z
---

# Crossplane Core

* [Composite resource model](composite-resource-model.md) - How XRs, XRDs, Compositions, and composed resources relate in Crossplane v2.
* [CompositeResourceDefinition v2](composite-resource-definition.md) - The current API for defining composite resource types.
* [Composition](composition.md) - The current function-pipeline API for composing resources.
* [Configuration packages](configurations/) - Portable OCI packages of Crossplane APIs, Compositions, and package dependencies.
* [Managed resources](managed-resources.md) - Kubernetes representations of external resources managed by Providers.
* [Managed resource anatomy](managed-resource-anatomy.md) - Common desired, observed, policy, configuration, and connection-detail fields.
* [Managed resource lifecycle](managed-resource-lifecycle.md) - Observe-first creation, update, late-initialization, deletion, and polling behavior.
* [Managed resource management policies](managed-resource-management-policies.md) - Beta action gates for external lifecycle operations.
* [External identity and creation safety](managed-resource-external-identity.md) - External names, provider-specific adoption, and duplicate-creation protection.
* [References and ProviderConfig](managed-resource-references-and-provider-config.md) - Generated references, configuration selection, usages, and connection details.
* [Reconciliation controls and conditions](managed-resource-controls-and-conditions.md) - Pause, polling, reconcile requests, Ready, and Synced signals.
* [ManagedResourceDefinition](managed-resource-definition.md) - The Alpha API for selectively activating provider-defined managed-resource APIs.
* [ManagedResourceActivationPolicy](managed-resource-activation-policy.md) - The Alpha API for activating MRDs by glob pattern.
