---
type: function
title: function-auto-ready readiness behavior
description: The ordered rules function-auto-ready v0.7.0 uses to determine composed-resource readiness.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, readiness]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: desired-and-observed-resource-matching
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L102-L119'
    title: 'Desired and observed resource matching'
  - id: explicit-readiness-preservation
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179'
    title: 'explicit-readiness preservation'
  - id: cel-evaluation-stage
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L130'
    title: 'CEL evaluation stage'
  - id: built-in-health-check-stage
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L159'
    title: 'Built-in health-check stage'
  - id: generic-ready-condition-fallback
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L161-L193'
    title: 'Generic Ready-condition fallback'
  - id: readme-readiness-overview
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L4-L13'
    title: 'README readiness overview'
  - id: cel-activation-contains-only-the-observed-object
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71'
    title: 'CEL activation contains only the observed object'
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [fn.go, fn_test.go]
release: v0.7.0
feature_state: Not stated by selected sources
---

# Behavior

The function evaluates only desired composed resources that have an observed resource under the same request resource-name key. It preserves `Ready=True` or `Ready=False` set by an earlier pipeline function.[^desired-and-observed-resource-matching][^explicit-readiness-preservation]

For resources whose readiness remains unspecified, evaluation proceeds in this order:

1. When the Alpha CEL feature is enabled and a rule matches the observed resource GVK, a successful Boolean result sets explicit readiness.[^cel-evaluation-stage]
2. A registered [built-in Kubernetes health check](built-in-health-checks.md) sets `Ready=True` when it succeeds.[^built-in-health-check-stage]
3. A remaining resource becomes ready when its observed object has a `Ready` condition with status `True`.[^generic-ready-condition-fallback]

A failed built-in check does not set `Ready=False`; it leaves readiness unspecified, so the generic condition fallback still runs. An unobserved desired resource also remains unspecified.[^built-in-health-check-stage][^generic-ready-condition-fallback]

The implementation matches resources by the desired and observed maps supplied in the Function request. It does not inspect composition-resource-name annotations itself.[^desired-and-observed-resource-matching][^explicit-readiness-preservation]

# Limitations

Maturity of the built-in implementation behavior is **Not stated by selected
sources**. The optional CEL branch remains explicitly Alpha.

The function writes desired composed-resource readiness. The README's statement that Crossplane considers an XR ready after all desired resources are ready describes downstream Crossplane behavior, not behavior implemented here.[^readme-readiness-overview]

CEL receives only the matched observed composed resource as `object`; it does
not directly evaluate a separate ExtraResources result.[^cel-activation-contains-only-the-observed-object] When readiness
depends on a controller-created non-composed object, use an earlier
[function-go-templating non-composed-resource readiness pattern](../function-go-templating/patterns/non-composed-resource-readiness.md).

[^desired-and-observed-resource-matching]: [Desired and observed resource matching](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L102-L119) and [explicit-readiness preservation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[^explicit-readiness-preservation]: [explicit-readiness preservation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[^cel-evaluation-stage]: [CEL evaluation stage](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L130)
[^built-in-health-check-stage]: [Built-in health-check stage](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L159)
[^generic-ready-condition-fallback]: [Generic Ready-condition fallback](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L161-L193)
[^readme-readiness-overview]: [README readiness overview](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L4-L13)
[^cel-activation-contains-only-the-observed-object]: [CEL activation contains only the observed object](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71)
