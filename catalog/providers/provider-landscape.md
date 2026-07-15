---
type: Crossplane Provider
title: Provider implementation families and selection
description: Release-pinned distinctions among Upjet-generated, AWS Go-codegen, and bespoke Crossplane providers, including the AWS migration boundary.
resource: https://github.com/crossplane/upjet
tags: [crossplane, providers, upjet, aws, opentofu]
timestamp: 2026-07-15T00:00:00Z
source_repository: crossplane-contrib/provider-upjet-aws
source_commit: 857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60
source_paths: [README.md, go.mod, package/crds/s3.aws.m.upbound.io_buckets.yaml]
feature_state: Stable by repository default; individual managed-resource APIs require their own maturity evidence
---

# Overview

Provider ownership, implementation method, and support status are separate questions. A GitHub organization name alone does not prove a provider is officially supported or gives it a selection priority.

| Family | Evidence-backed example | What the source establishes |
|---|---|---|
| Upjet-generated | `provider-upjet-aws` v2.6.0 | Upjet turns Terraform-provider schemas into Crossplane CRDs, controllers, examples, and runtime support; this provider explicitly says it is built with Upjet. |
| AWS Go-codegen with manual controller work | `provider-aws` v0.58.0 | Its separate generator produces API-related code, but requires Crossplane-specific additions and controller work. |
| Bespoke provider API | `provider-opentofu` v1.1.4 | Its `Workspace` resource executes OpenTofu modules and exposes OpenTofu-specific inputs and outputs; it is not a projection of every cloud Terraform resource. |

“Community-maintained” is a maintenance/governance category, not an implementation family: Upjet documents both providers it calls official and more than 50 community providers. It is not a complete ownership inventory.[1]

# AWS selection boundary

Do not treat `provider-aws` and `provider-upjet-aws` as interchangeable versions of one API. At the selected releases, their S3 `Bucket` CRDs use different groups and scopes: Upjet AWS uses the namespaced `s3.aws.m.upbound.io`, whereas the selected community AWS provider uses the cluster-scoped `s3.aws.crossplane.io`.[2][3] Existing manifests, compositions, ProviderConfigs, identity, and migration requirements must therefore be evaluated per managed resource.

Upjet documents a migration capability from the community AWS provider to its official AWS provider, which is useful evidence for that concrete path.[4] It does **not** establish a universal rule that an Upjet provider should always replace `provider-<name>` whenever both repositories exist. The same guidance lists cases for considering native providers: no usable Terraform provider, deeply customized reconciliation or API control, or Terraform execution that cannot meet performance needs.[4]

For a selected Upjet managed resource, publish a Terraform relationship only after the resource-level Upjet configuration or metadata names the Terraform resource and matching Terraform schema/documentation is pinned. This catalog foundation deliberately does not infer those mappings from similar names.

# Relationships

Provider-specific managed-resource schemas implement the provider-defined side of [Crossplane Core managed resources](/core/managed-resources.md). The Core concept defines common reconciliation contracts; it does not make two provider GVKs, schemas, or migration paths compatible.

See [Provider package revisions and activation scope](provider-package-revisions.md) for the separate question of how Crossplane activates provider package revisions.

# Limitations

No selected source proves a blanket maintainer policy for all repositories under `crossplane-contrib/` or `upbound/`. Record governance and support commitments only from a provider's own release or maintenance evidence.

# Citations

[1] [Upjet implementation families and provider landscape](https://github.com/crossplane/upjet/blob/b02902e67b336b94e6bd119b86d14077ed0a0a32/README.md#L20-L25) and [official/community scope](https://github.com/crossplane/upjet/blob/b02902e67b336b94e6bd119b86d14077ed0a0a32/README.md#L54-L78)
[2] [provider-upjet-aws Bucket CRD](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crds/s3.aws.m.upbound.io_buckets.yaml#L7-L20)
[3] [provider-aws Bucket CRD](https://github.com/crossplane-contrib/provider-aws/blob/405d4d48d20c332ee427beb4187f80cc4b0af4ea/package/crds/s3.aws.crossplane.io_buckets.yaml#L7-L31)
[4] [Upjet native-provider considerations and AWS migration support](https://github.com/crossplane/upjet/blob/b02902e67b336b94e6bd119b86d14077ed0a0a32/README.md#L79-L125)
[5] [provider-upjet-aws declaration](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/README.md#L20-L23), [provider-aws generation guide](https://github.com/crossplane-contrib/provider-aws/blob/405d4d48d20c332ee427beb4187f80cc4b0af4ea/CODE_GENERATION.md#L74-L161), and [provider-opentofu Workspace API](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/apis/cluster/v1beta1/workspace_types.go#L85-L203)
