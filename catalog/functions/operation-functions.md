---
type: concept
title: Operation functions
description: Alpha functions that run once-to-completion operational pipelines directly, on a schedule, or after watched-resource changes.
resource: https://docs.crossplane.io/v2.3/operations/operation/
tags: [crossplane, operation-functions, operations, alpha]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: alpha-operation-identity-and-api
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L7-L36'
    title: 'Alpha Operation identity and API'
  - id: once-to-completion-model-and-feature-flag
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L1-L49'
    title: 'Once-to-completion model and feature flag'
  - id: operation-request-construction-and-state-chaining
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L182-L299'
    title: 'Operation request construction and state chaining'
  - id: output-resource-application
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L347-L389'
    title: 'Output resource application'
  - id: documented-ownership-semantics
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L76'
    title: 'documented ownership semantics'
  - id: operation-capability-enforcement
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L86-L178'
    title: 'Operation capability enforcement'
  - id: operation-pipeline-retry-and-status-schema
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L68-L341'
    title: 'Operation pipeline, retry, and status schema'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/ops.crossplane.io_operations.yaml
  - internal/controller/ops/operation/reconciler.go
---

# Overview

An operation function runs in an `Operation` pipeline once to completion instead of continuously reconciling an XR. Operation APIs are served as `ops.crossplane.io/v1alpha1`, explicitly documented as Alpha, and require 
the `--enable-operations` feature flag.[^alpha-operation-identity-and-api][^once-to-completion-model-and-feature-flag]

# Behavior

Operation requests start without observed XR state. They use required resources, optional input and credentials, and pipeline context. Desired state accumulates across steps; Crossplane applies the resources produced by 
the pipeline without adding owner references.[^operation-request-construction-and-state-chaining][^output-resource-application][^documented-ownership-semantics]

Each referenced Function must declare the `operation` capability. A package may declare both `operation` and `composition` when it supports both roles.[^operation-capability-enforcement]

An `Operation` pipeline has 1–99 uniquely named steps. Status records applied resource references, conditions, failure count, and per-step outputs; `retryLimit` bounds permitted failures before further retries stop.[^operation-pipeline-retry-and-status-schema]

# Invocation

- Create an `Operation` to run a pipeline directly.
- A [CronOperation](scheduled-and-watched-operations.md) creates Operations from a template on a cron schedule.
- A [WatchOperation](scheduled-and-watched-operations.md) creates Operations when selected Kubernetes resources change.

# Limitations

Operation functions can output arbitrary Kubernetes resources and Crossplane force-applies them without ownership. Authors must account for conflicts with other field managers and for cleanup, because the Operation does 
not own those resources.[^output-resource-application][^documented-ownership-semantics]

[^alpha-operation-identity-and-api]: [Alpha Operation identity and API](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L7-L36)
[^once-to-completion-model-and-feature-flag]: [Once-to-completion model and feature flag](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L1-L49)
[^operation-request-construction-and-state-chaining]: [Operation request construction and state chaining](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L182-L299)
[^output-resource-application]: [Output resource application](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L347-L389) and [documented ownership semantics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L76)
[^documented-ownership-semantics]: [documented ownership semantics](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L76)
[^operation-capability-enforcement]: [Operation capability enforcement](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L86-L178)
[^operation-pipeline-retry-and-status-schema]: [Operation pipeline, retry, and status schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L68-L341)
