---
type: Crossplane Provider
title: Provider families and modern managed-resource groups
description: Release-pinned AWS family-package evidence and the Crossplane v2 `.m.` modern namespaced managed-resource convention.
resource: https://github.com/crossplane-contrib/provider-upjet-aws
tags: [crossplane, providers, provider-families, aws, managed-resources, v2]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane-contrib/provider-upjet-aws
source_commit: 857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60
source_paths: [package/crossplane.yaml.tmpl, docs/family/Quickstart.md, package/crds]
feature_state: Beta for the representative `v1beta1` managed-resource APIs; family package topology has no separate maturity label
---

# Overview

A provider family splits a large provider into a shared family/configuration
package and smaller resource packages. This lets an installation select the
resource domains it needs instead of installing the former monolithic package's
complete CRD surface.

The 2023 Crossplane blog records the historical rationale: large providers had
hundreds or thousands of CRDs and provider families were introduced to reduce
the installed set.[1] It is historical context, not evidence of a provider's
current package layout.

# AWS family evidence

For `provider-upjet-aws` v2.6.0, package metadata is the direct classification
source: non-monolithic packages carry a `pkg.crossplane.io/provider-family`
label, and non-configuration resource packages depend on `provider-family-aws`.
The same template deprecates the monolithic package in favor of family resource
packages.[2]

The repository's family quickstart says the first resource-provider installation
also installs the family Provider, which manages shared `ProviderConfig` for
the remaining family members.[3] This establishes AWS's selected-release
topology; it does not prove that every large provider, or every provider named
`family`, follows the same contract.

The GitHub Packages search for `family` is useful discovery evidence, but it is
a mutable UI query. Confirm a particular provider family from its pinned
package labels, dependencies, release metadata, and installation artifacts.

# Modern namespaced groups

The Crossplane v2.3 upgrade guide explicitly contrasts legacy cluster-scoped
`s3.aws.upbound.io` with namespaced `s3.aws.m.upbound.io` and says `.m.` means
“modern namespaced managed resources.”[4] For a provider version that supports
both forms, prefer the `.m.` API when adopting the Crossplane v2 namespaced
model and migration guidance applies.

This is not a universal rule that every `.m.` CRD is preferable in every
deployment, nor a test for family topology. The same guide instructs upgrades
to provider versions supporting both namespaced and cluster-scoped managed
resources.[5] The selected AWS release packages both `*.aws.m.upbound.io` and
non-`.m.` CRD groups, so group name alone cannot classify a package as family or
monolithic.[6][7]

# Relationships

Family packages provide a focused way to manage provider-package blast radius;
they do not change the [parent-scoped ProviderRevision activation rule](provider-package-revisions.md).
The `.m.` convention concerns provider-defined [managed-resource API identity](/core/managed-resources.md), while concrete schemas and migration compatibility remain provider-specific.

# Limitations

Do not infer a Terraform mapping, support commitment, or exact CRD set from a
family name. For an individual managed resource, pin its selected provider
release and inspect its package metadata and CRD/API schema. The historical
blog's CRD-scale observations must not be presented as current performance
guarantees.

# Citations

[1] [Historical provider-family rationale, 13 June 2023](https://blog.crossplane.io/crd-scaling-provider-families/)
[2] [AWS family labels, dependencies, and monolith deprecation](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crossplane.yaml.tmpl#L5-L8) and [deprecation text](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crossplane.yaml.tmpl#L17-L43)
[3] [AWS family ProviderConfig relationship](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/docs/family/Quickstart.md#L57-L84)
[4] [v2.3 modern namespaced `.m.` group definition](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/upgrade-to-crossplane-v2.md#L211-L224)
[5] [v2.3 provider upgrade compatibility guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/upgrade-to-crossplane-v2.md#L226-L244)
[6] [AWS modern Bucket CRD](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crds/s3.aws.m.upbound.io_buckets.yaml#L1-L20)
[7] [AWS non-modern Bucket CRD](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crds/s3.aws.upbound.io_buckets.yaml#L1-L20)
