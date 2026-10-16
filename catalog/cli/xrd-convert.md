---
type: Crossplane CLI Command
title: Convert an XRD to CRDs or JSON Schema
description: Use the Beta crossplane xrd convert command to inspect the CRD derived from an XRD or, from CLI v2.5.0, emit JSON Schema for YAML language server validation.
resource: https://github.com/crossplane/cli
tags: [crossplane, cli, xrd, json-schema, authoring]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T20:15:00Z" }
sources:
  - id: xrd-group-beta
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/main.go#L88'
    title: 'xrd command group maturity label'
  - id: convert-docs-beta-and-purpose
    resource: 'https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L2668-L2686'
    title: 'CLI v2.5 xrd convert Beta label and purpose'
  - id: convert-docs-jsonschema-examples
    resource: 'https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L2717-L2727'
    title: 'CLI v2.5 JSON Schema examples'
  - id: convert-docs-flags
    resource: 'https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L2742-L2750'
    title: 'CLI v2.5 xrd convert flags'
  - id: convert-flags
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert.go#L52-L64'
    title: 'xrd convert arguments and flags'
  - id: convert-format-routing
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert.go#L100-L144'
    title: 'CRD and JSON Schema output selection and file names'
  - id: convert-output-writing
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert.go#L146-L184'
    title: 'Output directory, file, and stdout writing'
  - id: jsonschema-id-and-gvk
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/json.go#L96-L126'
    title: 'JSON Schema $id and GVK metadata'
  - id: jsonschema-per-version
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/json.go#L128-L163'
    title: 'One JSON Schema per CRD version'
  - id: jsonschema-additional-properties
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/json.go#L165-L205'
    title: 'YAML language server compatibility mutation'
  - id: convert-tests
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert_test.go#L109-L181'
    title: 'Single-schema JSON Schema conversion test'
documentation_series: cli-v2.5
documentation_repository: crossplane/docs
documentation_commit: d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d
documentation_paths: [content/cli/v2.5/command-reference.md]
source_repository: crossplane/cli
source_tag: v2.5.0
source_commit: 1acb525095a4e43c9a765954efa66a47667a432b
source_paths: [cmd/crossplane/main.go, cmd/crossplane/xrd/convert.go, cmd/crossplane/xrd/convert_test.go, internal/schemas/generator/json.go]
feature_state: Beta
feature_state_basis: The CLI source tags the xrd command group maturity beta, and the CLI v2.5 command reference labels xrd convert [BETA].
---

# Overview

`crossplane xrd convert` converts a CompositeResourceDefinition into the
CustomResourceDefinition that Crossplane derives from it internally. The
documentation names inspecting the generated CRD shape, feeding tooling that
does not understand XRDs, and debugging as uses. A Namespaced or Cluster-scoped
XRD yields one CRD for the XR.[^convert-docs-beta-and-purpose]

The command is Beta: the `xrd` command group is tagged `maturity:"beta"`, and
the v2.5 reference warns that Beta features may change.[^xrd-group-beta][^convert-docs-beta-and-purpose]
Its CLI-side behavior is separate from Crossplane Core; see the
[XRD concept](../core/composite-resource-definition.md) for the API itself.

# Usage

| Input or flag | Behavior |
|---|---|
| `[<input-file>]` | XRD YAML file, or `-` for stdin (the default).[^convert-flags] |
| `-o`, `--output-file` | Write to one file. Mutually exclusive with `--output-dir`.[^convert-flags] |
| `--output-dir` | Write one file per output.[^convert-flags][^convert-output-writing] |
| `--format` | `crd` (default) or `jsonschema`. New in CLI v2.5.0.[^convert-flags][^convert-docs-flags] |

Without an output flag, the result goes to stdout.[^convert-output-writing]

# JSON Schema output

With `--format=jsonschema`, the command writes JSON Schema for the YAML
language server instead of CRDs.[^convert-flags][^convert-docs-jsonschema-examples]

- Every version of each derived CRD that has an `openAPIV3Schema` becomes one
  pretty-printed JSON Schema document. A test parses single-schema output as JSON Schema with `$id` set.[^jsonschema-per-version][^convert-tests]
- Each schema gets `$id` `<group>/<version>/<lowercase kind>.json` and an
  `x-kubernetes-group-version-kind` entry.[^jsonschema-id-and-gvk]
- With `--output-dir`, files are named `<group>_<version>_<lowercase kind>.json`.[^convert-format-routing][^convert-output-writing]
- Stdout and `-o` accept exactly one schema. More than one fails with
  "cannot write N JSON Schemas to a single output; use --output-dir".[^convert-output-writing]
  Inferred: an XRD that serves several versions therefore needs `--output-dir`.
- Every `type: object` schema without an explicit `additionalProperties` gets
  `additionalProperties: false`, applied recursively.[^jsonschema-additional-properties]

The documented examples are `crossplane xrd convert xrd.yaml --format=jsonschema`
for stdout and `crossplane xrd convert xrd.yaml --format=jsonschema --output-dir ./schemas/`
for files.[^convert-docs-jsonschema-examples]

# Limitations

- The `-o` help text and the v2.5 flag table still describe CRD YAML, and the
  flag table shows only `--format="crd"` without listing `jsonschema`. The
  source enum `crd,jsonschema` is authoritative.[^convert-docs-flags][^convert-flags]
- The selected sources do not show how to configure a YAML language server to
  use the schemas, or how the forced `additionalProperties: false` interacts
  with fields that preserve unknown fields. Treat both as unresolved.
- Legacy XRD and Claim CRD output was excluded from this concept.

# Relationships

Generate an XRD with the [control plane project](control-plane-projects.md)
workflow, and test the Composition with
[local rendering](local-composition-rendering.md).

[^xrd-group-beta]: [`xrd` command group maturity label](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/main.go#L88)
[^convert-docs-beta-and-purpose]: [CLI v2.5 `xrd convert` Beta label and purpose](https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L2668-L2686)
[^convert-docs-jsonschema-examples]: [CLI v2.5 JSON Schema examples](https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L2717-L2727)
[^convert-docs-flags]: [CLI v2.5 `xrd convert` flags](https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L2742-L2750)
[^convert-flags]: [`xrd convert` arguments and flags](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert.go#L52-L64)
[^convert-format-routing]: [CRD and JSON Schema output selection and file names](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert.go#L100-L144)
[^convert-output-writing]: [Output directory, file, and stdout writing](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert.go#L146-L184)
[^jsonschema-id-and-gvk]: [JSON Schema `$id` and GVK metadata](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/json.go#L96-L126)
[^jsonschema-per-version]: [One JSON Schema per CRD version](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/json.go#L128-L163)
[^jsonschema-additional-properties]: [YAML language server compatibility mutation](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/json.go#L165-L205)
[^convert-tests]: [Single-schema JSON Schema conversion test](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/xrd/convert_test.go#L109-L181)
