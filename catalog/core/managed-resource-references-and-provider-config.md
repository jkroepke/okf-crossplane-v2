---
type: concept
title: Managed resource references and ProviderConfig
description: Provider-generated cross-resource references, typed provider configuration selection, usage tracking, and connection detail publication.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, references, providerconfig]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: documented-references-and-selectors
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L80-L183'
    title: 'Documented references and selectors'
  - id: generated-reference-resolution-and-field-owner
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/api.go#L196-L262'
    title: 'Generated reference resolution and field owner'
  - id: field-manager-constant
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L39-L43'
    title: 'field-manager constant'
  - id: typed-providerconfig-reference-contract
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L82-L87'
    title: 'Typed ProviderConfig reference contract'
  - id: providerconfig-usage-tracking
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L157-L205'
    title: 'ProviderConfig usage tracking'
  - id: namespaced-common-spec-defaults
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_namespace.go#L19-L44'
    title: 'Namespaced common spec defaults'
  - id: connection-secret-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L453-L504'
    title: 'Connection Secret guidance'
  - id: mrd-metadata-limitation
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L147-L176'
    title: 'MRD metadata limitation'
  - id: namespaced-composition-namespace-enforcement
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L530'
    title: 'Namespaced composition namespace enforcement'
  - id: composition-observed-state-and-status-to-environment-example
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L611-L673'
    title: 'Composition observed state and status-to-environment example'
  - id: observed-identifier-environment-example
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L456-L492'
    title: 'observed identifier environment example'
  - id: reference-resolver-literal-cache-and-re-resolution
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reference/reference.go#L210-L252'
    title: 'Reference resolver literal cache and re-resolution'
  - id: xr-custom-api-and-composition-responsibility-split
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L7-L35'
    title: 'XR custom-API and Composition responsibility split'
  - id: function-patch-and-transform-managed-resource-base
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/function-patch-and-transform.md#L92-L144'
    title: 'Function Patch and Transform managed-resource base'
  - id: managed-resource-providerconfig-selection
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L358-L405'
    title: 'Managed-resource ProviderConfig selection'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/reconciler/managed/api.go, pkg/reconciler/managed/reconciler.go, pkg/reference/reference.go, pkg/resource/providerconfig.go]
feature_state: Not stated by selected sources; individual referenced APIs retain their own maturity
---

# References and selectors

A Provider may generate a literal external-identifier field plus `*Ref` and `*Selector` alternatives. A reference uses a Kubernetes MR name; selectors may match labels or
`matchControllerRef` to select a resource controlled by the same object, such as the same XR.[^documented-references-and-selectors]

Providers define each MR's available settings, so `*Ref` and `*Selector` are
not universal alternatives for every identifier field. Prefer generated
references when the selected Provider CRD exposes them, but inspect that exact
Provider release's CRD and generated controller/schema before depending on a
field such as `vpcIdRef` or `vpcIdSelector`.[^documented-references-and-selectors]

When a concrete MR implements generated reference resolution, the runtime calls it before external reconciliation. It server-side applies the fields changed by the Provider implementation with force ownership under the dedicated
`managed.crossplane.io/api-simple-reference-resolver` field manager.[^generated-reference-resolution-and-field-owner][^field-manager-constant]
Target kinds, readiness rules, selectors, extractors, and assigned fields remain provider-defined.

# Composition fallback and field ownership

When a required relationship has no generated reference field, a Composition
can explicitly place the prerequisite resource's observed identifier into the
dependent resource's desired input. Composition functions receive the observed
composed resources; the documented Patch and Transform pattern copies a
`status.atProvider.id` value into composition environment data for a later
resource.[^composition-observed-state-and-status-to-environment-example][^observed-identifier-environment-example] Treat this as a provider-specific composition pattern, not a
universal fallback: verify the exact observed field, its readiness condition,
and the dependent input field in the selected Provider CRD.

Do not edit a generated literal field as though it were an independently owned
configuration value. With the runtime's generic resolver pattern, a non-empty
resolved literal is cached by default, while clearing it causes a later
reconciliation to resolve it again unless the Provider chose a different
implementation or policy.[^reference-resolver-literal-cache-and-re-resolution] The runtime proves this behavior only for MRs
that implement generated resolution through that pattern; it does not prove
that every Provider or `*Ref`/`*Selector` field will repopulate a particular
literal such as `forProvider.vpcId`.[^generated-reference-resolution-and-field-owner][^field-manager-constant][^reference-resolver-literal-cache-and-re-resolution]

The dedicated server-side apply field owner explains why field ownership can be
surprising when another client changes a resolved literal. It does not, by
itself, establish a universal outcome for `kubectl edit`, client-side
`kubectl apply`, or any specific Provider CRD. Verify those interactions using
the selected Provider's controller and a managed-fields reproduction before
relying on them operationally.[^generated-reference-resolution-and-field-owner][^field-manager-constant]

# ProviderConfig

Modern MRs carry a typed `providerConfigRef` with name and kind. ProviderConfig selects configuration and credentials, but authentication fields and Secret layouts are provider-specific.[^typed-providerconfig-reference-contract]

Usage tracking applies a ProviderConfigUsage keyed to the MR and typed configuration before attempting to use the configuration, so references remain tracked even when configuration is
invalid.[^providerconfig-usage-tracking] Core supplies reusable usage contracts but Providers define the served ProviderConfig and usage CRDs.

The v2.3 docs conflict internally about the omitted-reference default. The released namespaced common type is authoritative: it defaults to
`ClusterProviderConfig/default`.[^namespaced-common-spec-defaults]

# Platform selection guidance

Set `providerConfigRef` explicitly in platform-owned MRs and Compositions. An
omitted reference silently selects `ClusterProviderConfig/default`, which can
hide the intended credential boundary.[^namespaced-common-spec-defaults]

## Keep provider selection out of the XR API by default

An XRD defines the custom API that people use to create XRs; a Composition
defines how that API creates managed resources.[^xr-custom-api-and-composition-responsibility-split] Do not expose a raw
`providerConfigRef` (`kind` and `name`) in a human-orderable XR schema by
default. It selects the credentials and configuration for a composed managed
resource, so it is ordinarily a platform implementation detail. Set it in the
Composition or in the Function-produced managed-resource template instead.[^managed-resource-providerconfig-selection]

This is a platform API design recommendation, not a Crossplane validation
rule. Crossplane does not prohibit an XRD from carrying such fields. If a
product deliberately allows an authorized tenant to choose between approved
account or credential boundaries, expose a constrained, platform-owned
selector—not an unrestricted `ProviderConfig` or `ClusterProviderConfig` name
and kind. Define that selector's authorization, allowed values, and tenancy
semantics for the selected provider rather than relying on implicit defaults.

The documented Function Patch and Transform resource `base` is a managed
resource manifest and may set its `spec.providerConfigRef` there.[^function-patch-and-transform-managed-resource-base] This
keeps a provider-specific kind, scope, and default out of the XR contract.

For tenant-local credentials, prefer the selected provider's namespaced modern
`ProviderConfig` API. A namespaced ProviderConfig cannot be referenced across
namespaces; use a `ClusterProviderConfig` only for an intentional shared or
central account, with the least permissions required. This is platform
security guidance: the actual ProviderConfig GVK and credential schema are
provider-specific.[^typed-providerconfig-reference-contract]

For a central account, subscription, or project (for example, network, identity,
or security) used by tenant compositions, choose deliberately:

- a least-privileged ClusterProviderConfig for the shared account;
- a tenant-local ProviderConfig for that account in every tenant namespace; or
- a composition pattern that keeps the composed resource in the tenant
  namespace, subject to the namespaced-composition boundary.

The last option is constrained by [namespaced composition boundaries](namespaced-composition-boundaries.md); Crossplane does not permit a namespaced XR to compose a resource into another namespace.[^namespaced-composition-namespace-enforcement]

# Connection details

`writeConnectionSecretToRef` selects a Secret destination for provider-published credentials or endpoints. Providers decide whether to publish and which keys exist. Alpha MRDs can document
available keys, but the docs warn that many Providers do not populate that metadata.[^connection-secret-guidance][^mrd-metadata-limitation]

For a Crossplane managed resource, retrieve the selected provider release's
resource-specific connection-detail implementation. An Upjet-based Crossplane
provider may configure `AdditionalConnectionDetailsFn`; another provider may
return typed `managed.ConnectionDetails` and pass it to its reconciler. The CRD
destination schema and `status.atProvider` do not replace that provider-specific
implementation evidence; see [provider connection-detail source retrieval](../providers/provider-connection-details-source-retrieval.md).

[^documented-references-and-selectors]: [Documented references and selectors](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L80-L183)
[^generated-reference-resolution-and-field-owner]: [Generated reference resolution and field owner](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/api.go#L196-L262) and [field-manager constant](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L39-L43)
[^field-manager-constant]: [field-manager constant](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L39-L43)
[^typed-providerconfig-reference-contract]: [Typed ProviderConfig reference contract](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L82-L87)
[^providerconfig-usage-tracking]: [ProviderConfig usage tracking](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L157-L205)
[^namespaced-common-spec-defaults]: [Namespaced common spec defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/resource_namespace.go#L19-L44)
[^connection-secret-guidance]: [Connection Secret guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L453-L504) and [MRD metadata limitation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L147-L176)
[^mrd-metadata-limitation]: [MRD metadata limitation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L147-L176)
[^namespaced-composition-namespace-enforcement]: [Namespaced composition namespace enforcement](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L530)
[^composition-observed-state-and-status-to-environment-example]: [Composition observed state and status-to-environment example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L611-L673) and [observed identifier environment example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L456-L492)
[^observed-identifier-environment-example]: [observed identifier environment example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/environment-configs.md#L456-L492)
[^reference-resolver-literal-cache-and-re-resolution]: [Reference resolver literal cache and re-resolution](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reference/reference.go#L210-L252)
[^xr-custom-api-and-composition-responsibility-split]: [XR custom-API and Composition responsibility split](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L7-L35)
[^function-patch-and-transform-managed-resource-base]: [Function Patch and Transform managed-resource base](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/function-patch-and-transform.md#L92-L144)
[^managed-resource-providerconfig-selection]: [Managed-resource ProviderConfig selection](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L358-L405)
