---
type: Crossplane Test Tool
title: Export xprin test-case inputs and outputs with --artifacts-dir
description: Use xprin test -a or --artifacts-dir, available since xprin v0.3.0, to keep a persistent copy of every test case's inputs and outputs for inspection.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, composition, debugging, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T22:45:00Z" }
sources:
  - id: artifacts-dir-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L48'
    title: 'xprin test --artifacts-dir flag'
  - id: artifacts-dir-wiring
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L139'
    title: 'Flag passed to test options'
  - id: artifacts-dir-default
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/utils/options.go#L44-L47'
    title: 'Empty artifacts directory disables export'
  - id: artifacts-layout
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts.go#L27-L118'
    title: 'Artifact suite and test-case paths'
  - id: artifacts-run-dir
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts.go#L120-L143'
    title: 'Per-invocation run directory'
  - id: artifacts-copy
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts.go#L145-L172'
    title: 'Per-test-case inputs and outputs copy'
  - id: artifacts-run-dir-setup
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L175-L180'
    title: 'Run directory created for suites with test cases'
  - id: artifacts-announce
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L197-L200'
    title: 'Artifacts path reported per suite'
  - id: artifacts-defer
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L238-L256'
    title: 'Copy runs on every exit path before cleanup'
  - id: artifacts-tests
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts_test.go#L26-L85'
    title: 'Artifact path tests'
  - id: artifacts-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/getting-started.md#L91-L95'
    title: 'Exporting artifacts guidance'
  - id: artifacts-purpose
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L699'
    title: 'Artifacts export purpose'
  - id: assertions-output
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L770-L793'
    title: 'assertions.txt output'
  - id: test-chaining
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L456-L492'
    title: 'Test chaining artifacts'
  - id: v0-3-0-artifacts-dir-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/cmd/xprin/test/test.go#L47'
    title: 'xprin v0.3.0 --artifacts-dir flag'
source_repository: crossplane-contrib/xprin
source_tag: v0.5.0
source_commit: eb5d7131c596e9a5663da349149184d54d704f42
source_paths: [cmd/xprin/test/test.go, internal/testexecution/utils/options.go, internal/testexecution/runner/artifacts.go, internal/testexecution/runner/runner.go, internal/testexecution/runner/artifacts_test.go, docs/getting-started.md, docs/how-it-works.md]
introduced_in: v0.3.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither the flag nor its documentation Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

From xprin v0.3.0, `xprin test -a <dir>` or `--artifacts-dir <dir>` copies each
test case's inputs and outputs to a persistent directory so they can be
inspected after the run.[^v0-3-0-artifacts-dir-flag][^artifacts-dir-flag][^artifacts-docs][^artifacts-purpose]
Without the flag nothing is exported.[^artifacts-dir-default][^artifacts-dir-wiring]

```shell
xprin test -a /tmp/xprin-debug tests/...
```

# Layout

Each invocation creates one timestamped run directory, shared by all suites in
that invocation:[^artifacts-run-dir][^artifacts-run-dir-setup]

```text
<dir>/xprin-artifacts-<YYYYMMDDHHMMSS>/
  <suite path relative to the working directory, without .yaml>/
    <NN>_<test-case-name>/
      inputs/
      outputs/
```

Test-case directories use a 1-based, zero-padded index. Unsafe path characters
are replaced, and a suite outside the working directory uses its sanitized
absolute path.[^artifacts-layout][^artifacts-tests]

# Behavior

- `inputs/` is always copied and `outputs/` is copied when present, on every
  exit path after the test case's temporary directory is created, including
  later failures, and before that directory is removed.[^artifacts-copy][^artifacts-defer]
- A copy error prints a warning and does not fail the test case.[^artifacts-copy]
- After each suite, xprin prints the suite's artifacts path to standard
  error.[^artifacts-announce][^artifacts-docs]
- Outputs can include an `assertions.txt` with the results of every executed
  assertion, independent of the display flags.[^assertions-output]
- The flag is not tied to an assertion type; it exports whatever each test case
  produced.[^artifacts-copy]

# Not test chaining

Test chaining is a separate feature: a test case with an `id` exposes its
outputs to later test cases through `.Tests.<id>.Outputs`, and those temporary
artifacts are cleaned up after the run.[^test-chaining] `--artifacts-dir` keeps
a persistent copy of every test case, with or without an `id`.[^artifacts-copy]

# Limitations

- The run-directory timestamp is the xprin process's local time from Go
  `time.Now()`; the documentation does not state a time zone.[^artifacts-run-dir]
- Keep exported suites XR-oriented in this catalog; legacy Claim inputs are
  excluded.

# Relationships

- [xprin test suites](xprin-test-suites.md) describes the suites whose test
  cases are exported.

[^artifacts-dir-flag]: [xprin test --artifacts-dir flag](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L48)
[^artifacts-dir-wiring]: [Flag passed to test options](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L139)
[^artifacts-dir-default]: [Empty artifacts directory disables export](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/utils/options.go#L44-L47)
[^artifacts-layout]: [Artifact suite and test-case paths](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts.go#L27-L118)
[^artifacts-run-dir]: [Per-invocation run directory](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts.go#L120-L143)
[^artifacts-copy]: [Per-test-case inputs and outputs copy](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts.go#L145-L172)
[^artifacts-run-dir-setup]: [Run directory created for suites with test cases](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L175-L180)
[^artifacts-announce]: [Artifacts path reported per suite](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L197-L200)
[^artifacts-defer]: [Copy runs on every exit path before cleanup](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L238-L256)
[^artifacts-tests]: [Artifact path tests](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/artifacts_test.go#L26-L85)
[^artifacts-docs]: [Exporting artifacts guidance](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/getting-started.md#L91-L95)
[^artifacts-purpose]: [Artifacts export purpose](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L699)
[^assertions-output]: [assertions.txt output](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L770-L793)
[^test-chaining]: [Test chaining artifacts](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L456-L492)
[^v0-3-0-artifacts-dir-flag]: [xprin v0.3.0 --artifacts-dir flag](https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/cmd/xprin/test/test.go#L47)
