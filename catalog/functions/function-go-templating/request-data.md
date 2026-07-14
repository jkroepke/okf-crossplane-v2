---
type: function
title: Template request data and pipeline context
description: Read observed and desired state, context, extra resources, and credentials from templates.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, context, extra-resources]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Behavior

Templates receive the function's `RunFunctionRequest`, including observed and desired composite and composed resources, pipeline context, and fetched extra resources.[1]

- Rendering the special [`Context`](context.md) instruction deeply merges data
  into response context for later pipeline steps.[2]
- [`ExtraResources`](extra-resources.md) requests can match resources by name or
  labels. Results are available in the current request and are merged into
  context under `apiextensions.crossplane.io/extra-resources` for later
  pipeline steps.[3]
- `getCredentialData` returns byte data for a named credential present in the request.[4]

The credential helper is present in released code and examples but omitted from the README's additional-functions table. See [template functions](template-functions.md) for the complete released helper list.

Feature maturity is **Not stated by selected sources**. Older, unverified reports about request data and extra resources are recorded separately in [project history](project-history.md).

# Citations

[1] [README request data](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73)
[2] [README Context resource](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277)
[3] [README ExtraResources behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L239)
[4] [getCredentialData implementation](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L177)
