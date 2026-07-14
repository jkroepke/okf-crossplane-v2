---
type: function
title: function-auto-ready CEL health checks
description: Alpha, feature-gated readiness expressions evaluated against observed composed resources.
resource: https://github.com/crossplane-contrib/function-auto-ready
tags: [crossplane, function, cel, readiness, alpha]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths: [README.md, features/features.go, cel/resolver.go, fn.go]
release: v0.7.0
feature_state: Alpha
feature_state_basis: CELHealthcheckCustomizations is explicitly registered as Alpha and disabled by default.
---

# Overview

Enable the `CELHealthcheckCustomizations` Alpha feature gate to define per-GVK readiness expressions. It is disabled by default.[1]

Rule keys use `<group>_<version>_<kind>`, replacing dots in the group with underscores. Each expression receives the observed
resource as `object` and must return a Boolean. `true` sets explicit `Ready=True`; `false` sets explicit `Ready=False`.[2]

# Sources and precedence

Rules may come from the request context field path named by `celHealthCheckCustomizationFrom`, the inline `celHealthCheckCustomization` map, or both. Context rules load first; inline entries overwrite matching keys.[3]

The bundled example reads rules from an EnvironmentConfig-populated context and checks that a Crossplane Configuration reports both `Installed=True` and `Healthy=True`. This catalog summarizes the example; it does not copy it.[4]

# Limitations

The README says an evaluation error is treated as not ready and that a customization takes precedence over a built-in check.
The implementation instead emits a Warning and leaves readiness unspecified after an error, allowing later built-in or generic
fallback stages to mark the resource ready. Runtime behavior here follows the implementation.[5][6]

The README's CEL snippets use `v1alpha1`, conflicting with the selected [v1beta1 Input](input.md). Use the schema-backed `v1beta1` API.[7]

# Citations

[1] [Alpha feature gate](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/features/features.go#L7-L18)
[2] [CEL key, type, and readiness mapping](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L23-L71)
[3] [Context and inline merge order](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L100)
[4] [Bundled CEL example](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/README.md#L14-L64)
[5] [README error and precedence description](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L85-L91)
[6] [Runtime error fallthrough](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L119-L159)
[7] [README v1alpha1 snippets](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/README.md#L100-L129)
