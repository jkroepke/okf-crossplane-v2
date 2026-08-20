---
type: Crossplane Development Guide
title: Provider configuration, credential extraction, and usage tracking
description: Implement namespaced and cluster-scoped provider configuration with typed usage records and provider-specific credential handling.
resource: https://github.com/crossplane/provider-template/tree/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/v1alpha1
tags: [crossplane, provider-development, sdk, providerconfig, credentials]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:09:30Z" }
sources:
  - id: provider-config-types
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/v1alpha1/types.go#L22-L110'
    title: Template ProviderConfig, credentials, and usage types
  - id: provider-config-schema
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/package/crds/template.crossplane.io_providerconfigs.yaml#L52-L112'
    title: Generated ProviderConfig credential schema
  - id: provider-config-controllers
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/config/config.go#L30-L82'
    title: ProviderConfig controller wiring
  - id: template-connector
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype.go#L120-L161'
    title: Template config lookup and credential extraction
  - id: common-credential-extractor
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L60-L113'
    title: crossplane-runtime common credential extractor
  - id: typed-usage-tracker
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L157-L207'
    title: Typed ProviderConfig usage tracker
  - id: provider-config-examples
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/examples/provider/config.yaml#L15-L38'
    title: Template Secret credential examples
  - id: readme-secret-only-description
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/README.md#L3-L10'
    title: README ProviderConfig summary
source_repository: crossplane/provider-template
source_commit: a74b386da0ec848036e16ff0a207c5a16bc9827f
supporting_source_repository: crossplane/crossplane-runtime
supporting_source_tag: v2.3.3
supporting_source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [apis/v1alpha1/types.go, internal/controller/config/config.go, internal/controller/mytype/mytype.go, examples/provider/config.yaml]
feature_state: Alpha
feature_state_basis: The owning template ProviderConfig and ProviderConfigUsage APIs are served as template.crossplane.io/v1alpha1.
---

# Configuration API

The template supplies one shared configuration spec across two scopes and one
typed usage kind:[^provider-config-types]

| Kind | Scope | Purpose |
|---|---|---|
| `ProviderConfig` | Namespaced | Configuration selected by a namespaced managed resource |
| `ClusterProviderConfig` | Cluster | Shared cluster-scoped configuration |
| `ProviderConfigUsage` | Namespaced | Typed record linking a managed resource to either configuration kind |

Both configuration controllers use crossplane-runtime's ProviderConfig
reconciler and watch usage records to enqueue the referenced configuration.[^provider-config-controllers]
The whole template API is `template.crossplane.io/v1alpha1`, so these concrete
sample APIs are **Alpha**.

# Credential sources

The authored type and generated schema admit `None`, `Secret`,
`InjectedIdentity`, `Environment`, and `Filesystem` credential sources.[^provider-config-types][^provider-config-schema]
The template connector passes that selection to
`CommonCredentialExtractor`.[^template-connector]

The runtime helper handles `None`, Secret, environment, and filesystem
selectors. It deliberately does not provide a generic InjectedIdentity
implementation because identity injection is provider-specific.[^common-credential-extractor]
If the new provider exposes `InjectedIdentity`, add and test its provider-specific
handling rather than assuming the common extractor implements it.

The README calls the sample ProviderConfig Secret-only, but the selected types
and generated schema expose all five sources.[^readme-secret-only-description][^provider-config-types][^provider-config-schema]
This is a source disagreement: use the types and schema for API shape, while
treating the README sentence as incomplete.

# Usage-before-configuration order

The runtime usage tracker derives a typed usage name from the managed-resource
UID and requires the ProviderConfig reference to include its kind. Its contract
specifically calls for tracking usage before trying to use the configuration,
so a misconfigured ProviderConfig is still represented by a usage record.[^typed-usage-tracker]

The template connector follows that order:

1. track the selected config usage;
2. fetch either `ProviderConfig` or `ClusterProviderConfig` by the typed kind;
3. extract credentials; and
4. construct the provider-specific external service client.[^template-connector]

The checked-in examples demonstrate Secret selectors for both configuration
scopes.[^provider-config-examples] They do not demonstrate the other admitted
credential sources; add provider-specific tests and examples for every source
the finished API retains.

# Relationships

Managed resources carry the typed reference described in
[managed-resource API contracts](managed-resource-apis.md). The connector uses
the resolved configuration to create the client used by the
[managed reconciler lifecycle](managed-reconciler.md).

[^provider-config-types]: [Template ProviderConfig, credentials, and usage types](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/v1alpha1/types.go#L22-L110)
[^provider-config-schema]: [Generated ProviderConfig credential schema](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/package/crds/template.crossplane.io_providerconfigs.yaml#L52-L112)
[^provider-config-controllers]: [ProviderConfig controller wiring](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/config/config.go#L30-L82)
[^template-connector]: [Template config lookup and credential extraction](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype.go#L120-L161)
[^common-credential-extractor]: [crossplane-runtime common credential extractor](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L60-L113)
[^typed-usage-tracker]: [Typed ProviderConfig usage tracker](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/providerconfig.go#L157-L207)
[^provider-config-examples]: [Template Secret credential examples](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/examples/provider/config.yaml#L15-L38)
[^readme-secret-only-description]: [README ProviderConfig summary](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/README.md#L3-L10)
