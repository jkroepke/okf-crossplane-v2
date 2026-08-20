---
type: reference
title: function-auto-ready built-in health checks
description: Kubernetes resource-specific readiness checks registered by function-auto-ready v0.7.0.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, kubernetes, readiness]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: registered-health-checks
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L58-L74'
    title: 'Registered health checks'
  - id: readme-health-check-inventory
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L15-L68'
    title: 'README health-check inventory'
  - id: pod-implementation
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/pod.go#L18-L66'
    title: 'Pod implementation'
  - id: deployment-implementation
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/deployment.go#L17-L73'
    title: 'Deployment implementation'
  - id: job-implementation
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/job.go#L18-L45'
    title: 'Job implementation'
  - id: hpa-implementation
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/horizontalpodautoscaler.go#L18-L50'
    title: 'HPA implementation'
  - id: secret-registers-the-existence-only-check
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/secret.go#L7-L13'
    title: 'Secret registers the existence-only check'
  - id: alwaysready-returns-true
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L27-L32'
    title: 'alwaysReady returns true'
  - id: earlier-explicit-readiness-is-preserved
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179'
    title: 'earlier explicit readiness is preserved'
  - id: built-in-and-fallback-ordering
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L193'
    title: 'Built-in and fallback ordering'
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [README.md, healthchecks]
release: v0.7.0
feature_state: Not stated by selected sources
---

# Behavior

The selected release registers specialized checks for 15 Kubernetes resource kinds.[^registered-health-checks]

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

The README provides the inventory, while the resource-specific implementations establish exact rules.[^readme-health-check-inventory][^pod-implementation][^deployment-implementation][^job-implementation][^hpa-implementation]

The built-in Secret rule establishes existence only. It does not check for
required data keys or prove that a producer is ready. When credential
completeness gates the XR contract, set explicit readiness in an earlier step
using the [strict connection publication pattern](../function-go-templating/patterns/safe-status-and-connection-publication.md);
function-auto-ready preserves explicit readiness.[^secret-registers-the-existence-only-check][^alwaysready-returns-true][^earlier-explicit-readiness-is-preserved]

# Limitations

Maturity of these implementation-provided checks is **Not stated by selected
sources**.

Resources without a registered check use the generic `Ready=True` condition fallback. A specialized check returning false also leaves readiness unspecified and does not prevent that fallback.[^built-in-and-fallback-ordering]

[^registered-health-checks]: [Registered health checks](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L58-L74)
[^readme-health-check-inventory]: [README health-check inventory](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L15-L68)
[^pod-implementation]: [Pod implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/pod.go#L18-L66)
[^deployment-implementation]: [Deployment implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/deployment.go#L17-L73)
[^job-implementation]: [Job implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/job.go#L18-L45)
[^hpa-implementation]: [HPA implementation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/horizontalpodautoscaler.go#L18-L50)
[^secret-registers-the-existence-only-check]: [Secret registers the existence-only check](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/secret.go#L7-L13), [`alwaysReady` returns true](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L27-L32), and [earlier explicit readiness is preserved](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[^alwaysready-returns-true]: [`alwaysReady` returns true](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L27-L32)
[^earlier-explicit-readiness-is-preserved]: [earlier explicit readiness is preserved](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[^built-in-and-fallback-ordering]: [Built-in and fallback ordering](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L193)
