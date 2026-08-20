# Crossplane OKF profile

This profile adds authoring guidance without narrowing OKF v0.2 conformance.

## Required by OKF v0.2

- Every non-reserved Markdown concept has parseable YAML frontmatter.
- Every concept has a non-empty `type`.
- `index.md` and `log.md` follow their reserved roles.

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

Use the OKF actor convention for `generated.by` and `verified[].by`:
`<producer>/<version>` for tools or agents, `process:<id>` for automated
processes, and `human:<id>` for people. Omit `verified` unless the recorded
verification actually occurred. An absent `status` means `stable`; do not add
lifecycle or staleness metadata without evidence.

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
