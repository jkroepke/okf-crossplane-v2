---
type: example
title: EnvironmentConfig, Go templating, and readiness pipeline
description: Evidence-backed ordering and data flow across function-environment-configs, function-go-templating, and function-auto-ready.
resource: https://github.com/crossplane-contrib/function-auto-ready/tree/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck
tags: [crossplane, composition, environment-config, go-template, readiness]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-auto-ready
source_commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
source_paths:
  - example/cel-healthcheck/composition.yaml
  - example/cel-healthcheck/extra-resources.yaml
supporting_source_repositories:
  - crossplane-contrib/function-environment-configs
  - crossplane-contrib/function-go-templating
feature_state: Alpha
feature_state_basis: The full pattern uses function-auto-ready CELHealthcheckCustomizations, which is explicitly Alpha and disabled by default.
---

# Data flow

The three functions have separate responsibilities and must be ordered by their data dependencies:

1. `function-environment-configs` selects Beta `EnvironmentConfig` objects and writes the merged map to `apiextensions.crossplane.io/environment`.
2. `function-go-templating` reads the map directly or loads template text with `source: Environment`, then produces desired composed resources and may publish Alpha Context updates.
3. `function-auto-ready` evaluates desired resources against their observed counterparts. Its optional Alpha CEL feature may also load rules from the environment context.[1][2][3]

The selected auto-ready example uses the order go-templating →
environment-configs → auto-ready because the template is inline and does not
consume the environment. If template text or rendering data comes from an
EnvironmentConfig, environment-configs must instead precede go-templating.
Auto-ready remains last because it consumes the desired resource and optional
context produced earlier.[1][4]

# Environment-supplied CEL rules

The current example stores a Configuration readiness expression at:

`data.celHealthCheckCustomizations.pkg.crossplane.io_v1_Configuration`

Auto-ready reads it with:

`[apiextensions.crossplane.io/environment].celHealthCheckCustomizations`

The rule requires the observed package to have `Installed=True` and `Healthy=True`.[1][5]

# Adaptation boundary

This page summarizes repository-owned Apache-2.0 examples; it does not reproduce a complete manifest set.

- The auto-ready v0.7.0 CEL example uses current `EnvironmentConfig/v1beta1` and `Input/v1beta1` and is the preferred basis for the readiness integration.[1][5]
- The go-templating environment example demonstrates Environment source and
  all three functions, but pins older function packages, uses
  `EnvironmentConfig/v1alpha1`, includes legacy XRD `connectionSecretKeys`, and
  configures local Development runtime. Do not apply it unchanged.[6]
- A v2 adaptation should use current namespaced or cluster-scoped v2 XR semantics, current function tags, `EnvironmentConfig/v1beta1`, and matching Function object names.

# Citations

[1] [Current auto-ready three-function composition](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/composition.yaml#L10-L48)
[2] [function-environment-configs context output](https://github.com/crossplane-contrib/function-environment-configs/blob/5589092483aea1d65b9988f5116106585c4b516b/fn.go#L101-L134)
[3] [function-go-templating Environment loader](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/template.go#L103-L122)
[4] [auto-ready desired and observed resource ordering](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L81-L119)
[5] [Current v1beta1 EnvironmentConfig CEL rule](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/example/cel-healthcheck/extra-resources.yaml#L1-L7)
[6] [Older go-templating environment pipeline snapshot](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/environment/composition.yaml#L1-L36)
