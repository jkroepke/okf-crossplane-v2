---
type: Crossplane Test Tool
title: Order xprin test cases with needs
description: Declare dependencies between xprin test cases with needs, available since xprin v0.6.0 and required since v0.7.0 for any test case that reads another test case's outputs through .Tests.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, composition, dependencies, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-11-22T14:30:00Z" }
sources:
  - id: needs-field
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/api/api.go#L84-L93'
    title: 'TestCase needs field'
  - id: needs-schema
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/data/xprin-testsuite.json#L262-L268'
    title: 'Testsuite JSON schema for needs'
  - id: needs-checks
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/discovery/check.go#L70-L91'
    title: 'Load-time checks for unknown IDs and empty needs'
  - id: needs-cycles
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/graph/graph.go#L218-L249'
    title: 'Cycle detection and execution order'
  - id: needs-skip
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/engine/needsresults.go#L21-L45'
    title: 'Skip reasons for failed or skipped needs'
  - id: needs-missing-error
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/runner/templates.go#L134-L148'
    title: 'Error for .Tests use without needs'
  - id: needs-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L406-L445'
    title: 'Dependencies between test cases'
  - id: tests-outputs-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L446-L488'
    title: 'Using the outputs of other test cases'
  - id: needs-migration-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L489-L512'
    title: 'Migrating from xprin 0.5 and earlier'
  - id: update-goldens-needs-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L596'
    title: 'update-goldens runs the test cases that golden test cases need'
  - id: needs-failure-example
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/examples/mytests/5_chained_tests/example2_needs-failure_xprin.yaml#L1-L37'
    title: 'Example: dependents of a failed test case are skipped'
  - id: v0-6-0-needs-field
    resource: 'https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/internal/api/api.go#L88'
    title: 'xprin v0.6.0 needs field'
source_repository: crossplane-contrib/xprin
source_tag: v0.7.0
source_commit: 891c1bf6de72c0978a695a02b854e15ae9a76350
source_paths: [internal/api/api.go, data/xprin-testsuite.json, internal/discovery/check.go, internal/graph/graph.go, internal/engine/needsresults.go, internal/testexecution/runner/templates.go, docs/how-it-works.md, examples/mytests/5_chained_tests/example2_needs-failure_xprin.yaml]
introduced_in: v0.6.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither needs nor the testsuite format Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API. The automatic .Tests detection that needs replaces was deprecated in v0.6.0 and removed in v0.7.0.
---

# Overview

A test case in an xprin testsuite file can list the `id`s of other test cases
of the same file in `needs`. It then runs after them, and only if they
passed.[^needs-field][^needs-docs] The field exists since xprin
v0.6.0.[^v0-6-0-needs-field]

Since xprin v0.7.0, `needs` is the only way to declare a dependency. A test
case that reads another test case's outputs through `.Tests.<id>` must list
that `id` in `needs`; otherwise it fails with `one or more test cases are used
but are not listed in needs`.[^needs-missing-error][^needs-migration-docs]

# Schema

```yaml
tests:
- name: "Create the database"
  id: db
  inputs:
    xr: db/xr.yaml
    composition: db/composition.yaml
    functions: functions.yaml

- name: "Create the app on top of the database"
  needs:
  - db
  inputs:
    xr: '{{ .Tests.db.Outputs.XR }}'
    composition: app/composition.yaml
    functions: functions.yaml
```

The example is adapted from the project's documentation.[^needs-docs][^tests-outputs-docs]

- `needs` is an optional list of strings with at least one item.[^needs-field][^needs-schema]
- Each item must be the `id` of a test case in the same file, listed before or
  after it.[^needs-checks][^needs-docs]
- A `needs` does not have to be used through `.Tests`; it can also only order
  test cases.[^needs-docs]

# Behavior

- xprin checks every file when it loads it. An unknown `id`, an empty
  `needs: []`, or a cycle makes the file invalid. Each cycle is reported as
  `needs cycle: a -> b -> a`.[^needs-checks][^needs-cycles]
- Test cases run in dependency order. When several can run, the one listed
  first runs first, so a file without `needs` runs in file
  order.[^needs-cycles][^needs-docs]
- If a needed test case failed or was skipped, the dependent test case does not
  run. It is reported as `SKIP` with one reason per needed test case, such as
  `needs failed test case "db"`, even without `-v`. The skip carries through
  every later dependent.[^needs-skip][^needs-docs][^needs-failure-example]
- A test case can read `.Tests.<id>.Outputs.*` only for the test cases it lists
  in `needs`. Those outputs are temporary and are removed when the testsuite
  file finishes.[^tests-outputs-docs]
- `xprin update-goldens` also runs any test case that a test case with golden
  assertions needs, directly or through others, so that its outputs
  exist. It writes no golden files for that test case.[^update-goldens-needs-docs]

# Migration from xprin v0.5.0

| xprin | Dependencies between test cases |
|---|---|
| v0.5.0 and earlier | Detected automatically from `.Tests` in templates; no `needs`. |
| v0.6.0 | `needs` and automatic detection both work, chosen per file: once any test case in a file lists `needs`, detection is off for that file. Detection is deprecated and prints a warning per file. |
| v0.7.0 and later | Only `needs`. `.Tests` without `needs` fails the test case. |

The table summarizes the project's migration notes.[^needs-migration-docs] The
project suggests migrating on v0.6.0, where both forms run, and checking the
files with `xprin-helpers check-testsuite-needs` before moving to
v0.7.0.[^needs-migration-docs]

# Limitations

- `needs` only reaches test cases in the same file.[^needs-checks][^needs-docs]
- xprin does not see dependencies that are not declared, such as a hook that
  relies on files another test case left behind. List them in `needs` to order
  the test cases.[^needs-docs]
- The migration notes and the reasons for removing automatic detection are xprin
  project documentation, not Crossplane behavior.[^needs-migration-docs]

# Relationships

- [xprin test suites](xprin-test-suites.md) describes the testsuite files whose
  test cases `needs` orders.
- [Export xprin test artifacts](xprin-test-artifacts-export.md) keeps a
  persistent copy of every test case; the `.Tests` outputs that `needs` exposes
  are temporary.
- [Regenerate xprin golden files](xprin-update-goldens.md) runs the needed test
  cases of golden-asserting test cases.

[^needs-field]: [TestCase needs field](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/api/api.go#L84-L93)
[^needs-schema]: [Testsuite JSON schema for needs](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/data/xprin-testsuite.json#L262-L268)
[^needs-checks]: [Load-time checks for unknown IDs and empty needs](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/discovery/check.go#L70-L91)
[^needs-cycles]: [Cycle detection and execution order](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/graph/graph.go#L218-L249)
[^needs-skip]: [Skip reasons for failed or skipped needs](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/engine/needsresults.go#L21-L45)
[^needs-missing-error]: [Error for .Tests use without needs](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/runner/templates.go#L134-L148)
[^needs-docs]: [Dependencies between test cases](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L406-L445)
[^tests-outputs-docs]: [Using the outputs of other test cases](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L446-L488)
[^needs-migration-docs]: [Migrating from xprin 0.5 and earlier](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L489-L512)
[^update-goldens-needs-docs]: [update-goldens runs the test cases that golden test cases need](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L596)
[^needs-failure-example]: [Example: dependents of a failed test case are skipped](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/examples/mytests/5_chained_tests/example2_needs-failure_xprin.yaml#L1-L37)
[^v0-6-0-needs-field]: [xprin v0.6.0 needs field](https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/internal/api/api.go#L88)
