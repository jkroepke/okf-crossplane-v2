---
type: Crossplane Test Tool
title: Test Composition rendering with xprin suites and assertions
description: Use xprin to run local Crossplane composition renders and evaluate declarative assertions over their output.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, composition, assertions, xprin]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/xprin
source_commit: b5a100aa3e7118c1acdd2096b7993929939624b2
source_paths:
  - README.md
  - docs/testsuite-specification.md
  - docs/assertions.md
---

# Overview

xprin is a Crossplane ecosystem test tool that orchestrates local CLI render
and validation commands, then evaluates declarative assertions. It does not
need a Kubernetes cluster, but rendering Composition Functions still requires
Docker. This concept describes xprin's own test framework; it does not change
the Crossplane CLI contract described in [local Composition rendering](/cli/local-composition-rendering.md).

# Suite inputs

A suite identifies an XR, Composition, and Functions input. It may also
provide observed resources and CRDs. Keep the suite XR-oriented for this
legacy-free catalog.

# Assertions

After rendering, a suite may validate rendered manifests and check declarative
assertions. The project's XR-oriented examples demonstrate count, existence,
field-existence, field-type, and field-value assertions. Golden-file diff
assertions are another optional check.

The suite sequence is setup; optional XR patching; rendering; optional
validation; optional assertions; hooks; and optional artifact export or
chaining. Treat assertions as a repeatable test suite around a known input,
not proof that providers will successfully reconcile the generated resources.

# Relationship to CLI rendering

Use the CLI directly for a fast authoring check:

```shell
crossplane composition render example.yaml composition.yaml functions.yaml
```

Use xprin when that render needs named, repeatable expectations. The same
observed-resource idea can model status-dependent Function behavior in both
workflows.

# Citations

[1] [xprin purpose, local prerequisites, and CLI integration](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/README.md#L9-L40)

[2] [Test-suite inputs and assertion configuration](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/docs/testsuite-specification.md#L1-L29)

[3] [Execution sequence](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/README.md#L123-L168)

[4] [XR-oriented assertion examples](https://github.com/crossplane-contrib/xprin/blob/b5a100aa3e7118c1acdd2096b7993929939624b2/examples/mytests/6_assertions/example1_assertions_xprin.yaml#L1-L110)
