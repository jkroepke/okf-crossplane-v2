---
type: reference
title: function-go-templating template functions
description: Signatures, return values, and failure behavior of the project-specific Go template helpers.
resource: https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go
tags: [crossplane, composition-function, template-functions]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T19:00:00Z" }
sources:
  - id: project-specific-function-map
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L24-L38'
    title: 'Project-specific function map'
  - id: randomchoice-toyaml-and-fromyaml-implementations
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L68-L88'
    title: 'randomChoice, toYaml, and fromYaml implementations'
  - id: getresourcecondition-lookup-behavior
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L90-L100'
    title: 'getResourceCondition lookup behavior'
  - id: setresourcenameannotation-output
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L102-L104'
    title: 'setResourceNameAnnotation output'
  - id: observed-composed-and-composite-resource-lookups
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L125-L142'
    title: 'Observed composed and composite resource lookups'
  - id: direct-and-context-extra-resource-lookups
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L154-L175'
    title: 'Direct and context extra-resource lookups'
  - id: getcomposedconnectiondetails-lookup
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L144-L152'
    title: 'getComposedConnectionDetails lookup'
  - id: getcomposedconnectiondetails-tests
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps_test.go#L502-L589'
    title: 'getComposedConnectionDetails test cases'
  - id: getcomposedconnectiondetails-example
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/example/functions/getComposedConnectionDetails/README.md#L1-L18'
    title: 'getComposedConnectionDetails example notes'
  - id: request-map-conversion
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L432-L440'
    title: 'Request converted to template data through protojson'
  - id: getcredentialdata-conversion-and-source-handling
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L177-L203'
    title: 'getCredentialData conversion and source handling'
  - id: include-recursion-handling
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L106-L122'
    title: 'include recursion handling'
  - id: pinned-sprig-dependency
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/go.mod#L5-L7'
    title: 'Pinned Sprig dependency'
  - id: removed-environment-functions
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L57-L62'
    title: 'Removed environment functions'
  - id: selected-release-additional-functions-table
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/README.md#L399-L417'
    title: 'Selected-release additional-functions table'
  - id: core-composition-resource-annotation-key
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40'
    title: 'Core composition-resource annotation key'
  - id: core-persists-the-logical-resource-key-on-the-rendered-object
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100'
    title: 'Core persists the logical resource key on the rendered object'
  - id: function-consumes-the-annotation-as-the-desired-resource-map-key
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L382-L391'
    title: 'Function consumes the annotation as the desired resource-map key'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.13.0
source_commit: 9b7ea49394a7cef38fe517d2b60f55d64c4c8511
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

`function-go-templating` v0.13.0 adds the following helpers to Go templates.[^project-specific-function-map]

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
  returns an empty Crossplane condition with status `Unknown`.[^getresourcecondition-lookup-behavior]
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
- `getComposedConnectionDetails request name` reads
  `observed.resources[<name>].connectionDetails` and returns that map, or `nil`
  when the named observed composed resource or its connection details are
  absent. Resource names that contain dots are supported.[^getcomposedconnectiondetails-lookup][^getcomposedconnectiondetails-tests]
  The values are strings rather than bytes. They are inferred to be
  base64-encoded because the request reaches templates through a protojson
  conversion, which encodes bytes as base64, and the tests use base64
  values.[^request-map-conversion][^getcomposedconnectiondetails-tests] The helper was added in v0.13.0; see
  [connection details](connection-details.md) for the composed-Secret pattern
  it shortens.

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
- Indexing a `nil` result from `getComposedConnectionDetails`, for example
  `index $cd "username"`, renders `<no value>` under the default template
  options instead of failing. Guard each map and key before writing
  `Secret.data` (inferred from Go `text/template` behavior; not stated by
  the selected sources).
- Connection details exist only in real observed state, so the upstream
  example notes that `crossplane render` cannot simulate this helper's
  input.[^getcomposedconnectiondetails-example]
- `getCredentialData` is implemented in the selected release but is omitted from its README helper table.[^getcredentialdata-conversion-and-source-handling][^selected-release-additional-functions-table]

[^project-specific-function-map]: [Project-specific function map](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L24-L38)
[^randomchoice-toyaml-and-fromyaml-implementations]: [`randomChoice`, `toYaml`, and `fromYaml` implementations](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L68-L88)
[^getresourcecondition-lookup-behavior]: [`getResourceCondition` lookup behavior](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L90-L100)
[^setresourcenameannotation-output]: [`setResourceNameAnnotation` output](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L102-L104)
[^observed-composed-and-composite-resource-lookups]: [Observed composed and composite resource lookups](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L125-L142)
[^direct-and-context-extra-resource-lookups]: [Direct and context extra-resource lookups](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L154-L175)
[^getcredentialdata-conversion-and-source-handling]: [`getCredentialData` conversion and source handling](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L177-L203)
[^include-recursion-handling]: [`include` recursion handling](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L106-L122)
[^pinned-sprig-dependency]: [Pinned Sprig dependency](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/go.mod#L5-L7)
[^removed-environment-functions]: [Removed environment functions](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L57-L62)
[^selected-release-additional-functions-table]: [Selected-release additional-functions table](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/README.md#L399-L417)
[^core-composition-resource-annotation-key]: [Core composition-resource annotation key](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)
[^core-persists-the-logical-resource-key-on-the-rendered-object]: [Core persists the logical resource key on the rendered object](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100)
[^function-consumes-the-annotation-as-the-desired-resource-map-key]: [Function consumes the annotation as the desired resource-map key](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L382-L391)
[^getcomposedconnectiondetails-lookup]: [`getComposedConnectionDetails` lookup](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps.go#L144-L152)
[^getcomposedconnectiondetails-tests]: [`getComposedConnectionDetails` test cases](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/function_maps_test.go#L502-L589)
[^getcomposedconnectiondetails-example]: [`getComposedConnectionDetails` example notes](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/example/functions/getComposedConnectionDetails/README.md#L1-L18)
[^request-map-conversion]: [Request converted to template data through protojson](https://github.com/crossplane-contrib/function-go-templating/blob/9b7ea49394a7cef38fe517d2b60f55d64c4c8511/fn.go#L432-L440)
