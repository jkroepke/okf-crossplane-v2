---
type: Crossplane Provider
title: Upjet Terraform provenance and example conversion
description: A release-pinned evidence chain for researching Upjet resources from their Terraform provider baseline without guessing the Crossplane API.
resource: https://github.com/crossplane-contrib/provider-upjet-aws
tags: [crossplane, providers, upjet, terraform, examples]
timestamp: 2026-07-15T00:00:00Z
source_repository: crossplane-contrib/provider-upjet-aws
source_commit: 857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60
source_paths: [Makefile, config/namespaced/s3/config.go, package/crds/s3.aws.m.upbound.io_buckets.yaml]
feature_state: Stable by repository default; individual managed-resource APIs retain their own version maturity
---

# Overview

An Upjet provider's selected-release `Makefile` is the provenance entry point
for its upstream Terraform baseline. In `provider-upjet-aws` v2.6.0 it pins
Terraform AWS `6.34.0`, `hashicorp/aws`, its repository, and the upstream
documentation path. The build derives `config/schema.json` from that version
and fetches its documentation tree.[1]

This makes Terraform documentation a strong supporting source for upstream
examples and arguments. It is not a drop-in Crossplane API specification.

Repository names are not implementation evidence: a provider may be
Upjet-generated without `upjet` in its name. Treat a release README that
explicitly declares Upjet as direct orientation evidence, then corroborate it
with the selected release's Makefile, `go.mod`, and resource configuration
before using Terraform documentation as supporting example material.[5]

# Required conversion evidence

Before adapting a Terraform example, require all of:

1. The selected Upjet provider Makefile, to pin Terraform source and version.
2. Resource-level Upjet configuration or metadata naming the Terraform resource
   and recording transformations.
3. The selected generated Crossplane CRD/schema, to establish the public GVK,
   scope, and fields.
4. The configured upstream Terraform documentation snapshot, as a supporting example.

For example, AWS's namespaced S3 configuration explicitly selects
`aws_s3_bucket` and adds Crossplane/Upjet transformations; the generated API is
the namespaced `Bucket` at `buckets.s3.aws.m.upbound.io`.[2][3] The matching
Terraform v6.34.0 S3 documentation is useful input, but its HCL must be
independently adapted to the generated Crossplane schema.[4]

# Why this matters

This chain avoids two common errors: using Terraform docs for a different
provider documentation snapshot, and inferring that similarly named Terraform and Crossplane
resources have identical fields or behavior. Upjet configuration can rename
fields, add references/selectors, move fields to status, inject defaults, or
exclude a resource.

Do not copy Terraform examples without verified licensing and attribution.
Prefer a concise, independently authored Crossplane example that cites the
four sources above.

For this AWS release, the schema binary is the Upbound fork release
`v6.34.0-upjet.1`, while the fetched documentation is upstream HashiCorp
`v6.34.0`. The latter may not describe fork-specific differences; the selected
resource configuration and generated Crossplane CRD remain authoritative.

# Provider example artifacts

Treat `examples/` as resource-focused coverage material, not as a curated
reference-architecture library: AWS CI checks that CRD types have examples.[6]
Some examples include prerequisite resources, so they are not categorically
single-resource manifests. They still do not establish an end-to-end platform
use case.[7]

`examples-generated/` is generator output derived from provider metadata and
configuration. Use it to inspect generated API illustration, but keep it
distinct from `examples/` and from independently sourced
composition/use-case patterns.[8]

# Relationships

This is the required evidence gate for a resource-specific Upjet mapping and
complements [provider implementation families](provider-landscape.md). For
modern namespaced resource selection, see [provider families](provider-families.md).

# Citations

[1] [AWS Makefile Terraform baseline](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/Makefile#L13-L18), [schema generation](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/Makefile#L168-L174), and [documentation fetch](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/Makefile#L193-L208)
[2] [AWS S3 Upjet resource configuration](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/config/namespaced/s3/config.go#L13-L56)
[3] [Generated modern AWS Bucket CRD](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crds/s3.aws.m.upbound.io_buckets.yaml#L7-L108)
[4] [Terraform AWS v6.34.0 S3 Bucket documentation](https://github.com/hashicorp/terraform-provider-aws/blob/b53a72bc2e0bf0395b4b1f91e06340785ddaac86/website/docs/r/s3_bucket.html.markdown#L9-L43)
[5] [provider-upjet-aws Upjet declaration](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/README.md#L20-L23) and [selected release Upjet/Terraform dependencies](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/go.mod#L21-L32)
[6] [Examples CI coverage check](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/.github/workflows/ci.yml#L218-L231) and [checker behavior](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/scripts/check-examples.py#L11-L60)
[7] [Multi-resource EKS example](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/examples/eks/namespaced/v1beta1/accessentry.yaml)
[8] [Generated-example pipeline](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/cmd/generator/main.go#L39-L55) and [metadata/config inputs](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/config/provider-metadata.yaml#L1-L29)
