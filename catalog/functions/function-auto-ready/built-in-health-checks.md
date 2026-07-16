---
type: reference
title: function-auto-ready built-in health checks
description: Kubernetes resource-specific readiness checks registered by function-auto-ready v0.7.0.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, kubernetes, readiness]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [README.md, healthchecks]
release: v0.7.0
feature_state: Not stated by selected sources
---

# Behavior

The selected release registers specialized checks for 15 Kubernetes resource kinds.[1]

| Resource | Ready when |
|---|---|
| ConfigMap, Namespace, Secret, ServiceAccount | The resource exists in observed state. |
| Pod | Phase is `Succeeded`, or phase is `Running`, restart policy is `Always`, and condition `Ready=True`. |
| Service | It is not type `LoadBalancer`, or it has at least one load-balancer ingress entry. |
| PersistentVolumeClaim | Phase is `Bound`. |
| Deployment | Desired replicas equal updated and available replicas, with condition `Available=True`. |
| StatefulSet | Desired replicas equal ready and current replicas, and current revision equals update revision. |
| DaemonSet | Desired scheduled pods equal ready, updated, and available counts. |
| ReplicaSet | Observed generation is current, no true replica-failure condition exists, and available replicas meet desired replicas. |
| Job | Condition `Complete=True`, unless a true failed or suspended condition is encountered first. |
| CronJob | It is suspended, has an active job, or its last successful time is at or after its last schedule time. |
| HorizontalPodAutoscaler | A true `ScalingActive` or `ScalingLimited` condition is encountered without an earlier recognized failure-like condition. |
| Ingress | It has at least one load-balancer ingress entry. |

The README provides the inventory, while the resource-specific implementations establish exact rules.[2][3][4][5][6]

The built-in Secret rule establishes existence only. It does not check for
required data keys or prove that a producer is ready. When credential
completeness gates the XR contract, set explicit readiness in an earlier step
using the [strict connection publication pattern](../function-go-templating/patterns/safe-status-and-connection-publication.md);
function-auto-ready preserves explicit readiness.[7]

# Limitations

Maturity of these implementation-provided checks is **Not stated by selected
sources**.

Resources without a registered check use the generic `Ready=True` condition fallback. A specialized check returning false also leaves readiness unspecified and does not prevent that fallback.[8]

# Citations

[1] [Registered health checks](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L58-L74)
[2] [README health-check inventory](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L15-L68)
[3] [Pod implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/pod.go#L18-L66)
[4] [Deployment implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/deployment.go#L17-L73)
[5] [Job implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/job.go#L18-L45)
[6] [HPA implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/horizontalpodautoscaler.go#L18-L50)
[7] [Secret registers the existence-only check](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/secret.go#L7-L13), [`alwaysReady` returns true](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L27-L32), and [earlier explicit readiness is preserved](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[8] [Built-in and fallback ordering](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L193)
