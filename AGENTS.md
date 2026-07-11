# Repository guidance

This repository contains an Open Knowledge Format (OKF) knowledge bundle for the Crossplane v2 ecosystem.

## Default behavior

- Do not start the OKF generation or enrichment workflow automatically.
- Run the workflow only when the user explicitly invokes `$okf`.
- Keep this file limited to repository-wide rules. The workflow lives in `.agents/skills/okf/`, and specialist behavior lives in `.codex/agents/`.

## Ownership

- The root agent owns planning, source selection, file edits, validation, commits, and pull request updates.
- Subagents are read-only researchers. They return compact evidence packets and never edit the catalog.
- Use at most three direct subagents at once. Do not create nested subagent trees.

## Evidence rules

- Use source code, API types, generated schemas, tests, and package metadata to establish API shape and runtime behavior.
- Use official Crossplane documentation to establish documented terminology, guidance, supported workflows, and versioned user-facing examples.
- Treat third-party examples as illustrative. They may describe their own implementation but must not be the sole evidence for general Crossplane behavior or recommended practice.
- Corroborate reusable third-party patterns with primary sources or official documentation.
- Verify licensing and attribution before copying or adapting third-party material. Otherwise summarize and cite it.
- Pin every source repository to an immutable commit before generating knowledge.
- Cite source files with commit-pinned GitHub URLs and line ranges whenever practical.
- Do not convert assumptions, name similarity, or undocumented behavior into facts.
- For Upjet resources, do not infer a Terraform mapping from names alone. Require Upjet configuration or generated metadata that identifies the Terraform resource.
- Preserve disagreements between source code and documentation as explicit notes instead of silently choosing one.

## Output rules

- Generated knowledge belongs under `catalog/`.
- Every non-reserved OKF Markdown document must contain parseable YAML frontmatter with a non-empty `type` field.
- `index.md` and `log.md` follow the OKF reserved-file rules.
- Prefer small concept documents, structural Markdown, progressive disclosure, and citations over broad narrative pages.
