---
type: Crossplane Test Tool
title: Regenerate xprin golden files with update-goldens
description: Use xprin update-goldens, available since xprin v0.3.0, to write current render output to the expected files of diff and dyff assertions.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, composition, golden-files, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T22:30:00Z" }
sources:
  - id: update-goldens-command
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/main.go#L42'
    title: 'update-goldens subcommand registration'
  - id: update-goldens-flags
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L35-L41'
    title: 'update-goldens arguments and flags'
  - id: update-goldens-options
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L77-L98'
    title: 'update-goldens options'
  - id: skip-without-golden-assertions
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L224-L228'
    title: 'Test cases without golden assertions are skipped'
  - id: stop-after-render
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L695-L697'
    title: 'update-goldens stops after render'
  - id: golden-writes
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/update_goldens.go#L27-L76'
    title: 'Golden file writes for diff and dyff entries'
  - id: golden-writes-tests
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/update_goldens_test.go#L39-L135'
    title: 'update-goldens runner tests'
  - id: update-goldens-flow-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L596-L628'
    title: 'update-goldens flow documentation'
  - id: update-goldens-guidance
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/getting-started.md#L98-L123'
    title: 'Bootstrapping golden files guidance'
  - id: v0-3-0-update-goldens
    resource: 'https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/cmd/xprin/main.go#L42'
    title: 'xprin v0.3.0 registers update-goldens'
source_repository: crossplane-contrib/xprin
source_tag: v0.5.0
source_commit: eb5d7131c596e9a5663da349149184d54d704f42
source_paths: [cmd/xprin/main.go, cmd/xprin/updategoldens/update_goldens.go, internal/testexecution/runner/runner.go, internal/testexecution/runner/update_goldens.go, internal/testexecution/runner/update_goldens_test.go, docs/how-it-works.md, docs/getting-started.md]
introduced_in: v0.3.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither the command nor its documentation Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

`xprin update-goldens` regenerates the expected files used by `assertions.diff`
and `assertions.dyff`.[^update-goldens-command][^update-goldens-flags] It is
available since xprin v0.3.0.[^v0-3-0-update-goldens] The project documents it for bootstrapping golden
files and for regenerating them after a Composition change, then committing them
as the baseline that `xprin test` compares against.[^update-goldens-guidance]

# Usage

```shell
xprin update-goldens tests/...
```

The example is adapted from the documented target forms.[^update-goldens-flags][^update-goldens-guidance]

Targets are suite files, directories, or recursive `dir/...` paths, as for
`xprin test`. At v0.5.0 the command accepts `-v`, `-q`, `--debug`,
`--color`, `--crossplane-version`, and `--no-container-reuse`, the last added
after v0.3.0; it has no `--show-*` flags and no artifact export.[^update-goldens-flags][^update-goldens-options]

# Behavior

- A test case with no `diff` or `dyff` assertion is skipped.[^skip-without-golden-assertions][^update-goldens-flow-docs]
- Setup, pre-test hooks, XR patching, and render run as in `xprin test`. Validation,
  all assertions, and post-test hooks do not run.[^stop-after-render][^update-goldens-flow-docs]
- For each `diff` entry and then each `dyff` entry, the render output is written
  to the entry's `expected` path, relative to the suite file. Without
  `resource`, the full render is written; with `resource: Kind/name`, only that
  resource is written, and a missing resource fails the test
  case.[^golden-writes][^golden-writes-tests]
- Each written file is reported as a `written:` line.[^update-goldens-flow-docs]
- `xprin` field, count, and existence assertions are neither evaluated nor
  written.[^stop-after-render][^golden-writes]

# Limitations

- The command overwrites expected files with current output, so review the diff
  before committing; it does not decide whether the new output is correct.
  Inferred from the unconditional write.[^golden-writes]
- The selected sources do not show missing parent directories of an `expected`
  path being created. Treat that case as unresolved.[^golden-writes]
- The project documentation's flow also covers converting legacy Claim inputs;
  that path is excluded from this catalog.

# Relationships

- [xprin test suites](xprin-test-suites.md) describes the suites and
  assertions that consume these golden files.

[^update-goldens-command]: [update-goldens subcommand registration](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/main.go#L42)
[^update-goldens-flags]: [update-goldens arguments and flags](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L35-L41)
[^update-goldens-options]: [update-goldens options](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L77-L98)
[^skip-without-golden-assertions]: [Test cases without golden assertions are skipped](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L224-L228)
[^stop-after-render]: [update-goldens stops after render](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L695-L697)
[^golden-writes]: [Golden file writes for diff and dyff entries](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/update_goldens.go#L27-L76)
[^golden-writes-tests]: [update-goldens runner tests](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/update_goldens_test.go#L39-L135)
[^update-goldens-flow-docs]: [update-goldens flow documentation](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L596-L628)
[^update-goldens-guidance]: [Bootstrapping golden files guidance](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/getting-started.md#L98-L123)
[^v0-3-0-update-goldens]: [xprin v0.3.0 registers update-goldens](https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/cmd/xprin/main.go#L42)
