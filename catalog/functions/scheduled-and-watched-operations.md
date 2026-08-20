---
type: api
title: Scheduled and watched Operations
description: Alpha CronOperation and WatchOperation APIs that create operation-function pipelines from templates.
resource: https://docs.crossplane.io/v2.3/operations/
tags: [crossplane, operation-functions, cronoperation, watchoperation, alpha]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: cronoperation-identity-and-version
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L7-L43'
    title: 'CronOperation identity and version'
  - id: watchoperation-identity-and-version
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L7-L46'
    title: 'WatchOperation identity and version'
  - id: cronoperation-template-concurrency-and-defaults
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L63-L90'
    title: 'CronOperation template, concurrency, and defaults'
  - id: schedule-history
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L281-L299'
    title: 'schedule/history'
  - id: watchoperation-template-and-selector
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L84-L100'
    title: 'WatchOperation template and selector'
  - id: watch-selector-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L290-L320'
    title: 'watch selector schema'
  - id: watched-resource-injection
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/watchoperation.md#L116-L149'
    title: 'Watched-resource injection'
  - id: watchoperation-concurrency-and-history-defaults
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L65-L83'
    title: 'WatchOperation concurrency and history defaults'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/ops.crossplane.io_cronoperations.yaml
  - cluster/crds/ops.crossplane.io_watchoperations.yaml
---

# Overview

`CronOperation` and `WatchOperation` are cluster-scoped, served and stored `ops.crossplane.io/v1alpha1` APIs. Both are **Alpha** and create [Operations](operation-functions.md) from embedded templates.[^cronoperation-identity-and-version][^watchoperation-identity-and-version]

# CronOperation

`CronOperation` requires a cron `schedule` and `operationTemplate`. Its concurrency policy defaults to `Allow` and also permits `Forbid` or `Replace`; failed and successful history limits default to 1 and 3.[^cronoperation-template-concurrency-and-defaults][^schedule-history]

# WatchOperation

`WatchOperation` requires an `operationTemplate` and an immutable watched `apiVersion` and `kind`. An optional namespace and label selector narrow the watched resources; an empty selector watches all resources of the 
kind. The changed resource is injected as the reserved required resource `ops.crossplane.io/watched-resource`.[^watchoperation-template-and-selector][^watch-selector-schema][^watched-resource-injection]

It uses the same `Allow`, `Forbid`, and `Replace` concurrency policies and the same history-limit defaults as `CronOperation`.[^watchoperation-concurrency-and-history-defaults]

[^cronoperation-identity-and-version]: [CronOperation identity and version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L7-L43)
[^watchoperation-identity-and-version]: [WatchOperation identity and version](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L7-L46)
[^cronoperation-template-concurrency-and-defaults]: [CronOperation template, concurrency, and defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L63-L90) and [schedule/history](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L281-L299)
[^schedule-history]: [schedule/history](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L281-L299)
[^watchoperation-template-and-selector]: [WatchOperation template and selector](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L84-L100) and [watch selector schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L290-L320)
[^watch-selector-schema]: [watch selector schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L290-L320)
[^watched-resource-injection]: [Watched-resource injection](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/watchoperation.md#L116-L149)
[^watchoperation-concurrency-and-history-defaults]: [WatchOperation concurrency and history defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L65-L83)
