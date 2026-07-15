---
type: pattern
title: Readiness and secret boundaries for provider-kubernetes Object wrappers
description: Choose explicit wrapper readiness and avoid treating observed wrapper status as a durable Secret store.
resource: https://github.com/crossplane-contrib/provider-kubernetes
tags: [crossplane, composition-function, provider-kubernetes, readiness, secrets]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/provider-kubernetes
source_tag: v1.2.1
source_commit: 0ea671a4dab090ff3b14877d35086f1950fa35e3
supporting_source_repository: crossplane-contrib/function-auto-ready
supporting_source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
feature_state: Alpha
feature_state_basis: The selected Object API serves kubernetes.m.crossplane.io/v1alpha1.
---

# Wrapper boundary

provider-kubernetes `Object` wraps an arbitrary Kubernetes manifest under
`spec.forProvider.manifest` and writes the observed target to
`status.atProvider.manifest`.[1] This makes it useful for composing Kubernetes
resources that do not have a dedicated Crossplane managed-resource API, but the
Object API is Alpha.[1]

# Choose readiness deliberately

The default Object readiness policy, `SuccessfulCreate`, means the target was
created or is up to date; it does not establish that an operator-managed
workload is usable.[2] Use an explicit readiness policy when XR readiness has
to represent application availability.

`DeriveFromObject` recognizes only a wrapped object's standard
`.status.conditions` entry with `type: Ready` and `status: "True"`. It is not
a general detector for arbitrary operator status conventions. Before selecting
it, verify the wrapped CR publishes that exact condition. Otherwise use a CEL
query that expresses the CR's documented status contract, or choose a different
readiness design.[2][3]

Place `function-auto-ready` after resource-rendering steps when it should
evaluate wrapper readiness. It considers only desired resources that have an
observed resource under the same composition-resource key, and preserves an
earlier explicit `Ready=True` or `Ready=False` decision.[4] Therefore an
unconditional ready annotation on an Object prevents the later function from
making a safer readiness decision.

# Secret persistence and exposure

Do not use `Object.status.atProvider.manifest` as a general password-recovery
or durable-secret mechanism. The provider can sanitize observed Kubernetes
Secret data before persisting the wrapper status, replacing it with a redacted
value. Whether status contains Secret data is therefore deployment-dependent,
and storing credentials in a readable wrapper status may itself broaden their
exposure.[5]

Generate a password only through a design that has an explicit persistence
contract. Random template functions are non-hermetic and can produce different
values for the same request; a fallback random value can churn whenever the
previous value is unavailable.[6] The exact persistence mechanism is
provider- and platform-specific. Keep consumer-facing Secret references behind
the strict publication gate described in [safe status and connection
publication](safe-status-and-connection-publication.md).

`managementPolicies` can limit Object actions, but omitting `Update` or
`Delete` does not prove that Secret contents are immutable or safely recoverable;
it only changes which lifecycle actions the provider performs.[7]

# Citations

[1] [Object desired and observed manifest fields](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/namespaced/object/v1alpha1/types.go#L78-L100)
[2] [Object default and derived readiness policies](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/namespaced/object/v1alpha1/types.go#L114-L148) and [DeriveFromObject evaluation](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L534-L599)
[3] [CEL readiness policy query activation](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/namespaced/object/v1alpha1/types.go#L129-L148)
[4] [function-auto-ready desired and observed resource matching](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L102-L119)
[5] [Observed Secret sanitization before wrapper status persistence](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L510-L531)
[6] [Sprig general versus hermetic function maps](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/functions.go#L67-L94)
[7] [Object management policy actions](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/package/crds/kubernetes.m.crossplane.io_objects.yaml#L134-L156)
