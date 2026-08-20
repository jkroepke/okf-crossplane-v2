---
type: function
title: Template request data and pipeline context
description: Read observed and desired state, context, extra resources, and credentials from templates.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, context, extra-resources]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: readme-request-data
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73'
    title: 'README request data'
  - id: readme-context-resource
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277'
    title: 'README Context resource'
  - id: readme-extraresources-behavior
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L239'
    title: 'README ExtraResources behavior'
  - id: getcredentialdata-implementation
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L177'
    title: 'getCredentialData implementation'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Behavior

Templates receive the function's `RunFunctionRequest`, including observed and desired composite and composed resources, pipeline context, and fetched extra resources.[^readme-request-data]

- Rendering the special [`Context`](context.md) instruction deeply merges data
  into response context for later pipeline steps.[^readme-context-resource]
- [`ExtraResources`](extra-resources.md) requests can match resources by name or
  labels. Results are available in the current request and are merged into
  context under `apiextensions.crossplane.io/extra-resources` for later
  pipeline steps.[^readme-extraresources-behavior]
- `getCredentialData` returns byte data for a named credential present in the request.[^getcredentialdata-implementation]

The credential helper is present in released code and examples but omitted from the README's additional-functions table. See [template functions](template-functions.md) for the complete released helper list.

Feature maturity is **Not stated by selected sources**. Older, unverified reports about request data and extra resources are recorded separately in [project history](project-history.md).

[^readme-request-data]: [README request data](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73)
[^readme-context-resource]: [README Context resource](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277)
[^readme-extraresources-behavior]: [README ExtraResources behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L239)
[^getcredentialdata-implementation]: [getCredentialData implementation](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L177)
