---
type: Crossplane Test Tool
title: Pin the Crossplane version in xprin runs
description: Use the xprin --crossplane-version flag, available since xprin v0.3.0, to pin the Crossplane image tag that render and validation use.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, cli, xprin, reproducibility]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T23:15:00Z" }
sources:
  - id: test-crossplane-version-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L46'
    title: 'xprin test --crossplane-version flag'
  - id: update-goldens-crossplane-version-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L40'
    title: 'xprin update-goldens --crossplane-version flag'
  - id: v0-3-0-crossplane-version-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/cmd/xprin/test/test.go#L46'
    title: 'xprin v0.3.0 --crossplane-version flag'
  - id: render-version-arg
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L581-L586'
    title: 'Render receives --crossplane-version on supporting CLIs'
  - id: render-version-tier
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L40-L45'
    title: 'CLI tiers and --crossplane-version support'
  - id: validate-image-arg
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L701-L709'
    title: 'Validation receives --crossplane-image'
  - id: update-goldens-stops-after-render
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L695-L697'
    title: 'update-goldens stops after render'
  - id: legacy-cli-debug-message
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L99-L107'
    title: 'Debug message on CLIs without render version support'
  - id: crossplane-version-tests
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test_test.go#L198-L240'
    title: '--crossplane-version tests'
  - id: e2e-render-and-validate-args
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/tests/e2e/expected/testcase_012.output#L38-L40'
    title: 'End-to-end render and validate arguments'
source_repository: crossplane-contrib/xprin
source_tag: v0.5.0
source_commit: eb5d7131c596e9a5663da349149184d54d704f42
source_paths: [cmd/xprin/test/test.go, cmd/xprin/updategoldens/update_goldens.go, internal/testexecution/runner/runner.go, internal/xpcli/tier.go, cmd/xprin/test/test_test.go, tests/e2e/expected/testcase_012.output]
introduced_in: v0.3.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither the flag nor its help text Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

`xprin test` and `xprin update-goldens` accept `--crossplane-version`, the
version of the Crossplane controller image to use.[^test-crossplane-version-flag][^update-goldens-crossplane-version-flag]
`xprin test` has had it since v0.3.0.[^v0-3-0-crossplane-version-flag] The flag
has no default; when it is empty, xprin adds nothing and the Crossplane CLI's
own defaults apply.[^render-version-arg][^validate-image-arg]

```shell
xprin test --crossplane-version=v2.4.2 tests/...
```

The example is illustrative. xprin uses the value verbatim as an image tag and
does not normalize it.[^validate-image-arg]

# Behavior

- **Render.** xprin appends `--crossplane-version=<value>` to `crossplane render`
  only when the detected CLI is v2.3.0 or later.[^render-version-arg][^render-version-tier]
- **Validation.** When a test case supplies CRDs, xprin appends
  `--crossplane-image=xpkg.crossplane.io/crossplane/crossplane:<value>` to the
  validate command on every CLI tier.[^validate-image-arg][^e2e-render-and-validate-args]
- **CLIs before v2.3.0.** Before CLI v2.3.0 the render argument is skipped and only
  validation is pinned; with `--debug`, `xprin test` says so.[^legacy-cli-debug-message][^crossplane-version-tests]
- **update-goldens.** It stops after render, so the flag affects render
  only.[^update-goldens-crossplane-version-flag][^update-goldens-stops-after-render]

# Limitations

- The flag is described only in the CLI help, not in the project documentation.
- What the render-side flag does inside the Crossplane CLI is CLI behavior and
  is not established by xprin's sources.
- xprin's tests do not show that `beta validate` on CLIs before v2.3.0 accepts
  `--crossplane-image`. Treat that case as unresolved.

# Relationships

- [xprin test suites](xprin-test-suites.md) describes the runs this flag pins.
- [Render a Composition locally](../cli/local-composition-rendering.md)
  describes the CLI's own `--crossplane-image` handling for validation.

[^test-crossplane-version-flag]: [xprin test --crossplane-version flag](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L46)
[^update-goldens-crossplane-version-flag]: [xprin update-goldens --crossplane-version flag](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L40)
[^v0-3-0-crossplane-version-flag]: [xprin v0.3.0 --crossplane-version flag](https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/cmd/xprin/test/test.go#L46)
[^render-version-arg]: [Render receives --crossplane-version on supporting CLIs](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L581-L586)
[^render-version-tier]: [CLI tiers and --crossplane-version support](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L40-L45)
[^validate-image-arg]: [Validation receives --crossplane-image](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L701-L709)
[^update-goldens-stops-after-render]: [update-goldens stops after render](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L695-L697)
[^legacy-cli-debug-message]: [Debug message on CLIs without render version support](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L99-L107)
[^crossplane-version-tests]: [--crossplane-version tests](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test_test.go#L198-L240)
[^e2e-render-and-validate-args]: [End-to-end render and validate arguments](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/tests/e2e/expected/testcase_012.output#L38-L40)
