---
type: function
title: function-go-templating response TTL
description: Set the response TTL that function-go-templating v0.13.0 returns to Crossplane through a flag, the input, or an XR annotation.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, ttl, caching]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T19:30:00Z" }
sources:
  - id: ttl-input-field
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/input/v1beta1/input.go#L32-L35'
    title: 'GoTemplate ttl field'
  - id: ttl-generated-crd
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L90-L98'
    title: 'Generated CRD ttl property and served version'
  - id: ttl-flag
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L21'
    title: 'ttl flag definition'
  - id: ttl-flag-parsing
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L34-L45'
    title: 'ttl flag parsed at startup'
  - id: ttl-flag-default
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L53-L58'
    title: 'ttl flag default from the SDK'
  - id: sdk-default-ttl
    resource: 'https://github.com/crossplane/function-sdk-go/blob/176ccd5428a608f823c8c7562ffb090ca2c166d5/response/response.go#L34-L48'
    title: 'function-sdk-go v0.7.1 DefaultTTL and response.To'
  - id: ttl-annotation-key
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L61-L64'
    title: 'ttl annotation key'
  - id: ttl-flag-and-input-precedence
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L78-L96'
    title: 'Flag TTL and input override'
  - id: ttl-annotation-override
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L220-L229'
    title: 'Observed-XR annotation override'
  - id: ttl-tests
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1995-L2072'
    title: 'CustomInputTtl and CustomAnnotationTtl tests'
  - id: v0-12-4-fixed-ttl
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/fe17e68927afd64046232f39a2376e87b45e2f58/fn.go#L68'
    title: 'v0.12.4 fixed default TTL'
  - id: response-ttl-meaning
    resource: 'https://github.com/crossplane/function-sdk-go/blob/176ccd5428a608f823c8c7562ffb090ca2c166d5/proto/v1/run_function.proto#L274-L277'
    title: 'ResponseMeta ttl semantics'
  - id: core-pipeline-ttl
    resource: 'https://github.com/crossplane/crossplane/blob/bf8ffd4048a0bb1b408b8b745e31960c717009cb/internal/controller/apiextensions/composite/composition_functions.go#L471-L476'
    title: 'Crossplane v2.4.2 pipeline TTL selection'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.13.0
source_commit: 9b7ea49394a7cef38fe517d2b60f55d64c4c8511
source_paths: [input/v1beta1/input.go, package/input/gotemplating.fn.crossplane.io_gotemplates.yaml, main.go, fn.go, fn_test.go]
supporting_source_repository: crossplane/function-sdk-go
supporting_source_tag: v0.7.1
supporting_source_commit: 176ccd5428a608f823c8c7562ffb090ca2c166d5
supporting_source_paths: [response/response.go, proto/v1/run_function.proto]
crossplane_release: v2.4.2
crossplane_source_commit: bf8ffd4048a0bb1b408b8b745e31960c717009cb
crossplane_source_paths: [internal/controller/apiextensions/composite/composition_functions.go]
feature_state: Beta (ttl input field); Not stated by selected sources (flag and annotation)
feature_state_basis: The ttl field belongs to the only served GoTemplate version, gotemplating.fn.crossplane.io/v1beta1. The flag and annotation are unlabelled implementation behavior.
---

# Overview

A function response carries a TTL. Crossplane calls the function again when it
expires and may cache the response until then.[^response-ttl-meaning]
Crossplane v2.4.2 uses the smallest non-zero TTL returned by any pipeline step
and ignores a zero TTL.[^core-pipeline-ttl]

The previously locked v0.12.4 release always returned the SDK default TTL
and had no TTL setting.[^v0-12-4-fixed-ttl] v0.13.0 makes it configurable in three places.[^ttl-tests]

# Settings

| Setting | Where | Behavior |
|---|---|---|
| `--ttl` | Function process flag | Go duration string. Defaults to function-sdk-go's `DefaultTTL`, one minute. It is parsed at startup, and an invalid value stops the function from starting.[^ttl-flag][^ttl-flag-parsing][^ttl-flag-default][^sdk-default-ttl] |
| `ttl` | GoTemplate input | Optional Go duration string with a generated CRD default of `1m0s` and no format validation. A non-empty value that parses replaces the flag value. An unparseable value is ignored, and the flag value stays in effect.[^ttl-input-field][^ttl-generated-crd][^ttl-flag-and-input-precedence] |
| `gotemplating.fn.crossplane.io/ttl` | Annotation on the observed composite resource | Replaces both the flag and the input value.[^ttl-annotation-key][^ttl-annotation-override] |

The tests confirm the order: input `20m` yields 20 minutes, and an XR annotation
of `5m` over input `20m` yields 5 minutes.[^ttl-tests]

# Behavior notes

- The annotation is read only after templates render and the observed and
  desired state are read. A response that fails earlier keeps the flag or input
  value (inferred from the order of early returns).[^ttl-annotation-override]
- The function removes the annotation only from its in-memory copy of the
  observed XR and passes the desired composite through unchanged; the test
  expects the desired composite to keep it.[^ttl-annotation-override][^ttl-tests]
- An unparseable annotation value sets the response TTL to zero. The code logs
  "Ignoring Ttl annotation, wrong format" at debug level but still assigns the
  zero duration that parsing returns. No test covers this case, so it is read
  from the code only.[^ttl-annotation-override] Crossplane v2.4.2 then ignores
  this step's TTL rather than refreshing immediately (inferred by combining the
  two sources).[^core-pipeline-ttl]

# Limitations

- The README and examples do not document the TTL settings. The selected
  sources do not show how to pass `--ttl` to an installed Function package.
- Whether Crossplane applies the CRD default `1m0s` to inline Composition
  input is unresolved. It matters only when `--ttl` is changed: an omitted
  `ttl` then uses the flag value only if the default is not applied.[^ttl-generated-crd][^ttl-flag-and-input-precedence]
- The `ttl` field is Beta because GoTemplate serves only `v1beta1`. The
  maturity of the flag and annotation is **Not stated by selected sources**.

# Relationships

The field extends the [GoTemplate input](input.md). The annotation sits beside
the readiness and resource-name annotations described in
[rendered output](rendered-output.md). See [package and installation](package.md)
for the Function package. Crossplane's use of the pipeline TTL is covered in
[realtime composition reconciliation](../../core/realtime-composition-reconciliation.md)
and the [composition function specification](../composition-function-specification.md).

[^ttl-input-field]: [GoTemplate `ttl` field](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/input/v1beta1/input.go#L32-L35)
[^ttl-generated-crd]: [Generated CRD `ttl` property and served version](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L90-L98)
[^ttl-flag]: [`--ttl` flag definition](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L21)
[^ttl-flag-parsing]: [`--ttl` parsed at startup](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L34-L45)
[^ttl-flag-default]: [`--ttl` default from the SDK](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L53-L58)
[^sdk-default-ttl]: [function-sdk-go v0.7.1 `DefaultTTL` and `response.To`](https://github.com/crossplane/function-sdk-go/blob/176ccd5428a608f823c8c7562ffb090ca2c166d5/response/response.go#L34-L48)
[^ttl-annotation-key]: [`ttl` annotation key](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L61-L64)
[^ttl-flag-and-input-precedence]: [Flag TTL and input override](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L78-L96)
[^ttl-annotation-override]: [Observed-XR annotation override](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L220-L229)
[^ttl-tests]: [`CustomInputTtl` and `CustomAnnotationTtl` tests](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1995-L2072)
[^response-ttl-meaning]: [`ResponseMeta` `ttl` semantics](https://github.com/crossplane/function-sdk-go/blob/176ccd5428a608f823c8c7562ffb090ca2c166d5/proto/v1/run_function.proto#L274-L277)
[^core-pipeline-ttl]: [Crossplane v2.4.2 pipeline TTL selection](https://github.com/crossplane/crossplane/blob/bf8ffd4048a0bb1b408b8b745e31960c717009cb/internal/controller/apiextensions/composite/composition_functions.go#L471-L476)
[^v0-12-4-fixed-ttl]: [v0.12.4 fixed default TTL](https://github.com/crossplane-contrib/function-go-templating/blob/fe17e68927afd64046232f39a2376e87b45e2f58/fn.go#L68)
