---
type: Crossplane Test Tool
title: Run xprin test cases in parallel
description: Use xprin test --parallel, available since xprin v0.7.0, to run up to N test cases at the same time across testsuite files while each test case waits only for its needs.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, performance, ci, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-11-22T14:30:00Z" }
sources:
  - id: parallel-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/test/test.go#L50'
    title: 'xprin test --parallel flag'
  - id: parallel-value
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/test/parallelism.go#L27-L75'
    title: 'Parsing of the --parallel value'
  - id: parallel-scheduler
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/scheduler/scheduler.go#L17-L59'
    title: 'Scheduler for test cases across testsuite files'
  - id: parallel-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L636-L657'
    title: 'Parallel execution documentation'
  - id: parallel-container-creation
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/containers/acquire.go#L24-L28'
    title: 'Serialized first use of a function container'
  - id: parallel-reuse-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L698'
    title: 'Container reuse with --parallel'
  - id: v0-6-0-test-flags
    resource: 'https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/cmd/xprin/test/test.go#L35-L52'
    title: 'xprin v0.6.0 test flags without --parallel'
source_repository: crossplane-contrib/xprin
source_tag: v0.7.0
source_commit: 891c1bf6de72c0978a695a02b854e15ae9a76350
source_paths: [cmd/xprin/test/test.go, cmd/xprin/test/parallelism.go, internal/testexecution/scheduler/scheduler.go, internal/testexecution/containers/acquire.go, docs/how-it-works.md]
introduced_in: v0.7.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither the flag nor its documentation Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

From xprin v0.7.0, `xprin test -p N` (or `--parallel=N`) runs up to N test
cases at the same time, across all testsuite files of the
run.[^parallel-flag][^parallel-docs] xprin v0.6.0 had no such
flag.[^v0-6-0-test-flags] `xprin update-goldens` has no parallel
flag.[^parallel-docs]

```shell
xprin test tests/... -p 4
```

The example is taken from the project's documentation.[^parallel-docs]

# Usage

- N must be 1 or more; the default is 1, one test case at a time.[^parallel-value][^parallel-docs]
- `--parallel` without a number uses the CPU count that Go sees
  (`GOMAXPROCS`), which respects a container's CPU limit.[^parallel-value][^parallel-docs]
- A number after the flag is read as N, so a target that is a number must be
  written as `./4`.[^parallel-flag][^parallel-value]
- N counts test cases, not CPUs. Most time is spent waiting on
  `crossplane render` and Docker, so N can exceed the CPU count.[^parallel-docs]

# Behavior

- A test case waits only for the test cases in its
  [`needs`](xprin-test-case-needs.md). Any other test case, including one from
  another file, may run at the same time.[^parallel-scheduler][^parallel-docs]
- A failure does not stop the run. A test case whose `needs` failed or was
  skipped is still skipped.[^parallel-docs]
- Output matches a serial run except for timings. Results print in serial-run
  order. With `--debug`, each test case's debug lines print together just
  before its result.[^parallel-scheduler][^parallel-docs]
- With [function container reuse](xprin-function-container-reuse.md), the first
  render that uses an image creates its container, and other renders of that
  image wait for it.[^parallel-container-creation][^parallel-reuse-docs]

# Limitations

- xprin assumes test cases are independent apart from `needs`. Shared files,
  ports, directories, or external systems are not detected; order such test
  cases with `needs`.[^parallel-docs]
- N parallel test cases are N simultaneous renders on Docker, each with a
  Crossplane controller container on CLI v2.3.0 or later.[^parallel-docs]
- With `--no-container-reuse`, every render creates its own Docker network.
  A high N can exhaust Docker address pools, failing renders with
  `all predefined address pools have been fully subnetted`. Keep reuse on, or
  lower N.[^parallel-docs]
- Performance guidance is xprin project documentation, not a measured catalog
  claim.[^parallel-docs]

# Relationships

- [Order xprin test cases with needs](xprin-test-case-needs.md) is the only
  ordering that parallel runs respect.
- [xprin function container reuse](xprin-function-container-reuse.md) shares
  function containers between parallel renders.

[^parallel-flag]: [xprin test --parallel flag](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/test/test.go#L50)
[^parallel-value]: [Parsing of the --parallel value](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/test/parallelism.go#L27-L75)
[^parallel-scheduler]: [Scheduler for test cases across testsuite files](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/scheduler/scheduler.go#L17-L59)
[^parallel-docs]: [Parallel execution documentation](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L636-L657)
[^parallel-container-creation]: [Serialized first use of a function container](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/containers/acquire.go#L24-L28)
[^parallel-reuse-docs]: [Container reuse with --parallel](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L698)
[^v0-6-0-test-flags]: [xprin v0.6.0 test flags without --parallel](https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/cmd/xprin/test/test.go#L35-L52)
