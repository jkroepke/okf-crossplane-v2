---
type: Crossplane Test Tool
title: Test Composition rendering with xprin suites and assertions
description: Use xprin to run local Crossplane composition renders and evaluate declarative assertions over their output.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, composition, assertions, xprin]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: xprin-purpose-local-prerequisites-and-cli-integration
    resource: 'https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/README.md#L9-L40'
    title: 'xprin purpose, local prerequisites, and CLI integration'
  - id: test-suite-inputs-and-assertion-configuration
    resource: 'https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/docs/testsuite-specification.md#L1-L29'
    title: 'Test-suite inputs and assertion configuration'
  - id: execution-sequence
    resource: 'https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/README.md#L123-L168'
    title: 'Execution sequence'
  - id: xr-oriented-assertion-examples
    resource: 'https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/examples/mytests/6_assertions/example1_assertions_xprin.yaml#L1-L110'
    title: 'XR-oriented assertion examples'
source_repository: crossplane-contrib/xprin
source_commit: b5a100aa3e7118c1acdd2096b7993929939624b2
source_paths:
  - README.md
  - docs/testsuite-specification.md
  - docs/assertions.md
  - examples/mytests/6_assertions/example1_assertions_xprin.yaml
feature_state: Not stated by selected sources
---

# Overview

xprin is a Crossplane ecosystem test tool that orchestrates local CLI render
and validation commands, then evaluates declarative assertions. It does not
need a Kubernetes cluster, but rendering Composition Functions still requires
Docker.[^xprin-purpose-local-prerequisites-and-cli-integration] This concept describes xprin's own test framework; it does not change
the Crossplane CLI contract described in [local Composition rendering](/cli/local-composition-rendering.md).

# Suite inputs

A suite identifies an XR, Composition, and Functions input. It may also
provide observed resources and CRDs. Keep the suite XR-oriented for this
legacy-free catalog.[^test-suite-inputs-and-assertion-configuration]

# Assertions

After rendering, a suite may validate rendered manifests and check declarative
assertions. The project's XR-oriented examples demonstrate count, existence,
field-existence, field-type, and field-value assertions. Golden-file diff
assertions are another optional check.[^xr-oriented-assertion-examples]

The suite sequence is setup; optional XR patching; rendering; optional
validation; optional assertions; hooks; and optional artifact export or
chaining.[^execution-sequence] Treat assertions as a repeatable test suite around a known input,
not proof that providers will successfully reconcile the generated resources.

# Relationship to CLI rendering

Use the CLI directly for a fast authoring check:

```shell
crossplane composition render example.yaml composition.yaml functions.yaml
```

Use xprin when that render needs named, repeatable expectations. The same
observed-resource idea can model status-dependent Function behavior in both
workflows.

[^xprin-purpose-local-prerequisites-and-cli-integration]: [xprin purpose, local prerequisites, and CLI integration](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/README.md#L9-L40)
[^test-suite-inputs-and-assertion-configuration]: [Test-suite inputs and assertion configuration](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/docs/testsuite-specification.md#L1-L29)
[^execution-sequence]: [Execution sequence](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/README.md#L123-L168)
[^xr-oriented-assertion-examples]: [XR-oriented assertion examples](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/examples/mytests/6_assertions/example1_assertions_xprin.yaml#L1-L110)
