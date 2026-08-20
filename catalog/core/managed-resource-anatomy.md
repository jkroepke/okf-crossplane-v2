---
type: concept
title: Managed resource anatomy
description: Common desired, initialization, observed, policy, provider configuration, and connection-detail fields around provider-defined schemas.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, schema]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: namespaced-common-mr-spec
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_namespace.go#L19-L44'
    title: 'Namespaced common MR spec'
  - id: cluster-common-mr-spec
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_cluster.go#L19-L58'
    title: 'Cluster common MR spec'
  - id: desired-parameters-drift-and-immutable-fields
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L43-L78'
    title: 'Desired parameters, drift, and immutable fields'
  - id: immutability
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L185-L203'
    title: 'immutability'
  - id: beta-initprovider-semantics
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L224-L264'
    title: 'Beta initProvider semantics'
  - id: late-initialization-persistence-gate
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1473-L1521'
    title: 'Late-initialization persistence gate'
  - id: modern-runtime-interface-excludes-deletion-policy
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L200-L219'
    title: 'Modern runtime interface excludes deletion policy'
  - id: observed-composed-resource-identity-overrides-desired-name-changes
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L491-L498'
    title: 'Observed composed-resource identity overrides desired name changes'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [apis/core/v2/resource.go, apis/core/v2/resource_namespace.go, apis/core/v2/resource_cluster.go, internal/controller/apiextensions/composite/composition_functions.go]
feature_state: Stable by repository default; Beta fields identified separately
feature_state_basis: Stable applies to the selected common managed-resource API contract; explicitly Beta initProvider and managementPolicies surfaces retain their lower state.
---

# Common shape

Providers define each concrete MR schema. Common modern contracts supply management policies, a typed `providerConfigRef`, optional connection-secret publication, conditions, and
observed reconciliation status.[^namespaced-common-mr-spec][^cluster-common-mr-spec]

| Area | Meaning | Boundary |
|---|---|---|
| `spec.forProvider` | Desired external-resource parameters, normally continuously enforced | Members and immutability are provider-defined |
| `spec.initProvider` | Create-time parameters not enforced after creation | Explicitly Beta; members are provider-defined |
| `status.atProvider` | Provider-observed external state | No universal field set or Core schema |
| `spec.managementPolicies` | Allowed observe/create/update/late-init/delete actions | Explicitly Beta; provider support varies |
| `spec.providerConfigRef` | Typed provider configuration selection | Credential schema is provider-defined |
| `spec.writeConnectionSecretToRef` | Destination for provider-published connection details | Keys and availability are provider-defined |

The documentation describes `forProvider` as desired state whose mutable fields are normally corrected after out-of-band drift. Kubernetes may accept an edit to a provider-declared
immutable field, but Crossplane does not recreate the external resource solely to apply it.[^desired-parameters-drift-and-immutable-fields][^immutability]

This provider-side immutability is distinct from
[composed-resource identity](composed-resource-identity-and-replacement.md):
under an unchanged logical Composition key, Crossplane preserves an observed
Kubernetes `metadata.name` instead of interpreting a changed name as replacement
intent.[^observed-composed-resource-identity-overrides-desired-name-changes]

# Initialization and observation

`initProvider` settings apply only during creation and are not enforced afterward. The v2.3 documentation recommends excluding `LateInitialize` when `initProvider` would otherwise
conflict with provider-assigned values.[^beta-initprovider-semantics]

Late initialization copies provider-observed values only into eligible unset desired fields. The Provider decides which fields qualify and reports whether observation changed the MR;
the runtime persists the change only when `LateInitialize` is allowed.[^late-initialization-persistence-gate]

# Scope differences

The namespaced common spec defaults `providerConfigRef` to `ClusterProviderConfig/default` and restricts connection-secret publication to the MR namespace. The cluster common spec uses
a cross-namespace Secret reference and also retains `deletionPolicy`; the modern runtime contract does not require deletion policy and gates deletion through management policies.[^namespaced-common-mr-spec][^cluster-common-mr-spec][^modern-runtime-interface-excludes-deletion-policy]

# Limitations

The official page does not document `status.atProvider`, and Core cannot establish its fields. Concrete MR, ProviderConfig, reference, selector, and connection-detail schemas require a
selected Provider release.

[^namespaced-common-mr-spec]: [Namespaced common MR spec](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_namespace.go#L19-L44)
[^cluster-common-mr-spec]: [Cluster common MR spec](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_cluster.go#L19-L58)
[^desired-parameters-drift-and-immutable-fields]: [Desired parameters, drift, and immutable fields](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L43-L78) and [immutability](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L185-L203)
[^immutability]: [immutability](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L185-L203)
[^beta-initprovider-semantics]: [Beta initProvider semantics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L224-L264)
[^late-initialization-persistence-gate]: [Late-initialization persistence gate](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1473-L1521)
[^modern-runtime-interface-excludes-deletion-policy]: [Modern runtime interface excludes deletion policy](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L200-L219)
[^observed-composed-resource-identity-overrides-desired-name-changes]: [Observed composed-resource identity overrides desired name changes](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L491-L498)
