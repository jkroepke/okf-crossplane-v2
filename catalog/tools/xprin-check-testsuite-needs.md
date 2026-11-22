---
type: Crossplane Test Tool
title: Check xprin testsuite needs before upgrading
description: Use xprin-helpers check-testsuite-needs, available since xprin v0.6.0, to find test cases that read .Tests outputs without listing them in needs, as a migration gate for xprin v0.7.0.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, migration, ci, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-11-22T14:30:00Z" }
sources:
  - id: helpers-registration
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin-helpers/main.go#L24-L34'
    title: 'xprin-helpers check-testsuite-needs registration'
  - id: check-needs-cmd
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin-helpers/testsuiteneeds/cmd.go#L33-L103'
    title: 'check-testsuite-needs flags, help and exit code'
  - id: check-needs-usage-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/xprin-helpers/check-testsuite-needs.md#L1-L34'
    title: 'check-testsuite-needs purpose, usage and scope'
  - id: check-needs-output-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/xprin-helpers/check-testsuite-needs.md#L35-L90'
    title: 'check-testsuite-needs results and cases that require a person'
  - id: needs-migration-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L489-L512'
    title: 'Migrating from xprin 0.5 and earlier'
  - id: v0-6-0-helpers-registration
    resource: 'https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/cmd/xprin-helpers/main.go#L32'
    title: 'xprin v0.6.0 registers check-testsuite-needs'
source_repository: crossplane-contrib/xprin
source_tag: v0.7.0
source_commit: 891c1bf6de72c0978a695a02b854e15ae9a76350
source_paths: [cmd/xprin-helpers/main.go, cmd/xprin-helpers/testsuiteneeds/cmd.go, docs/xprin-helpers/check-testsuite-needs.md, docs/how-it-works.md]
introduced_in: v0.6.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither the helper nor its documentation Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

`xprin-helpers check-testsuite-needs` checks that every test case lists in
[`needs`](xprin-test-case-needs.md) the test cases whose outputs it reads through
`.Tests.<id>`.[^helpers-registration][^check-needs-usage-docs] It ships in the
separate `xprin-helpers` binary since xprin v0.6.0.[^v0-6-0-helpers-registration]
xprin v0.7.0 fails such test cases at run time, so the helper serves as a
migration check.[^check-needs-cmd][^needs-migration-docs]

```shell
xprin-helpers check-testsuite-needs tests/...
```

The example is adapted from the documented target forms.[^check-needs-usage-docs]

# Usage

- Targets are suite files, directories, or recursive `dir/...` paths, as for
  `xprin test`. `-v` shows every test case; `-q` suppresses empty-target
  messages.[^check-needs-cmd][^check-needs-usage-docs]
- The exit code is 1 when anything is missing or needs a person, so a CI
  pipeline can use the command as a gate.[^check-needs-cmd][^check-needs-usage-docs]

# Behavior

- Every test case of every file is checked, including files that already use
  `needs`. It looks for `.Tests` in the test case's fields, in the `common`
  configuration it inherits, and in its hooks.[^check-needs-usage-docs]
- Output follows `xprin test`. A test case `PASS`es when it lists everything it
  reads, is skipped when it reads nothing, and `FAIL`s with a `Missing Needs:`
  list of `[x] <id>` lines when ids are missing.[^check-needs-output-docs]
- It does not guess. It fails with a `[!]` line when `.Tests` use cannot be
  traced, such as `range .Tests`, when an id does not exist, when a test case
  reads its own outputs, or when adding the missing ids would create a cycle.
  Untraceable use in a test case that already lists `needs` is reported as a
  skip with a reason.[^check-needs-output-docs]
- A `needs` entry that is not read through `.Tests` is never reported, because
  it is a valid way to order test cases.[^check-needs-cmd][^check-needs-usage-docs]

# Migration route

The project suggests moving to v0.6.0, running the helper, adding the missing
ids, confirming that `xprin test` prints no deprecation warnings, and then
moving to v0.7.0. The helper also works with later versions.[^needs-migration-docs]

# Limitations

- The helper finds only `.Tests` use. It does not find dependencies through
  shared files or other state; declare those in `needs` by hand.[^check-needs-cmd][^check-needs-usage-docs]
- `xprin-helpers` is a separate binary from `xprin`.[^helpers-registration]
  Its Claim conversion helper is excluded from this legacy-free catalog.

# Relationships

- [Order xprin test cases with needs](xprin-test-case-needs.md) describes the
  field that the helper checks and the v0.7.0 removal it prepares for.
- [Show xprin test-case dependencies](xprin-dependency-graph.md) shows the
  declared `needs` after migration.

[^helpers-registration]: [xprin-helpers check-testsuite-needs registration](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin-helpers/main.go#L24-L34)
[^check-needs-cmd]: [check-testsuite-needs flags, help and exit code](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin-helpers/testsuiteneeds/cmd.go#L33-L103)
[^check-needs-usage-docs]: [check-testsuite-needs purpose, usage and scope](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/xprin-helpers/check-testsuite-needs.md#L1-L34)
[^check-needs-output-docs]: [check-testsuite-needs results and cases that require a person](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/xprin-helpers/check-testsuite-needs.md#L35-L90)
[^needs-migration-docs]: [Migrating from xprin 0.5 and earlier](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L489-L512)
[^v0-6-0-helpers-registration]: [xprin v0.6.0 registers check-testsuite-needs](https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/cmd/xprin-helpers/main.go#L32)
