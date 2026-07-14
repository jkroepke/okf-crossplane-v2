---
type: functioninput
title: GoTemplate input
description: Schema and source modes for gotemplating.fn.crossplane.io/v1beta1 GoTemplate input.
resource: https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml
tags: [crossplane, composition-function, schema]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Beta
feature_state_basis: The generated CRD serves and stores only gotemplating.fn.crossplane.io/v1beta1.
---

# Schema

The generated CRD serves and stores `gotemplating.fn.crossplane.io/v1beta1`. Its accepted fields are `source`, `inline`, `fileSystem`, `environment`, `delims`, and `options`; only `source` is globally required.[1]

| Field | Shape and constraint |
|---|---|
| `source` | Required string. The schema does not enumerate values or enforce correspondence with a source object. |
| `inline.template` | One string containing one or more YAML documents. |
| `inline.templates` | Array of template strings. Exactly one of `template` and `templates` is required when `inline` is present.[2] |
| `fileSystem.dirPath` | Directory whose files supply templates. |
| `environment.key` | Context key whose value supplies templates. |
| `delims.left`, `delims.right` | Custom delimiters; defaults are `{{` and `}}`.[3] |
| `options` | Top-level array of Go `text/template` option strings.[1] |

# Source modes

The README documents Inline, FileSystem, and Environment loading. Inline accepts either a multi-document `template` or multiple `templates`; FileSystem loads beneath `dirPath`; Environment reads the context value at `environment.key`.[4]

# Limitations

The README example nests `options` beneath `inline`, but the generated CRD places it at the top level.
Follow the generated schema.
The only bundled FileSystem example depends on excluded legacy Claim/XRD semantics, so this catalog does not present it as a runnable v2 example.

The overall input is Beta because its only served and stored version is `v1beta1`. Capabilities implemented through separate `v1alpha1` meta instructions, such as Context, retain their Alpha ceilings.

# Citations

[1] [Generated GoTemplate CRD](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L94)
[2] [Inline validation rules](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L56-L69)
[3] [Delimiter schema and defaults](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L31-L42)
[4] [README source modes](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L59)
