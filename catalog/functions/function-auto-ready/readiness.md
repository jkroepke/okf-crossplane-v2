---
type: function
title: function-auto-ready readiness behavior
description: The ordered rules function-auto-ready v0.7.0 uses to determine composed-resource readiness.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, readiness]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [fn.go, fn_test.go]
release: v0.7.0
feature_state: Not stated by selected sources
---

# Behavior

The function evaluates only desired composed resources that have an observed resource under the same request resource-name key. It preserves `Ready=True` or `Ready=False` set by an earlier pipeline function.[1]

For resources whose readiness remains unspecified, evaluation proceeds in this order:

1. When the Alpha CEL feature is enabled and a rule matches the observed resource GVK, a successful Boolean result sets explicit readiness.[2]
2. A registered [built-in Kubernetes health check](built-in-health-checks.md) sets `Ready=True` when it succeeds.[3]
3. A remaining resource becomes ready when its observed object has a `Ready` condition with status `True`.[4]

A failed built-in check does not set `Ready=False`; it leaves readiness unspecified, so the generic condition fallback still runs. An unobserved desired resource also remains unspecified.[3][4]

The implementation matches resources by the desired and observed maps supplied in the Function request. It does not inspect composition-resource-name annotations itself.[1]

# Limitations

Maturity of the built-in implementation behavior is **Not stated by selected
sources**. The optional CEL branch remains explicitly Alpha.

The function writes desired composed-resource readiness. The README's statement that Crossplane considers an XR ready after all desired resources are ready describes downstream Crossplane behavior, not behavior implemented here.[5]

CEL receives only the matched observed composed resource as `object`; it does
not directly evaluate a separate ExtraResources result.[6] When readiness
depends on a controller-created non-composed object, use an earlier
[function-go-templating non-composed-resource readiness pattern](../function-go-templating/patterns/non-composed-resource-readiness.md).

# Citations

[1] [Desired and observed resource matching](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L102-L119) and [explicit-readiness preservation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[2] [CEL evaluation stage](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L130)
[3] [Built-in health-check stage](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L159)
[4] [Generic Ready-condition fallback](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L161-L193)
[5] [README readiness overview](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L4-L13)
[6] [CEL activation contains only the observed object](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71)
