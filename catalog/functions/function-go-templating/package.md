---
type: function
title: Install function-go-templating
description: Install and reference the v0.12.2 function package in a pipeline Composition.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, go-template]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Overview

`function-go-templating` renders desired resources from Go templates.
This catalog selected stable release `v0.12.2`, pinned to commit `0a1e6d386f4363fae257ddbfb5b497416370e830`.
Install a `pkg.crossplane.io/v1` `Function`, then reference that object's name from a pipeline step and provide a [GoTemplate input](input.md).[1][2]

The bundled installation example still pins `v0.11.5`; use `v0.12.2` for this knowledge set. Example object names also vary, so `functionRef.name` must match the installed `Function` object's name.[1]

Feature maturity is **Not stated by selected sources**.

# Citations

[1] [README installation and pipeline input](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L9-L44)
[2] [Selected v0.12.2 commit](https://github.com/crossplane-contrib/function-go-templating/commit/0a1e6d386f4363fae257ddbfb5b497416370e830)
