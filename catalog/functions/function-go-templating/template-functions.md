---
type: reference
title: function-go-templating template functions
description: Signatures, return values, and failure behavior of the project-specific Go template helpers.
resource: https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go
tags: [crossplane, composition-function, template-functions]
timestamp: 2026-07-14T00:00:00Z
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

`function-go-templating` v0.12.2 adds the following helpers to Go templates.[1]

## Serialization and selection

- `randomChoice choices...` takes one or more strings and returns one. It uses a
  new time-seeded, non-cryptographic pseudo-random generator. Calling it with no
  arguments fails during template execution because the implementation cannot
  select from an empty list.[2]
- `toYaml value` marshals any value with `gopkg.in/yaml.v3` and returns
  `(string, error)`. A marshal error stops template execution.[2]
- `fromYaml string` unmarshals YAML into a dynamically typed value and returns
  `(value, error)`. Invalid YAML stops template execution.[2]

## Resource access

- `getResourceCondition type resource` reads conditions first from
  `resource.status`, which matches an observed-resource wrapper, then from
  top-level `status`, which matches a raw resource. A missing path or condition
  returns the Crossplane runtime's empty condition with status `Unknown`.[3]
- `setResourceNameAnnotation name` returns the YAML mapping line
  `gotemplating.fn.crossplane.io/composition-resource-name: <name>`. It is
  intended for use beneath `metadata.annotations`; it does not mutate an
  object.[4] This function-specific annotation selects the desired-map key.[14]
  Crossplane Core persists a separate `crossplane.io/composition-resource-name`
  annotation on the actual object; neither annotation is `metadata.name`.[12][13]
- `getComposedResource request name` reads
  `observed.resources[<name>].resource` and returns a resource map or `nil` when
  the named observed composed resource or path is absent.[5]
- `getCompositeResource request` reads `observed.composite.resource` and
  returns a resource map or `nil` when the path is absent.[5]

## Request data

- `getExtraResources request name` reads `requiredResources[<name>].items`
  first, then the deprecated-compatible `extraResources[<name>].items` path. It
  returns a list or `nil` when neither path exists.[6]
- `getExtraResourcesFromContext request name` reads
  `context[apiextensions.crossplane.io/extra-resources][<name>].items`. It
  returns a list or `nil` when that context entry is absent.[6]
- `getCredentialData request credentialName` converts the template data back to
  a function request. It returns the named credential's `map[string][]byte`
  only when its source is `CredentialData`; conversion failure, a missing
  credential, or another source returns `nil`.[7]

## Template inclusion

- `include name data` executes the named template into a string and returns
  `(string, error)`. It tracks nesting per template name, sets
  `recursionMaxNums` to 1,000, and rejects when the recorded depth is already
  greater than 1,000 before the next increment.[8]

The [ExtraResources capability](extra-resources.md) explains how requirements are declared and how the two extra-resource access helpers differ.

# Sprig boundary

The release depends on Sprig `v3.3.0`.[9] It starts with Sprig's general
function map and deletes `env` and `expandenv` because the source identifies an
information-leakage risk.[10] See the versioned [Sprig reference](sprig.md) for
the retained capability groups.

# Limitations

- Maturity of these implementation-provided helpers is **Not stated by selected
  sources**. The selected stable release tag pins evidence but is not a product
  lifecycle label.
- `randomChoice` is nondeterministic and is not suitable for cryptographic selection.[2]
- Lookup helpers intentionally collapse malformed or missing paths to `nil` (or an `Unknown` condition), so templates that must distinguish those cases need explicit validation.[3][5][6]
- `getCredentialData` is implemented in the selected release but is omitted from its README helper table.[7][11]

# Citations

[1] [Project-specific function map](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L38)
[2] [`randomChoice`, `toYaml`, and `fromYaml` implementations](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L67-L87)
[3] [`getResourceCondition` lookup behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L89-L99)
[4] [`setResourceNameAnnotation` output](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103)
[5] [Observed composed and composite resource lookups](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L141)
[6] [Direct and context extra-resource lookups](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L164)
[7] [`getCredentialData` conversion and source handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L190)
[8] [`include` recursion handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L105-L121)
[9] [Pinned Sprig dependency](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L10)
[10] [Removed environment functions](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62)
[11] [Selected-release additional-functions table](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L393-L410)
[12] [Core composition-resource annotation key](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)
[13] [Core persists the logical resource key on the rendered object](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100)
[14] [Function consumes the annotation as the desired resource-map key](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)
