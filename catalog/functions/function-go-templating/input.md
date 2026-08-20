---
type: functioninput
title: GoTemplate input
description: Schema and source modes for gotemplating.fn.crossplane.io/v1beta1 GoTemplate input.
resource: https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml
tags: [crossplane, composition-function, schema]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: generated-gotemplate-crd
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L94'
    title: 'Generated GoTemplate CRD'
  - id: inline-validation-rules
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L56-L69'
    title: 'Inline validation rules'
  - id: delimiter-schema-and-defaults
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L31-L42'
    title: 'Delimiter schema and defaults'
  - id: readme-source-modes
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L59'
    title: 'README source modes'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Beta
feature_state_basis: The generated CRD serves and stores only gotemplating.fn.crossplane.io/v1beta1.
---

# Schema

The generated CRD serves and stores `gotemplating.fn.crossplane.io/v1beta1`. Its accepted fields are `source`, `inline`, `fileSystem`, `environment`, `delims`, and `options`; only `source` is globally required.[^generated-gotemplate-crd]

| Field | Shape and constraint |
|---|---|
| `source` | Required string. The schema does not enumerate values or enforce correspondence with a source object. |
| `inline.template` | One string containing one or more YAML documents. |
| `inline.templates` | Array of template strings. Exactly one of `template` and `templates` is required when `inline` is present.[^inline-validation-rules] |
| `fileSystem.dirPath` | Directory whose files supply templates. |
| `environment.key` | Context key whose value supplies templates. |
| `delims.left`, `delims.right` | Custom delimiters; defaults are `{{` and `}}`.[^delimiter-schema-and-defaults] |
| `options` | Top-level array of Go `text/template` option strings.[^generated-gotemplate-crd] |

# Source modes

The README documents Inline, FileSystem, and Environment loading. Inline accepts either a multi-document `template` or multiple `templates`; FileSystem loads beneath `dirPath`; Environment reads the context value at `environment.key`.[^readme-source-modes]

# Limitations

The README example nests `options` beneath `inline`, but the generated CRD places it at the top level.
Follow the generated schema.
The only bundled FileSystem example depends on excluded legacy Claim/XRD semantics, so this catalog does not present it as a runnable v2 example.

The overall input is Beta because its only served and stored version is `v1beta1`. Capabilities implemented through separate `v1alpha1` meta instructions, such as Context, retain their Alpha ceilings.

[^generated-gotemplate-crd]: [Generated GoTemplate CRD](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L94)
[^inline-validation-rules]: [Inline validation rules](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L56-L69)
[^delimiter-schema-and-defaults]: [Delimiter schema and defaults](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L31-L42)
[^readme-source-modes]: [README source modes](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L59)
