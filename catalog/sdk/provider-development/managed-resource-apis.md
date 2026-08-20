---
type: Crossplane Development Guide
title: Managed-resource API contracts for a hand-written provider
description: Define a modern managed-resource API from authored Go types and generate its runtime method sets and CRD artifacts.
resource: https://github.com/crossplane/provider-template/tree/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/sample
tags: [crossplane, provider-development, sdk, managed-resource, api, code-generation]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:09:30Z" }
sources:
  - id: sample-managed-resource-type
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/sample/v1alpha1/mytype_types.go#L29-L73'
    title: Sample modern managed-resource type
  - id: sample-api-version
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/sample/v1alpha1/groupversion_info.go#L17-L32'
    title: Sample managed-resource group and version
  - id: managed-resource-interfaces
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L192-L225'
    title: Managed, ModernManaged, and deprecated LegacyManaged interfaces
  - id: generation-directives
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/generate.go#L20-L27'
    title: Provider API generation directives
  - id: angryjet-methodsets
    resource: 'https://github.com/crossplane/crossplane-tools/blob/60e57f817ad1f80dcf052a940cf923fde56fab1f/cmd/angryjet/main.go#L66-L118'
    title: angryjet generated method-set command
source_repository: crossplane/provider-template
source_commit: a74b386da0ec848036e16ff0a207c5a16bc9827f
supporting_source_repositories:
  - repository: crossplane/crossplane-runtime
    tag: v2.3.3
    commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
  - repository: crossplane/crossplane-tools
    commit: 60e57f817ad1f80dcf052a940cf923fde56fab1f
source_paths: [apis/sample/v1alpha1/mytype_types.go, apis/sample/v1alpha1/groupversion_info.go, apis/generate.go]
feature_state: Alpha
feature_state_basis: The owning sample managed-resource API is served as sample.template.crossplane.io/v1alpha1; this state does not transfer to crossplane-runtime.
---

# Authored API shape

The template's `MyType` demonstrates a namespaced modern managed resource:

| Area | Template shape | Provider responsibility |
|---|---|---|
| `spec` | Embeds `ManagedResourceSpec` | Define provider-specific desired parameters under `forProvider` |
| `status` | Embeds `ManagedResourceStatus` | Define provider-observed fields under `atProvider` |
| Kubernetes scope | Namespaced | Choose and generate the intended scope deliberately |
| API version | `sample.template.crossplane.io/v1alpha1` | Select and maintain the provider's own API lifecycle |

The sample types establish the scaffold shape, not a schema for any real
external service.[^sample-managed-resource-type][^sample-api-version] Replace
`MyTypeParameters` and `MyTypeObservation` with fields derived from the external
API and Kubernetes API conventions.

# Runtime interface contract

In crossplane-runtime v2.3.3, `resource.Managed` combines Kubernetes object,
management-policy, and condition behavior. `resource.ModernManaged` adds a
local connection-secret target and a typed ProviderConfig reference.[^managed-resource-interfaces]

Use the modern contract for new namespace-scoped managed resources. The SDK's
`LegacyManaged` shape carries an arbitrary-namespace connection Secret,
untyped ProviderConfig reference, and deletion policy; it is explicitly
deprecated for new namespace-scoped managed resources.[^managed-resource-interfaces]

The Go interface maturity is **Not stated by selected sources**. The **Alpha**
state on this page belongs to the template's sample `v1alpha1` API, not to the
runtime package.

# Authored versus generated files

Edit the API type and registration files. The template's generation directive
then:

1. removes the existing packaged CRDs;
2. runs `controller-gen` for deepcopy methods and v1 CRDs; and
3. runs `angryjet generate-methodsets` for Crossplane interface methods.[^generation-directives][^angryjet-methodsets]

Treat `zz_generated*.go` and `package/crds/**` as generated outputs. Review
their diff after changing API types, but make the corresponding authored Go
types or generator configuration the source change.

# Relationships

The API's typed `providerConfigRef` connects it to
[provider configuration and credential wiring](provider-configuration.md).
The generated managed-resource methods allow the
[managed reconciler](managed-reconciler.md) to operate on the resource.

[^sample-managed-resource-type]: [Sample modern managed-resource type](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/sample/v1alpha1/mytype_types.go#L29-L73)
[^sample-api-version]: [Sample managed-resource group and version](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/sample/v1alpha1/groupversion_info.go#L17-L32)
[^managed-resource-interfaces]: [Managed, ModernManaged, and deprecated LegacyManaged interfaces](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/interfaces.go#L192-L225)
[^generation-directives]: [Provider API generation directives](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/generate.go#L20-L27)
[^angryjet-methodsets]: [angryjet generated method-set command](https://github.com/crossplane/crossplane-tools/blob/60e57f817ad1f80dcf052a940cf923fde56fab1f/cmd/angryjet/main.go#L66-L118)
