---
type: Crossplane API
title: ConfigurationRevision
description: A controller-managed revision created when a Crossplane Configuration changes.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, configurations, revisions, api]
timestamp: 2026-07-12T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/pkg.crossplane.io_configurationrevisions.yaml
  - apis/pkg/v1/configuration_types.go
  - apis/pkg/v1/revision_types.go
feature_state: Not stated by selected sources
---

# Overview

`ConfigurationRevision` is a cluster-scoped `pkg.crossplane.io/v1` API, served and stored without deprecation metadata. Crossplane creates a revision when a [Configuration](configuration.md) changes, manages it, and directs users not to edit it directly.[1]

# Schema

The required fields are `desiredState`, `image`, and `revision`. Desired state is `Active` or `Inactive`; the image is used for package installation, and the revision number participates in garbage collection according to the parent Configuration's history limit.[2] The Go revision types directly define the desired-state constants and provide the source types for the generated schema.[3]

Status exposes conditions, dependency counts, owned object references, applied image configurations, a potentially rewritten resolved image, and opaque capabilities.[4]

# Behavior

Installing a newer package version creates a new revision. One revision is active and determines the installed Composition and XRD resources; by default one inactive revision is retained.[5] Automatic activation selects the newest revision, while manual activation leaves activation under user control.[6]

# Limitations

Feature maturity is not stated. The generated CRD reports `controller-gen` v0.19.0.[7] Desired state is defined by Go constants but not encoded as an OpenAPI enum. No rollback-specific field or status exists, so this page does not claim a rollback procedure.

# Citations

[1] [ConfigurationRevision identity and ownership](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurationrevisions.yaml#L7-L53)
[2] [Required revision fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurationrevisions.yaml#L91-L154)
[3] [Revision state source types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/v1/revision_types.go#L25-L114)
[4] [ConfigurationRevision status](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurationrevisions.yaml#L155-L275)
[5] [Revision lifecycle and retention](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L102-L142)
[6] [Automatic and manual activation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L177-L208)
[7] [Generated artifact annotation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurationrevisions.yaml#L1-L7)
