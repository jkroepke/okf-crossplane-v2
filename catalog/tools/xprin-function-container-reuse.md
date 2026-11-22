---
type: Crossplane Test Tool
title: xprin function container reuse
description: Understand how xprin, since v0.5.0, reuses one Docker container per Composition Function image across a run, how v0.7.0 overrides user-set container annotations, and how --no-container-reuse opts out.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, docker, functions, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-11-22T14:30:00Z" }
sources:
  - id: no-container-reuse-test-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L47'
    title: 'xprin test --no-container-reuse flag'
  - id: no-container-reuse-update-goldens-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L41'
    title: 'xprin update-goldens --no-container-reuse flag'
  - id: v0-4-0-test-flags
    resource: 'https://github.com/crossplane-contrib/xprin/blob/457dfbea3570cfd1016d00838e6999243f7c6c74/cmd/xprin/test/test.go#L38-L47'
    title: 'xprin v0.4.0 test flags without container reuse'
  - id: reuse-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L673-L693'
    title: 'Function container reuse documentation'
  - id: reuse-setup
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/processor/processor.go#L44-L75'
    title: 'Per-invocation reuse coordinator'
  - id: docker-client
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/docker.go#L42-L64'
    title: 'Docker client and removal'
  - id: reuse-annotations
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/reuse.go#L33-L171'
    title: 'Function annotations for reuse'
  - id: reuse-annotation-wiring
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L466-L475'
    title: 'Annotations applied to the temporary functions copy'
  - id: container-names
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/coordinator.go#L36-L57'
    title: 'Container naming'
  - id: reuse-network
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/coordinator.go#L59-L79'
    title: 'Shared Docker network'
  - id: reuse-network-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L588-L598'
    title: 'Render receives the shared network on CLI v2.3 or later'
  - id: reuse-cleanup
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/coordinator.go#L81-L92'
    title: 'Cleanup at the end of the run'
  - id: reuse-tests
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/reuse_test.go#L78-L221'
    title: 'Container reuse annotation tests'
  - id: render-version-tier
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L39-L84'
    title: 'CLI tiers: render version support only at v2.3.0 or later'
  - id: v0-7-0-annotation-override
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/containers/annotate.go#L154-L186'
    title: 'xprin v0.7.0 replaces user-set container annotations'
  - id: v0-7-0-annotation-migration-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L706-L726'
    title: 'Migrating from user-set container annotations'
  - id: v0-7-0-interrupt
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/interrupt/interrupt.go#L34-L69'
    title: 'xprin v0.7.0 SIGINT and SIGTERM handling'
  - id: v0-7-0-interrupt-wiring
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/test/test.go#L105-L109'
    title: 'xprin test installs the interrupt handler'
  - id: v0-7-0-interrupt-update-goldens
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/updategoldens/update_goldens.go#L74'
    title: 'xprin update-goldens installs the interrupt handler'
  - id: v0-7-0-interrupted-summary
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/engine/testsuiteresult.go#L156-L160'
    title: 'FAIL <file> [interrupted] summary'
  - id: v0-7-0-stop-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L702-L704'
    title: 'Stopping a run and the known edge case'
  - id: v0-7-0-interrupted-run
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/processor/processor.go#L117-L122'
    title: 'An interrupted run fails'
source_repository: crossplane-contrib/xprin
source_tag: v0.5.0
source_commit: eb5d7131c596e9a5663da349149184d54d704f42
source_paths: [cmd/xprin/test/test.go, cmd/xprin/updategoldens/update_goldens.go, docs/how-it-works.md, internal/xpcli/tier.go, internal/testexecution/processor/processor.go, internal/testexecution/containers/docker.go, internal/testexecution/containers/reuse.go, internal/testexecution/containers/coordinator.go, internal/testexecution/runner/runner.go, internal/testexecution/containers/reuse_test.go]
introduced_in: v0.5.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither container reuse nor its flag Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

From xprin v0.5.0, `xprin test` and `xprin update-goldens` reuse one Docker
container per Composition Function image for the whole invocation instead of
starting a container for every `crossplane render` call.[^reuse-docs][^reuse-setup]
Reuse is on by default; `--no-container-reuse` restores a fresh container per
render call.[^no-container-reuse-test-flag][^no-container-reuse-update-goldens-flag][^reuse-docs]
xprin v0.4.0 had no such flag.[^v0-4-0-test-flags]

```shell
xprin test --no-container-reuse tests/...
```

# Behavior

- xprin edits only the temporary copy of each test case's functions file. On
  every `Function` with a `spec.package`, it sets
  `render.crossplane.io/runtime-docker-name` and
  `render.crossplane.io/runtime-docker-cleanup: Orphan`. At v0.5.0 it leaves
  either annotation alone if the user already set it.[^reuse-annotation-wiring][^reuse-annotations][^reuse-tests]
- Since xprin v0.7.0, with reuse on, xprin replaces user-set
  `runtime-docker-name` and `runtime-docker-cleanup` annotations and removes a
  user-set `render.crossplane.io/runtime-docker-network` annotation, without a
  warning. v0.6.0 kept them and printed a deprecation warning. With
  `--no-container-reuse`, xprin never touches these
  annotations.[^v0-7-0-annotation-override][^v0-7-0-annotation-migration-docs]
- Container names are derived from a run id and the image reference, as
  `xprin-<run-id>-<hash>`, so one image maps to one container across all suites
  in the run.[^container-names][^reuse-docs]
- With Crossplane CLI v2.3.0 or later, xprin creates one `xprin-net-<run-id>`
  network and passes it to every render as
  `--crossplane-docker-network`.[^reuse-network][^reuse-network-flag][^render-version-tier][^reuse-docs]
- At the end of the run, whether it passed or failed, xprin force-removes the
  tracked containers and the network on a best-effort
  basis. Up to v0.6.0, containers named by a user-set annotation are not
  tracked and are not removed.[^reuse-cleanup][^docker-client][^reuse-annotations][^v0-7-0-annotation-migration-docs]
- The Crossplane controller container that `crossplane render` starts on CLI
  v2.3.0 or later is not reused.[^reuse-docs]
- xprin talks to Docker through the Docker API client from the environment; if
  it cannot create that client, the run fails.[^reuse-setup][^docker-client]

# Stopping a run

Since xprin v0.7.0, the first Ctrl-C (`SIGINT`) or `SIGTERM` stops `xprin test`
and `xprin update-goldens` gracefully. Running test cases finish, test cases
that have not started are not run, and the containers, the network and the
temporary directories are removed.[^v0-7-0-interrupt][^v0-7-0-interrupt-wiring][^v0-7-0-interrupt-update-goldens][^v0-7-0-stop-docs]
Unstarted test cases are not reported as `SKIP`; a file that has them prints
`FAIL <file> [interrupted]`, and the run fails.[^v0-7-0-interrupted-summary][^v0-7-0-stop-docs][^v0-7-0-interrupted-run]
A second signal exits at once with code 130 and skips the
cleanup.[^v0-7-0-interrupt]

# Migrating user-set container annotations

To keep a container you manage yourself, for example a Function that runs
locally while you debug it, keep the annotations and run with
`--no-container-reuse`. Otherwise remove them and let xprin name the container
after its image.[^v0-7-0-annotation-migration-docs]

# Limitations

- If xprin is killed abruptly, for example with `SIGKILL`, out of memory, or a
  second Ctrl-C on v0.7.0, containers and the network are left behind. Their
  names start with `xprin-`, and the project documents removing them by
  name.[^reuse-docs][^v0-7-0-stop-docs]
- The project's safety rationale is that Functions are stateless by contract;
  use `--no-container-reuse` when a Function under test may keep state. That
  rationale is xprin's own documentation, not a Crossplane Core
  guarantee.[^reuse-docs]
- The documentation describes cleanup when `xprin test` finishes; the code uses
  the same lifecycle for `update-goldens`.[^reuse-docs][^reuse-setup]
- Container reuse with Podman through the Docker API client is not shown by the
  selected sources. Treat it as unresolved.

# Relationships

- [xprin test suites](xprin-test-suites.md) describes the runs whose Function
  containers are reused.
- [Run xprin test cases in parallel](xprin-parallel-test-runs.md) shares these
  containers between renders that run at the same time.

[^no-container-reuse-test-flag]: [xprin test --no-container-reuse flag](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/test/test.go#L47)
[^no-container-reuse-update-goldens-flag]: [xprin update-goldens --no-container-reuse flag](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/updategoldens/update_goldens.go#L41)
[^v0-4-0-test-flags]: [xprin v0.4.0 test flags without container reuse](https://github.com/crossplane-contrib/xprin/blob/457dfbea3570cfd1016d00838e6999243f7c6c74/cmd/xprin/test/test.go#L38-L47)
[^reuse-docs]: [Function container reuse documentation](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/how-it-works.md#L673-L693)
[^reuse-setup]: [Per-invocation reuse coordinator](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/processor/processor.go#L44-L75)
[^docker-client]: [Docker client and removal](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/docker.go#L42-L64)
[^reuse-annotations]: [Function annotations for reuse](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/reuse.go#L33-L171)
[^reuse-annotation-wiring]: [Annotations applied to the temporary functions copy](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L466-L475)
[^container-names]: [Container naming](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/coordinator.go#L36-L57)
[^reuse-network]: [Shared Docker network](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/coordinator.go#L59-L79)
[^reuse-network-flag]: [Render receives the shared network on CLI v2.3 or later](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L588-L598)
[^reuse-cleanup]: [Cleanup at the end of the run](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/coordinator.go#L81-L92)
[^reuse-tests]: [Container reuse annotation tests](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/containers/reuse_test.go#L78-L221)
[^render-version-tier]: [CLI tiers: render version support only at v2.3.0 or later](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L39-L84)
[^v0-7-0-annotation-override]: [xprin v0.7.0 replaces user-set container annotations](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/containers/annotate.go#L154-L186)
[^v0-7-0-annotation-migration-docs]: [Migrating from user-set container annotations](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L706-L726)
[^v0-7-0-interrupt]: [xprin v0.7.0 SIGINT and SIGTERM handling](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/interrupt/interrupt.go#L34-L69)
[^v0-7-0-interrupt-wiring]: [xprin test installs the interrupt handler](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/test/test.go#L105-L109)
[^v0-7-0-interrupt-update-goldens]: [xprin update-goldens installs the interrupt handler](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/updategoldens/update_goldens.go#L74)
[^v0-7-0-interrupted-summary]: [FAIL <file> [interrupted] summary](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/engine/testsuiteresult.go#L156-L160)
[^v0-7-0-stop-docs]: [Stopping a run and the known edge case](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L702-L704)
[^v0-7-0-interrupted-run]: [An interrupted run fails](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/testexecution/processor/processor.go#L117-L122)
