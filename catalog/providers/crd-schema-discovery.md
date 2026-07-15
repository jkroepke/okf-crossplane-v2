---
type: Reference
title: Discover provider CRD schemas
description: Retrieve provider CRD inventories quickly from the Upbound API, then use version-pinned package and source artifacts for reproducible work.
tags: [crossplane, providers, crd, schema, upbound]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/provider-upjet-aws
source_commit: 857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60
source_paths:
  - package/crds
supporting_sources:
  - api.upbound.io/v1
  - marketplace.upbound.io
---

# Fast registry lookup

The Upbound API package-resource routes are useful for quickly discovering
available CRDs. Use the package route, not the `/v1/` root by itself:

```text
https://api.upbound.io/v1/packages/upbound/provider-aws-s3/v2.6.1/resources
```

This version-addressed route returns the package resource inventory. To fetch
one CRD definition directly, use its group and kind:

```text
https://api.upbound.io/v1/packages/upbound/provider-aws-s3/latest/resources/s3.aws.m.upbound.io/Bucket
```

The latter is a fast way to inspect the `Bucket` CRD. `latest` is mutable, so
use it for exploration only. For a test, validation fixture, or published
claim, select the exact package version installed by the environment and retain
the retrieved CRD as an explicit fixture. A version in this API URL is useful
package identity, but is not a Git commit pin.

# Package identity boundary

Do not conflate `upbound/provider-aws-s3` with
`crossplane-contrib/provider-aws`. They are different provider families and
their APIs are not interchangeable. There is also no
`crossplane-contrib/provider-aws-s3` repository. The Upbound S3 subpackage
identifies `crossplane-contrib/provider-upjet-aws` as its source.

The Upbound Marketplace documents supported package capabilities including
backporting for selected releases. Do not turn that into a claim that public
Upbound packages and an upstream repository are byte-for-byte equivalent, or
that a particular fix is paywalled: establish the exact package version,
digest, entitlement, and selected upstream source before making a compatibility
or availability claim.

# Source-tree fallback

For the following provider repositories, generated or packaged CRDs are
available under `package/crds/`. This is a useful source fallback when a
registry lookup is not available or when reviewing a selected source release:

| Repository | Pinned CRD directory |
| --- | --- |
| provider-kubernetes | [package/crds](https://github.com/crossplane-contrib/provider-kubernetes/tree/46af47297f636dc015afdf5743929c12990a5fc5/package/crds) |
| provider-sql | [package/crds](https://github.com/crossplane-contrib/provider-sql/tree/9665c434424129d54f2bc265f5921fa3dab29581/package/crds) |
| provider-gitlab | [package/crds](https://github.com/crossplane-contrib/provider-gitlab/tree/c2a24e3ffe91fc25926c2f558f6b1cc97d60e3ee/package/crds) |
| provider-upjet-aws | [package/crds](https://github.com/crossplane-contrib/provider-upjet-aws/tree/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/package/crds) |

These directories reflect the pinned snapshots, not moving `main` or `master`.
Always verify that the source commit and package version correspond to the
provider installed in the target environment.

# Citations

[1] [Version-pinned Upbound package resource inventory](https://api.upbound.io/v1/packages/upbound/provider-aws-s3/v2.6.1/resources)

[2] [Upbound API Bucket CRD lookup](https://api.upbound.io/v1/packages/upbound/provider-aws-s3/latest/resources/s3.aws.m.upbound.io/Bucket)

[3] [Upbound S3 package source identity](https://marketplace.upbound.io/providers/upbound/provider-aws-s3/v2.6.0)

[4] [Different community AWS provider package](https://marketplace.upbound.io/providers/crossplane-contrib/provider-aws/latest)

[5] [Marketplace support capabilities for an Upbound S3 release](https://marketplace.upbound.io/providers/upbound/provider-aws-s3/v2.4.0)
