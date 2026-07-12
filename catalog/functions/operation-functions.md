---
type: concept
title: Operation functions
description: Alpha functions that run once-to-completion operational pipelines directly, on a schedule, or after watched-resource changes.
resource: https://docs.crossplane.io/v2.3/operations/operation/
tags: [crossplane, operation-functions, operations, alpha]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/ops.crossplane.io_operations.yaml
  - internal/controller/ops/operation/reconciler.go
---

# Overview

An operation function runs in an `Operation` pipeline once to completion instead of continuously reconciling an XR. Operation APIs are served as `ops.crossplane.io/v1alpha1`, explicitly documented as Alpha, and require 
the `--enable-operations` feature flag.[1][2]

# Behavior

Operation requests start without observed XR state. They use required resources, optional input and credentials, and pipeline context. Desired state accumulates across steps; Crossplane applies the resources produced by 
the pipeline without adding owner references.[3][4]

Each referenced Function must declare the `operation` capability. A package may declare both `operation` and `composition` when it supports both roles.[5]

An `Operation` pipeline has 1–99 uniquely named steps. Status records applied resource references, conditions, failure count, and per-step outputs; `retryLimit` bounds permitted failures before further retries stop.[6]

# Invocation

- Create an `Operation` to run a pipeline directly.
- A [CronOperation](scheduled-and-watched-operations.md) creates Operations from a template on a cron schedule.
- A [WatchOperation](scheduled-and-watched-operations.md) creates Operations when selected Kubernetes resources change.

# Limitations

Operation functions can output arbitrary Kubernetes resources and Crossplane force-applies them without ownership. Authors must account for conflicts with other field managers and for cleanup, because the Operation does 
not own those resources.[4]

# Citations

[1] [Alpha Operation identity and API](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L7-L36)
[2] [Once-to-completion model and feature flag](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L1-L49)
[3] [Operation request construction and state chaining](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L182-L299)
[4] [Output resource application](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L347-L389) and [documented ownership 
semantics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L76)
[5] [Operation capability enforcement](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L86-L178)
[6] [Operation pipeline, retry, and status schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L68-L341)
