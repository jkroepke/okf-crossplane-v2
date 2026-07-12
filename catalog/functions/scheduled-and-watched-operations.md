---
type: api
title: Scheduled and watched Operations
description: Alpha CronOperation and WatchOperation APIs that create operation-function pipelines from templates.
resource: https://docs.crossplane.io/v2.3/operations/
tags: [crossplane, operation-functions, cronoperation, watchoperation, alpha]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/ops.crossplane.io_cronoperations.yaml
  - cluster/crds/ops.crossplane.io_watchoperations.yaml
---

# Overview

`CronOperation` and `WatchOperation` are cluster-scoped, served and stored `ops.crossplane.io/v1alpha1` APIs. Both are **Alpha** and create [Operations](operation-functions.md) from embedded templates.[1][2]

# CronOperation

`CronOperation` requires a cron `schedule` and `operationTemplate`. Its concurrency policy defaults to `Allow` and also permits `Forbid` or `Replace`; failed and successful history limits default to 1 and 3.[3]

# WatchOperation

`WatchOperation` requires an `operationTemplate` and an immutable watched `apiVersion` and `kind`. An optional namespace and label selector narrow the watched resources; an empty selector watches all resources of the 
kind. The changed resource is injected as the reserved required resource `ops.crossplane.io/watched-resource`.[4][5]

It uses the same `Allow`, `Forbid`, and `Replace` concurrency policies and the same history-limit defaults as `CronOperation`.[6]

# Citations

[1] [CronOperation identity and version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L7-L43)
[2] [WatchOperation identity and version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L7-L46)
[3] [CronOperation template, concurrency, and defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L63-L90) and 
[schedule/history](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L281-L299)
[4] [WatchOperation template and selector](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L84-L100) and [watch selector 
schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L290-L320)
[5] [Watched-resource injection](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/watchoperation.md#L116-L149)
[6] [WatchOperation concurrency and history defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L65-L83)
