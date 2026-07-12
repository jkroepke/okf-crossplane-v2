# Repository guidance

This repository contains an Open Knowledge Format (OKF) knowledge bundle for the Crossplane v2 ecosystem.

## Default behavior

- Do not start the OKF generation or enrichment workflow automatically.
- Run the workflow only when the user explicitly invokes `$okf`, `/skill:okf`, or `/okf`.
- Keep this file limited to repository-wide rules. The shared workflow lives in `.agents/skills/okf/`.
- Canonical specialist instructions live in `.agents/agents/<name>/AGENT.md`.
- Runtime adapters in `.codex/agents/` and `.pi/agents/` contain only runtime metadata and a reference to the matching canonical instruction file. Do not duplicate role instructions in runtime adapters.

## Ownership

- The root or parent agent owns planning, source selection, file edits, validation, commits, and pull request updates.
- Subagents are read-only researchers. They return compact evidence packets and never edit the catalog.
- Use at most three direct subagents at once. Do not create nested subagent trees.
- When running in Pi, use only the project agents whose names start with `okf-`. Their tool allowlists intentionally omit editing tools and nested delegation.

## Change workflow

- For every content addition or update, create a new dedicated branch from the latest default branch before editing. Never add or update content directly on the default branch.
- Keep the complete related change set on that branch, including catalog documents, source locks, claim ledgers, indexes, logs, and required agent or source-profile changes.
- Run deterministic validation and the `okf-reviewer` before committing the changes.
- Resolve all blocking review findings and rerun targeted validation. Continue only after the reviewer returns `APPROVED`.
- After the final review fixes, run `mise run lint` before creating any commit. Fix every lint error and rerun the command until it succeeds.
- After reviewer approval and a successful lint run, commit every intended change. Do not leave generated or supporting files uncommitted.
- Push the branch and open a pull request for the reviewed commit set. Do not merge the pull request unless the user explicitly requests it.

## Domain routing

- Use `okf-crossplane-core-docs-researcher` for current stable Crossplane Core documentation.
- Use `okf-crossplane-core-code-researcher` for current stable Crossplane Core CRDs under `cluster/crds`.
- Use `okf-function-go-templating-researcher` for user-facing `function-go-templating` installation, input schema, examples, and additional template functions.
- Use `okf-function-go-templating-sprig-researcher` for the exact Sprig version exposed by the selected stable `function-go-templating` release.
- Use `okf-function-go-templating-project-history-researcher` for human-authored issues and pull requests related to that function.
- Every composition function must have its own canonical instruction files and matching Codex and Pi adapters before its OKF concepts are generated.
- Use the generic `okf-crossplane-researcher` only for domains without a dedicated agent, such as CLI, runtime, SDKs, tools, native providers, and testing tools.
- The Crossplane CLI is a separate catalog domain and is not part of Crossplane Core.

## Evidence rules

- Use source code, API types, generated schemas, tests, and package metadata to establish API shape and runtime behavior.
- Use official Crossplane documentation to establish documented terminology, guidance, supported workflows, lifecycle states, and versioned user-facing examples.
- Resolve the latest stable Crossplane release before Core research and use the matching stable documentation major.minor series.
- Resolve the highest stable semantic-version tag before researching a composition function. Do not assume a sample tag and do not silently fall back to `main`.
- Treat a feature as Stable unless selected sources explicitly label it Alpha, Beta, Preview, or Deprecated. Require direct source evidence for every non-stable label.
- Never infer feature maturity from API version names such as `v1alpha1`, `v1beta1`, or `v1`.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1, legacy v1 XR semantics, and sections explicitly labelled `v1 Composite Resources (Legacy)` from legacy-free output.
- Do not treat every `apiextensions.crossplane.io/v1` resource as legacy. Require explicit deprecation metadata or a legacy label.
- Project-history evidence must exclude bots and apps and record a research timestamp.
- Open issues are reports. Open or unmerged pull requests are proposals. Neither establishes released behavior.
- A merged pull request belongs to a selected release only when its merge commit is contained in that release tag. A closed issue is not automatically fixed.
- Treat third-party examples as illustrative. They may describe their own implementation but must not be the sole evidence for general Crossplane behavior or recommended practice.
- Corroborate reusable third-party patterns with primary sources or official documentation.
- Verify licensing and attribution before copying or adapting third-party material. Otherwise summarize and cite it.
- Pin every released source repository to an immutable commit before generating knowledge.
- Cite source files with commit-pinned GitHub URLs and line ranges whenever practical.
- Do not convert assumptions, name similarity, issue reports, proposals, or undocumented behavior into facts.
- For Upjet resources, do not infer a Terraform mapping from names alone. Require Upjet configuration or generated metadata that identifies the Terraform resource.
- Preserve disagreements between source code and documentation as explicit notes instead of silently choosing one.

## Output rules

- Generated knowledge belongs under `catalog/`.
- Every non-reserved OKF Markdown document must contain parseable YAML frontmatter with a non-empty `type` field.
- `index.md` and `log.md` follow the OKF reserved-file rules.
- Prefer small concept documents, structural Markdown, progressive disclosure, and citations over broad narrative pages.