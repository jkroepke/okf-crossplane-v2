---
type: concept
title: Managed resource references and ProviderConfig
description: Provider-generated cross-resource references, typed provider configuration selection, usage tracking, and connection detail publication.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, references, providerconfig]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/reconciler/managed/api.go, pkg/resource/providerconfig.go, pkg/resource/reference.go]
feature_state: Stable by repository default
---

# References and selectors

A Provider may generate a literal external-identifier field plus `*Ref` and `*Selector` alternatives. A reference uses a Kubernetes MR name; selectors may match labels or
`matchControllerRef` to select a resource controlled by the same object, such as the same XR.[1]

When a concrete MR implements generated reference resolution, the runtime calls it before external reconciliation and server-side applies only the resolved reference fields under a dedicated
field owner.[2] Target kinds, readiness rules, selectors, extractors, and assigned fields remain provider-defined.

# ProviderConfig

Modern MRs carry a typed `providerConfigRef` with name and kind. ProviderConfig selects configuration and credentials, but authentication fields and Secret layouts are provider-specific.[3]

Usage tracking applies a ProviderConfigUsage keyed to the MR and typed configuration before attempting to use the configuration, so references remain tracked even when configuration is
invalid.[4] Core supplies reusable usage contracts but Providers define the served ProviderConfig and usage CRDs.

The v2.3 docs conflict internally about the omitted-reference default. The released namespaced common type is authoritative: it defaults to
`ClusterProviderConfig/default`.[5]

# Connection details

`writeConnectionSecretToRef` selects a Secret destination for provider-published credentials or endpoints. Providers decide whether to publish and which keys exist. Alpha MRDs can document
available keys, but the docs warn that many Providers do not populate that metadata.[6]

# Citations

[1] [Documented references and selectors](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L80-L183)
[2] [Generated reference resolution](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/api.go#L196-L262)
[3] [Typed ProviderConfig reference contract](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L82-L87)
[4] [ProviderConfig usage tracking](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L157-L205)
[5] [Namespaced common spec defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_namespace.go#L19-L44)
[6] [Connection Secret guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L453-L504) and [MRD metadata 
limitation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L147-L176)
