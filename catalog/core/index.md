# Crossplane Core

# Composition

* [Composition developer starter guide](../composition-developer-starter.md) - Route through API/provider design, pipeline/security design, and mandatory verification.
* [Composite resource model](composite-resource-model.md) - How XRs, XRDs, Compositions, and composed resources relate in Crossplane v2.
* [CompositeResourceDefinition v2](composite-resource-definition.md) - The current API for defining composite resource types.
* [XRD OpenAPI schemas](xrd-openapi-schema.md) - Model an XR API with an OpenAPI v3 schema that Crossplane carries into its generated CRD.
* [XRD CEL validation](xrd-cel-validation.md) - Apply schema-scoped CEL rules and understand the current root-rule release boundary.
* [XRD unknown data and collections](xrd-unknown-data.md) - Choose pruning, preserved data, and Kubernetes list semantics deliberately.
* [XRD API version evolution](xrd-api-version-evolution.md) - Serve and reference XR versions, with CRD conversion boundaries.
* [XRD scale and display](xrd-subresources-and-display.md) - Expose `/scale` and useful `kubectl get` columns from an XRD version.
* [Tenant XR API and admission security](tenant-xr-api-security.md) - Organization-specific API-group, RBAC, namespace, and admission-policy hardening guidance.
* [Composition](composition.md) - The current function-pipeline API for composing resources.
* [Composed-resource identity and replacement](composed-resource-identity-and-replacement.md) - Why changing metadata.name under an unchanged logical key does not rename or replace an existing object, and how to stage replacement.
* [Composition project layout](composition-project-layout.md) - A reference manifest layout that keeps render inputs and provider setup distinct.
* [Controlled rollout design for Composition Functions](controlled-rollout-of-composition-functions-design.md) - Historical accepted proposal; selected-release source proof shows its rollout API is not current behavior.
* [Composed-resource RBAC](composed-resource-rbac.md) - Why Crossplane cannot manage every Kubernetes resource kind by default and how to grant additional access.
* [Real-time composition reconciliation](realtime-composition-reconciliation.md) - Beta composed-resource watches, TTL requeues, and required-resource refresh boundaries.
* [Real-time composition project history](realtime-composition-project-history.md) - Selected-release churn reports, a contained runtime fix, and the post-release GA proposal.
* [Namespaced composition boundaries](namespaced-composition-boundaries.md) - Same-namespace enforcement with PR #6588 release and source proof.
* [Cross-namespace synchronization patterns](cross-namespace-synchronization-patterns.md) - Evidence-backed provider-kubernetes and community-controller tradeoffs.
* [Composition health in GitOps tools](composition-gitops-health.md) - Native status limitations and the documented Argo CD and Flux customization boundaries.
* [Push platform-team Secrets to external stores](pushsecret-external-store-pattern.md) - An Alpha External Secrets Operator pattern for publishing selected Kubernetes Secret data to configured external stores.

# Environment and migration

* [EnvironmentConfig](environment-config.md) - The retained Beta cluster-scoped data API consumed by environment-aware functions.
* [Native Composition environment removal](native-composition-environment-removal.md) - The v1.18 removal and migration boundary without conflating it with the retained resource API.

# Configuration packages

* [Configuration packages](configurations/index.md) - Portable OCI packages of Crossplane APIs, Compositions, and package dependencies.

# Managed resources

* [Managed resources](managed-resources.md) - Kubernetes representations of external resources managed by Providers.
* [Managed resource anatomy](managed-resource-anatomy.md) - Common desired, observed, policy, configuration, and connection-detail fields.
* [Managed resource lifecycle](managed-resource-lifecycle.md) - Observe-first creation, update, late-initialization, deletion, and polling behavior.
* [Managed resource management policies](managed-resource-management-policies.md) - Beta action gates for external lifecycle operations.
* [Management Policies project history](managed-resource-management-policies-project-history.md) - GA tracking, known reports, proposals, and selected-release containment.
* [Usage and ClusterUsage deletion protection](usages-and-clusterusages.md) - Beta deletion protection, ordering behavior, scope rules, and mixed-scope limitations.
* [External identity and creation safety](managed-resource-external-identity.md) - External names, provider-specific adoption, and duplicate-creation protection.
* [References and ProviderConfig](managed-resource-references-and-provider-config.md) - Generated references, configuration selection, usages, and connection details.
* [Reconciliation controls and conditions](managed-resource-controls-and-conditions.md) - Pause, polling, reconcile requests, Ready, and Synced signals.
* [ManagedResourceDefinition](managed-resource-definition.md) - The Alpha API for selectively activating provider-defined managed-resource APIs.
* [ManagedResourceActivationPolicy](managed-resource-activation-policy.md) - The Alpha API for activating MRDs by glob pattern.
* [Minimal managed-resource activation](minimal-managed-resource-activation.md) - A preventive platform policy for explicit modern MRD activation and configuration-scoped dependencies.
