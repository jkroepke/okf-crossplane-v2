---
type: concept
title: Managed resource anatomy
description: Common desired, initialization, observed, policy, provider configuration, and connection-detail fields around provider-defined schemas.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, schema]
timestamp: 2026-07-16T00:00:00Z
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
observed reconciliation status.[1][2]

| Area | Meaning | Boundary |
|---|---|---|
| `spec.forProvider` | Desired external-resource parameters, normally continuously enforced | Members and immutability are provider-defined |
| `spec.initProvider` | Create-time parameters not enforced after creation | Explicitly Beta; members are provider-defined |
| `status.atProvider` | Provider-observed external state | No universal field set or Core schema |
| `spec.managementPolicies` | Allowed observe/create/update/late-init/delete actions | Explicitly Beta; provider support varies |
| `spec.providerConfigRef` | Typed provider configuration selection | Credential schema is provider-defined |
| `spec.writeConnectionSecretToRef` | Destination for provider-published connection details | Keys and availability are provider-defined |

The documentation describes `forProvider` as desired state whose mutable fields are normally corrected after out-of-band drift. Kubernetes may accept an edit to a provider-declared
immutable field, but Crossplane does not recreate the external resource solely to apply it.[3]

This provider-side immutability is distinct from
[composed-resource identity](composed-resource-identity-and-replacement.md):
under an unchanged logical Composition key, Crossplane preserves an observed
Kubernetes `metadata.name` instead of interpreting a changed name as replacement
intent.[7]

# Initialization and observation

`initProvider` settings apply only during creation and are not enforced afterward. The v2.3 documentation recommends excluding `LateInitialize` when `initProvider` would otherwise
conflict with provider-assigned values.[4]

Late initialization copies provider-observed values only into eligible unset desired fields. The Provider decides which fields qualify and reports whether observation changed the MR;
the runtime persists the change only when `LateInitialize` is allowed.[5]

# Scope differences

The namespaced common spec defaults `providerConfigRef` to `ClusterProviderConfig/default` and restricts connection-secret publication to the MR namespace. The cluster common spec uses
a cross-namespace Secret reference and also retains `deletionPolicy`; the modern runtime contract does not require deletion policy and gates deletion through management policies.[1][2][6]

# Limitations

The official page does not document `status.atProvider`, and Core cannot establish its fields. Concrete MR, ProviderConfig, reference, selector, and connection-detail schemas require a
selected Provider release.

# Citations

[1] [Namespaced common MR spec](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_namespace.go#L19-L44)
[2] [Cluster common MR spec](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_cluster.go#L19-L58)
[3] [Desired parameters, drift, and immutable fields](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L43-L78) and 
[immutability](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L185-L203)
[4] [Beta initProvider semantics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L224-L264)
[5] [Late-initialization persistence gate](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1473-L1521)
[6] [Modern runtime interface excludes deletion policy](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L200-L219)
[7] [Observed composed-resource identity overrides desired name changes](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L491-L498)
