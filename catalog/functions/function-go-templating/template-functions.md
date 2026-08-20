---
type: reference
title: function-go-templating template functions
description: Signatures, return values, and failure behavior of the project-specific Go template helpers.
resource: https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go
tags: [crossplane, composition-function, template-functions]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: project-specific-function-map
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L38'
    title: 'Project-specific function map'
  - id: randomchoice-toyaml-and-fromyaml-implementations
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L67-L87'
    title: 'randomChoice, toYaml, and fromYaml implementations'
  - id: getresourcecondition-lookup-behavior
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L89-L99'
    title: 'getResourceCondition lookup behavior'
  - id: setresourcenameannotation-output
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103'
    title: 'setResourceNameAnnotation output'
  - id: observed-composed-and-composite-resource-lookups
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L141'
    title: 'Observed composed and composite resource lookups'
  - id: direct-and-context-extra-resource-lookups
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L164'
    title: 'Direct and context extra-resource lookups'
  - id: getcredentialdata-conversion-and-source-handling
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L190'
    title: 'getCredentialData conversion and source handling'
  - id: include-recursion-handling
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L105-L121'
    title: 'include recursion handling'
  - id: pinned-sprig-dependency
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L10'
    title: 'Pinned Sprig dependency'
  - id: removed-environment-functions
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62'
    title: 'Removed environment functions'
  - id: selected-release-additional-functions-table
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L393-L410'
    title: 'Selected-release additional-functions table'
  - id: core-composition-resource-annotation-key
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40'
    title: 'Core composition-resource annotation key'
  - id: core-persists-the-logical-resource-key-on-the-rendered-object
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100'
    title: 'Core persists the logical resource key on the rendered object'
  - id: function-consumes-the-annotation-as-the-desired-resource-map-key
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350'
    title: 'Function consumes the annotation as the desired resource-map key'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths:
  - function_maps.go
  - fn.go
  - README.md
  - example/functions
supporting_source_repository: crossplane/crossplane-runtime
supporting_source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
supporting_source_paths: [pkg/xcrd/composite.go]
crossplane_source_repository: crossplane/crossplane
crossplane_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
crossplane_source_paths: [internal/controller/apiextensions/composite/composition_render.go]
feature_state: Not stated by selected sources
---

# Functions

`function-go-templating` v0.12.2 adds the following helpers to Go templates.[^project-specific-function-map]

## Serialization and selection

- `randomChoice choices...` takes one or more strings and returns one. It uses a
  new time-seeded, non-cryptographic pseudo-random generator. Calling it with no
  arguments fails during template execution because the implementation cannot
  select from an empty list.[^randomchoice-toyaml-and-fromyaml-implementations]
- `toYaml value` marshals any value with `gopkg.in/yaml.v3` and returns
  `(string, error)`. A marshal error stops template execution.[^randomchoice-toyaml-and-fromyaml-implementations]
- `fromYaml string` unmarshals YAML into a dynamically typed value and returns
  `(value, error)`. Invalid YAML stops template execution.[^randomchoice-toyaml-and-fromyaml-implementations]

## Resource access

- `getResourceCondition type resource` reads conditions first from
  `resource.status`, which matches an observed-resource wrapper, then from
  top-level `status`, which matches a raw resource. A missing path or condition
  returns the Crossplane runtime's empty condition with status `Unknown`.[^getresourcecondition-lookup-behavior]
- `setResourceNameAnnotation name` returns the YAML mapping line
  `gotemplating.fn.crossplane.io/composition-resource-name: <name>`. It is
  intended for use beneath `metadata.annotations`; it does not mutate an
  object.[^setresourcenameannotation-output] This function-specific annotation selects the desired-map key.[^function-consumes-the-annotation-as-the-desired-resource-map-key]
  Crossplane Core persists a separate `crossplane.io/composition-resource-name`
  annotation on the actual object; neither annotation is `metadata.name`.[^core-composition-resource-annotation-key][^core-persists-the-logical-resource-key-on-the-rendered-object]
- `getComposedResource request name` reads
  `observed.resources[<name>].resource` and returns a resource map or `nil` when
  the named observed composed resource or path is absent.[^observed-composed-and-composite-resource-lookups]
- `getCompositeResource request` reads `observed.composite.resource` and
  returns a resource map or `nil` when the path is absent.[^observed-composed-and-composite-resource-lookups]

## Request data

- `getExtraResources request name` reads `requiredResources[<name>].items`
  first, then the deprecated-compatible `extraResources[<name>].items` path. It
  returns a list or `nil` when neither path exists.[^direct-and-context-extra-resource-lookups]
- `getExtraResourcesFromContext request name` reads
  `context[apiextensions.crossplane.io/extra-resources][<name>].items`. It
  returns a list or `nil` when that context entry is absent.[^direct-and-context-extra-resource-lookups]
- `getCredentialData request credentialName` converts the template data back to
  a function request. It returns the named credential's `map[string][]byte`
  only when its source is `CredentialData`; conversion failure, a missing
  credential, or another source returns `nil`.[^getcredentialdata-conversion-and-source-handling]

## Template inclusion

- `include name data` executes the named template into a string and returns
  `(string, error)`. It tracks nesting per template name, sets
  `recursionMaxNums` to 1,000, and rejects when the recorded depth is already
  greater than 1,000 before the next increment.[^include-recursion-handling]

The [ExtraResources capability](extra-resources.md) explains how requirements are declared and how the two extra-resource access helpers differ.

# Sprig boundary

The release depends on Sprig `v3.3.0`.[^pinned-sprig-dependency] It starts with Sprig's general
function map and deletes `env` and `expandenv` because the source identifies an
information-leakage risk.[^removed-environment-functions] See the versioned [Sprig reference](sprig.md) for
the retained capability groups.

# Limitations

- Maturity of these implementation-provided helpers is **Not stated by selected
  sources**. The selected stable release tag pins evidence but is not a product
  lifecycle label.
- `randomChoice` is nondeterministic and is not suitable for cryptographic selection.[^randomchoice-toyaml-and-fromyaml-implementations]
- Lookup helpers intentionally collapse malformed or missing paths to `nil` (or an `Unknown` condition), so templates that must distinguish those cases need explicit validation.[^getresourcecondition-lookup-behavior][^observed-composed-and-composite-resource-lookups][^direct-and-context-extra-resource-lookups]
- `getCredentialData` is implemented in the selected release but is omitted from its README helper table.[^getcredentialdata-conversion-and-source-handling][^selected-release-additional-functions-table]

[^project-specific-function-map]: [Project-specific function map](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L38)
[^randomchoice-toyaml-and-fromyaml-implementations]: [`randomChoice`, `toYaml`, and `fromYaml` implementations](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L67-L87)
[^getresourcecondition-lookup-behavior]: [`getResourceCondition` lookup behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L89-L99)
[^setresourcenameannotation-output]: [`setResourceNameAnnotation` output](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103)
[^observed-composed-and-composite-resource-lookups]: [Observed composed and composite resource lookups](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L141)
[^direct-and-context-extra-resource-lookups]: [Direct and context extra-resource lookups](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L164)
[^getcredentialdata-conversion-and-source-handling]: [`getCredentialData` conversion and source handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L190)
[^include-recursion-handling]: [`include` recursion handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L105-L121)
[^pinned-sprig-dependency]: [Pinned Sprig dependency](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L10)
[^removed-environment-functions]: [Removed environment functions](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62)
[^selected-release-additional-functions-table]: [Selected-release additional-functions table](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L393-L410)
[^core-composition-resource-annotation-key]: [Core composition-resource annotation key](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)
[^core-persists-the-logical-resource-key-on-the-rendered-object]: [Core persists the logical resource key on the rendered object](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100)
[^function-consumes-the-annotation-as-the-desired-resource-map-key]: [Function consumes the annotation as the desired resource-map key](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
