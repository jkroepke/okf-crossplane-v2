---
type: functioninput
title: Environment template source in function-go-templating
description: Load a Go template string from the reserved environment pipeline-context map.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, function, go-template, environment-config, context]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: environment-source-lookup-and-validation
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/template.go#L103-L122'
    title: 'Environment source lookup and validation'
  - id: generated-gotemplate-input-schema
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L18-L94'
    title: 'Generated GoTemplate input schema'
  - id: source-retrieval-parsing-options-and-fatal-execution-paths
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L82-L117'
    title: 'Source retrieval, parsing, options, and fatal execution paths'
  - id: readme-direct-environment-context-expression
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L68'
    title: 'README direct environment context expression'
  - id: readme-environment-context-update
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277'
    title: 'README environment Context update'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths:
  - package/input/gotemplating.fn.crossplane.io_gotemplates.yaml
  - template.go
  - fn.go
feature_state: Beta
feature_state_basis: The Environment source is configured through the served and stored gotemplating.fn.crossplane.io/v1beta1 GoTemplate input.
---

# Schema and lookup

Configure `source: Environment` with `environment.key`. Runtime reads exactly `context["apiextensions.crossplane.io/environment"][key]` and requires the result to be a string.[^environment-source-lookup-and-validation]

```yaml
apiVersion: gotemplating.fn.crossplane.io/v1beta1
kind: GoTemplate
source: Environment
environment:
  key: template
```

The generated schema requires only `source`; it does not enumerate source values or conditionally require `environment.key`. Runtime supplies the missing validation.[^generated-gotemplate-input-schema]

# Errors

A missing `environment.key`, absent reserved context, absent nested key, non-map environment, or non-string template value becomes a fatal `invalid function input` result before template parsing.[^environment-source-lookup-and-validation][^source-retrieval-parsing-options-and-fatal-execution-paths]

Template `missingkey` options do not affect source lookup because they apply later during template execution. They only govern missing data accessed by the loaded template.[^source-retrieval-parsing-options-and-fatal-execution-paths]

# Direct data access and updates

An Inline or FileSystem template can still read environment values directly
with `index .context "apiextensions.crossplane.io/environment" ...`;
Environment source is needed only when the template text itself is stored in
the environment.[^readme-direct-environment-context-expression]

The Alpha rendered `Context` instruction can deep-merge updates under the same reserved key. See [Context](context.md) for its separate Alpha feature state and same-invocation overwrite limitations.[^readme-environment-context-update]

# Relationships

[function-environment-configs](../function-environment-configs/index.md) must run first to select and merge EnvironmentConfigs. [function-auto-ready](../function-auto-ready/index.md) may run after resource rendering when its readiness behavior is needed. The [combined pipeline guide](../environment-config-pipeline.md) documents shared-key overwrite ownership.

[^environment-source-lookup-and-validation]: [Environment source lookup and validation](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/template.go#L103-L122)
[^generated-gotemplate-input-schema]: [Generated GoTemplate input schema](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L18-L94)
[^source-retrieval-parsing-options-and-fatal-execution-paths]: [Source retrieval, parsing, options, and fatal execution paths](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L82-L117)
[^readme-direct-environment-context-expression]: [README direct environment context expression](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L68)
[^readme-environment-context-update]: [README environment Context update](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277)
