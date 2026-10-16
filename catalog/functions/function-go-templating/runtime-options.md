---
type: function
title: function-go-templating default template options and receive size
description: Set function-wide default template options and the gRPC receive-size limit for function-go-templating v0.13.0.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, configuration, template-options]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T19:45:00Z" }
sources:
  - id: runtime-flag-definitions
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L22-L24'
    title: 'Runtime flag and environment-variable definitions'
  - id: runtime-flag-wiring
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L39-L50'
    title: 'Flags passed to the function server'
  - id: option-selection
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L112-L125'
    title: 'Default and per-input option selection'
  - id: safe-option-application
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L454-L463'
    title: 'Template option panic recovery'
  - id: readme-options-and-receive-size
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/README.md#L75-L82'
    title: 'README default options and receive size'
  - id: default-option-tests
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1249-L1339'
    title: 'Per-input and default option tests'
  - id: readme-nested-options-example
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/README.md#L25-L31'
    title: 'README example with options nested beneath inline'
  - id: v0-12-2-receive-size-flag
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/main.go#L18'
    title: 'v0.12.2 receive-size flag without an environment variable'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.13.0
source_commit: 9b7ea49394a7cef38fe517d2b60f55d64c4c8511
source_paths: [main.go, fn.go, fn_test.go, README.md]
feature_state: Not stated by selected sources
feature_state_basis: Function process flags and environment variables are unlabelled implementation behavior, not a served API. The Beta state of the GoTemplate input does not transfer to them.
---

# Settings

| Flag | Environment variable | Behavior |
|---|---|---|
| `--default-options` | `FUNCTION_GO_TEMPLATING_DEFAULT_OPTIONS` | New in v0.13.0. Comma-separated Go `text/template` options used when a GoTemplate input does not set `options`. Empty by default.[^runtime-flag-definitions][^runtime-flag-wiring][^option-selection] |
| `--max-recv-message-size` | `MAX_RECV_MESSAGE_SIZE` | Maximum received gRPC message size in MB, default `4`. The flag existed in v0.12.2; v0.13.0 adds the environment variable.[^runtime-flag-definitions][^runtime-flag-wiring][^v0-12-2-receive-size-flag][^readme-options-and-receive-size] |

# Default template options

- A per-input `options` list replaces the defaults entirely; the two are not
  merged. The test with an invalid per-input option and a valid default fails
  on the per-input option.[^option-selection][^default-option-tests]
- The value is split on `,` without trimming whitespace or dropping empty
  entries.[^option-selection] An invalid option makes the function return a
  fatal "cannot apply template options" result instead of crashing.[^safe-option-application][^default-option-tests]
  Inferred from Go `text/template`: a space after a comma or a trailing comma
  produces such an invalid entry.
- With nothing configured, the README describes the effective default as
  `missingkey=default`, which renders a missing key as `<no value>`. A
  default of `missingkey=error` makes a missing key a fatal template error.[^readme-options-and-receive-size][^default-option-tests]
- Inferred: an explicit empty `options: []` is set, so it suppresses the
  defaults and applies no options.[^option-selection]

# Limitations

- The help text says defaults apply "when input is not provided", but the code
  applies them whenever the input's `options` field is unset.[^runtime-flag-definitions][^option-selection]
- The selected sources do not show how to set these flags or environment
  variables on an installed Function package, and they do not state whether a
  flag or its environment variable wins when both are set.
- The README example nests `options` beneath `inline`, while the schema
  places it at the top level (see [GoTemplate input](input.md)).[^readme-nested-options-example] Inferred: a
  mis-nested list leaves the top-level field unset, so configured defaults
  would apply instead.

# Relationships

These settings configure the function process installed through
[package and installation](package.md). They supply defaults for the
`options` field of the [GoTemplate input](input.md).

[^runtime-flag-definitions]: [Runtime flag and environment-variable definitions](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L22-L24)
[^runtime-flag-wiring]: [Flags passed to the function server](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/main.go#L39-L50)
[^option-selection]: [Default and per-input option selection](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L112-L125)
[^safe-option-application]: [Template option panic recovery](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L454-L463)
[^readme-options-and-receive-size]: [README default options and receive size](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/README.md#L75-L82)
[^default-option-tests]: [Per-input and default option tests](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn_test.go#L1249-L1339)
[^v0-12-2-receive-size-flag]: [v0.12.2 receive-size flag without an environment variable](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/main.go#L18)
[^readme-nested-options-example]: [README example with `options` nested beneath `inline`](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/README.md#L25-L31)
