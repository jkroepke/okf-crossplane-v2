# Repository guidance

This repository contains an Open Knowledge Format (OKF) knowledge bundle for the Crossplane v2 ecosystem.

## Default behavior

- Do not start the OKF generation or enrichment workflow automatically.
- Run the workflow only when the user explicitly invokes `$okf`, `/skill:okf`, or `/okf`.
- Keep this file limited to repository-wide rules. The shared workflow lives in `.agents/skills/okf/`; runtime-specific specialist definitions live in `.codex/agents/` and `.pi/agents/`.

## Ownership

- The root or parent agent owns planning, source selection, file edits, validation, commits, and pull request updates.
- Subagents are read-only researchers. They return compact evidence packets and never edit the catalog.
- Use at most three direct subagents at once. Do not create nested subagent trees.
- When running in Pi, use only the project agents whose names start with `okf-`. Their tool allowlists intentionally omit editing tools and nested delegation.

## Domain routing

- Use `okf-crossplane-core-docs-researcher` for current stable Crossplane Core documentation.
- Use `okf-crossplane-core-code-researcher` for current stable Crossplane Core CRDs under `cluster/crds`.
- Use `okf-function-go-templating-researcher` only for `crossplane-contrib/function-go-templating`.
- Every composition function must have its own matching Codex and Pi researcher set before its OKF concepts are generated.
- Use the generic `okf-crossplane-researcher` only for domains without a dedicated agent, such as CLI, runtime, SDKs, tools, native providers, and testing tools.
- The Crossplane CLI is a separate catalog domain and is not part of Crossplane Core.

## Evidence rules

- Use source code, API types, generated schemas, tests, and package metadata to establish API shape and runtime behavior.
- Use official Crossplane documentation to establish documented terminology, guidance, supported workflows, lifecycle states, and versioned user-facing examples.
- Resolve the latest stable Crossplane release before Core research and use the matching stable documentation major.minor series.
- Record Alpha, Beta, Stable, or Deprecated only with direct source evidence. Never infer feature maturity from API version names.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1, legacy v1 XR semantics, and sections explicitly labelled `v1 Composite Resources (Legacy)` from legacy-free output.
- Do not treat every `apiextensions.crossplane.io/v1` resource as legacy. Require explicit deprecation metadata or a legacy label.
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
