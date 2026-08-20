---
type: function
title: Install function-go-templating
description: Install and reference the v0.12.2 function package in a pipeline Composition.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, go-template]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: readme-installation-and-pipeline-input
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L9-L44'
    title: 'README installation and pipeline input'
  - id: selected-v0-12-2-commit
    resource: 'https://github.com/crossplane-contrib/function-go-templating/commit/0a1e6d386f4363fae257ddbfb5b497416370e830'
    title: 'Selected v0.12.2 commit'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Overview

`function-go-templating` renders desired resources from Go templates.
This catalog selected stable release `v0.12.2`, pinned to commit `0a1e6d386f4363fae257ddbfb5b497416370e830`.
Install a `pkg.crossplane.io/v1` `Function`, then reference that object's name from a pipeline step and provide a [GoTemplate input](input.md).[^readme-installation-and-pipeline-input][^selected-v0-12-2-commit]

The bundled installation example still pins `v0.11.5`; use `v0.12.2` for this knowledge set. Example object names also vary, so `functionRef.name` must match the installed `Function` object's name.[^readme-installation-and-pipeline-input]

Feature maturity is **Not stated by selected sources**.

[^readme-installation-and-pipeline-input]: [README installation and pipeline input](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L9-L44)
[^selected-v0-12-2-commit]: [Selected v0.12.2 commit](https://github.com/crossplane-contrib/function-go-templating/commit/0a1e6d386f4363fae257ddbfb5b497416370e830)
