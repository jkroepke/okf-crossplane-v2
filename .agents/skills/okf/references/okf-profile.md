# Crossplane OKF profile

This profile adds authoring guidance on top of OKF v0.3. Where it is stricter
than the specification, the stricter rule applies to this catalog.

## Required by OKF v0.3

- Every frontmatter block parses as a YAML 1.2 mapping. Producers must not
  write duplicate keys (§4).
- `index.md` and `log.md` follow their reserved roles: only the bundle-root
  `index.md` has frontmatter, and `log.md` never has frontmatter.

OKF v0.3 treats a `.md` file without frontmatter or without `type` as a
non-concept, not as an error. This catalog is stricter: every non-reserved
Markdown file under `catalog/` is a concept with a non-empty `type`.

## Bundle metadata

The bundle-root `catalog/index.md` frontmatter holds `okf_version: "0.3"`,
`title`, `description`, and `license: Apache-2.0`. Keep these keys when you
regenerate or edit the root index.

## Recommended frontmatter

```yaml
---
type: Crossplane Function
title: function-go-templating
description: One sentence supported by the cited sources.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, function]
generated: { by: "process:crossplane-okf-generation", at: "2026-07-11T00:00:00Z" }
sources:
  - id: package-metadata
    resource: https://github.com/crossplane-contrib/function-go-templating/blob/<full-SHA>/package/crossplane.yaml
    title: Function package metadata
source_repository: crossplane-contrib/function-go-templating
source_commit: <full SHA>
source_paths:
  - package/crossplane.yaml
---
```

Use extension fields only when populated by evidence. Preserve unknown fields.
Existing extension keys such as `source_commit` and `feature_state` keep their
names. OKF v0.3 recommends `x-<producer>-<name>` for producer keys, because future
OKF versions will not define keys that start with `x-`, and the validator reports unprefixed keys as
info only.

Use the OKF actor convention for `generated.by`, `verified[].by`, and
`sources[].author`: `<producer>/<version>` for tools or agents,
`process:<id>` for automated processes, `team:<id>` for groups, and
`human:<id>` for people. Omit `verified` unless the recorded verification
actually occurred; each event needs both `by` and `at`, and it counts only
while its `at` is not older than `generated.at`.

`generated.at` is the last meaningful change to the content. Do not change it
for formatting, whitespace, or link repairs. Quote every OKF timestamp and
write it as an RFC 3339 date-time with an offset, for example
`"2026-11-22T00:00:00Z"`.

An absent `status` means `stable`; do not add lifecycle or staleness metadata
without evidence. Use only `draft`, `stable`, or `deprecated`. To retire or
move a concept, keep a short `status: deprecated` concept at the old path with
`superseded_by` set to the replacement path.

## Links and path fields

A link target or path field (`resource`, `sources[].resource`,
`superseded_by`, and for an Attested Computation `computation`,
`executor.resource`, and `attester.resource`) without a leading `/` resolves from the directory of the file
that contains it. A leading `/` resolves from the bundle root (`catalog/`).
Prefer relative links such as `../core/composition.md`. Never write a
bundle-root path without the leading `/`. Use only `[text](target)` links;
`[[wikilinks]]` are not OKF links.

## Body dialect

Write CommonMark with GFM tables and `[^label]` footnotes. Do not depend on
other Markdown extensions.

## Preferred concept types

- `Crossplane Core Concept`
- `Crossplane API`
- `Crossplane CLI Command`
- `Crossplane Provider`
- `Crossplane Managed Resource`
- `Crossplane Function`
- `Crossplane Function Input`
- `Crossplane Development Guide`
- `Crossplane Test Tool`
- `Crossplane Example`
- `Terraform Resource Reference`
- `Reference`

These values are conventions, not a closed taxonomy.

## Body structure

Use only sections that add evidence-backed value:

- `# Overview`
- `# Schema`
- `# Behavior`
- `# Examples`
- `# Computation` for an `Attested Computation`
- `# Relationships`
- `# Limitations`

Put provenance in frontmatter `sources`, with one concrete `resource` per entry.
Give claim-bearing entries stable `id` values and attribute claims with matching
keyed Markdown footnotes, for example `[^package-metadata]`. Footnote definitions
may repeat the human-readable source link. Prefer commit-pinned GitHub blob URLs
with line anchors. Do not emit the superseded v0.1 `# Citations` section or
`timestamp` field.

## Granularity

- One independently useful concept per file.
- Keep package knowledge separate from API schema, runtime behavior, and examples.
- Do not mirror every generated type by default. Generate at resource level only when requested or when the resource is needed by another concept.
- Use `index.md` for progressive disclosure instead of large overview pages.
