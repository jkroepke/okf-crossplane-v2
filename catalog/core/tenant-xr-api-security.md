---
type: Crossplane Development Guide
title: Tenant XR API and admission security
description: Organization-specific API-group and tenant-namespace hardening guidance for human-orderable composite resources.
resource: https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/
tags: [crossplane, core, xrd, security, rbac, tenancy, admission]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
source_repository: kubernetes/website
source_commit: be897babb9149b808e2ab8ed5367e5d0651b3dca
feature_state: Stable by repository default
---

# Organization convention

For fictional, human-orderable composite resources owned by one team, use one
API group: `apigroup.example.com`. This permits a single Role or ClusterRole
rule, and therefore a single binding, to grant that team's selected XR
resources and verbs. Kubernetes RBAC scopes a rule by API group, resource, and
verb; grant explicit resources and verbs rather than wildcards.[1]

This is local organizational guidance, not a Kubernetes or Crossplane
requirement. It applies only to fictional examples; do not rename real APIs.
An API proxy or network boundary that exposes only `/apis/apigroup.example.com`
is a deployment-specific defence-in-depth control, not an RBAC guarantee.

# Tenant namespace baseline

Treat a tenant namespace as a boundary with several independent controls:

- namespace-scoped RBAC for the tenant's XR APIs;
- a ResourceQuota such as `count/pods: 0` when tenant workloads must not create
  Pods directly;
- default-deny ingress and egress NetworkPolicies, then narrow explicit allow
  policies; and
- admission validation for relationships that the XR schema alone cannot see.

These controls complement rather than replace [XRD schema validation](xrd-cel-validation.md).

# Admission layering

Prefer OpenAPI and XRD CEL validation for object-local invariants. For dynamic
rules that depend on namespace labels, use either Kyverno or Kubernetes native
`ValidatingAdmissionPolicy` (VAP). VAP is Stable since Kubernetes v1.30 and
exposes `namespaceObject` for namespaced admission requests; it is null for
cluster-scoped requests.[2]

For new Kyverno-specific policy material, use its Stable
`policies.kyverno.io/v1` `ValidatingPolicy`; its documented extensions include
external data and exceptions beyond native VAP. Kyverno also supports reading
`namespaceObject` labels in CEL. Exclude Crossplane controller identities from
matching Kyverno rules to skip rule evaluation, and scope matching/webhooks if
reducing admission traffic matters.[3][4]

For example, a VAP variable can read a tenant's cloud-account label. Complete
the condition with the comparison appropriate for the XR; the expression below
only derives the label value.

```yaml
variables:
  - name: securityLevel
    expression: >-
      namespaceObject.?metadata.labels[
        'platform.example.com/aws-cloud-account'
      ].orValue('')
```

Use equivalent labels for Azure subscriptions or OpenStack tenants. The
official VAP examples establish namespace-label lookup and use of variables in
validation expressions.[3]

# Controller exclusions and cost

`matchConditions` run before the remaining policy expressions; if any returns
false, the policy is skipped. Adapt the following exclusion to the actual
service accounts in your Crossplane installation:

```yaml
matchConditions:
  - name: exclude-crossplane-controllers
    expression: >-
      !request.userInfo.username.startsWith(
        "system:serviceaccount:crossplane-system:crossplane"
      ) &&
      !request.userInfo.username.startsWith(
        "system:serviceaccount:crossplane-system:provider-"
      )
```

For one known service account, exact equality is narrower and easier to audit.
The prefix form avoids the policy body for Crossplane and provider controller
requests, but can exclude an unintended account if the prefix is too broad.
Do not use an `authorizer.check()` exclusion merely to optimize this path: the
Kubernetes CEL library cautions that authorization checks can be expensive,
especially with webhook authorization.[5]

# Citations

[1] [Kubernetes RBAC rule scope and least-privilege guidance](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/reference/access-authn-authz/rbac.md#L226-L253)
[2] [VAP stability and `namespaceObject`](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/docs/reference/access-authn-authz/validating-admission-policy.md#L12-L14)
[3] [VAP namespace-label variable example](https://github.com/kubernetes/website/blob/be897babb9149b808e2ab8ed5367e5d0651b3dca/content/en/examples/access/image-matches-namespace-environment.policy.yaml#L17-L28)
[4] [Kyverno ValidatingPolicy and namespace-label CEL](https://github.com/kyverno/website/blob/e8d76c57e95060e61a8e864178862747a3a693fb/src/content/docs/docs/policy-types/validating-policy.mdx#L11-L51) and [Kyverno webhook scoping](https://github.com/kyverno/website/blob/e8d76c57e95060e61a8e864178862747a3a693fb/src/content/docs/docs/installation/customization.md#L562-L584)
[5] [VAP match-condition evaluation order](https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/api/admissionregistration/v1/types.go#L258-L292) and [CEL authorizer cost note](https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/apiserver/pkg/cel/library/authz.go#L147-L154)
