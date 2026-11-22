---
type: Crossplane Test Tool
title: Show xprin test-case dependencies with xprin graph
description: Use xprin graph, available since xprin v0.6.0, to print the needs dependency tree of each testsuite file without running tests or loading an xprin configuration.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, dependencies, cli, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-11-22T14:30:00Z" }
sources:
  - id: graph-command
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/main.go#L38-L51'
    title: 'graph subcommand registration and no-config commands'
  - id: graph-cmd
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/graph/graph.go#L31-L76'
    title: 'graph command targets, quiet flag and file walk'
  - id: graph-tree
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/graph/render/tree.go#L28-L90'
    title: 'Tree rendering with repeated test cases marked (*)'
  - id: graph-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L606-L634'
    title: 'Dependency graph documentation'
  - id: v0-6-0-graph-command
    resource: 'https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/cmd/xprin/main.go#L42'
    title: 'xprin v0.6.0 registers graph'
source_repository: crossplane-contrib/xprin
source_tag: v0.7.0
source_commit: 891c1bf6de72c0978a695a02b854e15ae9a76350
source_paths: [cmd/xprin/main.go, cmd/xprin/graph/graph.go, internal/graph/render/tree.go, docs/how-it-works.md]
introduced_in: v0.6.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither the graph command nor its documentation Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

`xprin graph <targets>` prints which test cases of each testsuite file
[need](xprin-test-case-needs.md) which others, without running
anything.[^graph-command][^graph-docs] It is available since xprin
v0.6.0.[^v0-6-0-graph-command]

```shell
xprin graph tests/...
```

The example is adapted from the documented target forms.[^graph-docs]

# Usage

- Targets are suite files, directories, or recursive `dir/...` paths, as for
  `xprin test`. `-q` suppresses the `[no testsuite files]` and
  `[no test cases found]` messages.[^graph-cmd][^graph-docs]
- The command needs no xprin configuration file.[^graph-command][^graph-docs]

# Reading the tree

- Test cases at the top level need no other test case.[^graph-docs]
- A test case listed under another one needs it. Siblings do not need each
  other.[^graph-docs]
- A test case that needs several others is listed under each of them. It is
  expanded the first time and marked `(*)` after that.[^graph-tree][^graph-docs]
- A test case's `id`, if it has one, is shown in brackets.[^graph-docs]

# Limitations

- The tree is built from `needs` only. xprin does not read templates for
  `.Tests` to build it, so a file without `needs` shows every test case at the
  top level.[^graph-docs]
- Dependencies that are not declared in `needs`, such as a hook that relies on
  another test case's files, are not shown.[^graph-docs]

# Relationships

- [Order xprin test cases with needs](xprin-test-case-needs.md) defines the
  dependencies that the tree shows.
- [xprin test suites](xprin-test-suites.md) describes the testsuite files that
  the command reads.

[^graph-command]: [graph subcommand registration and no-config commands](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/main.go#L38-L51)
[^graph-cmd]: [graph command targets, quiet flag and file walk](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/cmd/xprin/graph/graph.go#L31-L76)
[^graph-tree]: [Tree rendering with repeated test cases marked (*)](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/internal/graph/render/tree.go#L28-L90)
[^graph-docs]: [Dependency graph documentation](https://github.com/crossplane-contrib/xprin/blob/891c1bf6de72c0978a695a02b854e15ae9a76350/docs/how-it-works.md#L606-L634)
[^v0-6-0-graph-command]: [xprin v0.6.0 registers graph](https://github.com/crossplane-contrib/xprin/blob/76fbb80af158f8b10a6b707399c7c87e54f442d4/cmd/xprin/main.go#L42)
