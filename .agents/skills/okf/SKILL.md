---
name: okf
description: Explicit-only workflow that builds or updates a source-backed Open Knowledge Format catalog for Crossplane core, providers, functions, SDKs, tools, official documentation, and examples. Never invoke implicitly; the user must invoke `$okf`, `/skill:okf`, or `/okf`.
disable-model-invocation: true
metadata:
  version: "1.2"
  license: Apache-2.0
---

# Crossplane OKF workflow

Run this workflow only after the user explicitly invokes `$okf`, `/skill:okf`, or `/okf`. Do not treat a request that merely mentions OKF, Crossplane, a provider, or a function as permission to start this workflow.

The root or parent agent owns all writes. Subagents are bounded, read-only researchers that return evidence packets.

## Inputs

Derive the requested scope from the explicit invocation:

- source repositories or source groups
- concepts, APIs, commands, providers, functions, documentation, examples, or resource batches
- create, update, validate, or review operation
- output path, defaulting to `catalog/`

Read:

- `references/sources.yaml`
- `references/evidence-contract.md`
- `references/okf-profile.md`
- `references/okf-spec.md`

Treat the source categories in `references/sources.yaml` as separate authority roles. Do not flatten primary source, official documentation, supporting source, and third-party example evidence into one undifferentiated source list.

## Runtime adapters

The workflow and evidence contracts are shared across agent runtimes:

- Codex specialist definitions live in `.codex/agents/`.
- Pi specialist definitions live in `.pi/agents/` and are loaded through `pi-subagents`.
- Pi users may invoke the shared skill with `/skill:okf` or use the project prompt `/okf`.
- Runtime-specific agents use the same `okf-*` role names and must preserve the same read-only evidence contract.
- The root or parent agent remains the only writer regardless of runtime.

## Workflow

### 1. Bound the work

Create the smallest useful source and concept set. Do not process every repository or every managed resource unless the user explicitly requests full coverage.

For incremental work, inspect existing catalog concepts and source locks first. Regenerate only concepts affected by changed source paths or dependencies.

### 2. Pin sources

Resolve every selected repository to a full commit SHA before extracting knowledge. Record the resolved commits in `.okf/sources.lock.yaml` or update the existing lock file.

Never cite a moving branch in generated knowledge. A repository homepage may be used as the frontmatter `resource`, but evidence citations must be immutable.

### 3. Scout cheaply

Use `okf-source-scout` for repository classification and high-signal path discovery.

Batch repositories by source kind. Do not spawn one agent per repository. Prefer one scout task for up to five related repositories or one changed-source batch.

Scout official documentation and third-party examples separately from implementation repositories so their authority roles remain explicit in the evidence packet.

Skip scouting when existing locks and evidence already identify the relevant files and their source paths have not changed.

### 4. Research only what needs semantics

Use `okf-crossplane-researcher` for Crossplane core, CLI, runtime, tools, native providers, functions, SDKs, official documentation, examples, and testing tools.

Use `okf-upjet-researcher` only for Upjet provider concepts that require Terraform correlation. Give it an explicit provider service or managed-resource batch. Do not ask it to map an entire provider in one run.

For third-party example repositories, restrict research to the configured paths. Extract concrete patterns, relationships, and use cases without treating the repository as proof of general Crossplane behavior.

Run independent read-heavy research in parallel, with at most three direct agents. Wait for all required evidence packets before writing. Never allow subagents to spawn subagents.

### 5. Apply source authority

Use evidence according to its source role:

- Primary implementation sources, API types, generated schemas, tests, and package metadata establish API shape and runtime behavior.
- Official Crossplane documentation establishes documented terminology, guidance, supported workflows, and user-facing examples. When documentation conflicts with implementation or schemas, record the conflict and prefer implementation evidence for runtime behavior.
- Supporting sources provide background that is relevant only to their domain, such as Upjet generation or Terraform resource behavior.
- Third-party examples are illustrative. They may establish what that repository implements, but they must not be the sole evidence for Crossplane API semantics, runtime behavior, compatibility, security properties, or recommended practices.

Corroborate reusable patterns from third-party examples with primary sources or official documentation. Label repository-specific design choices as such.

Do not copy third-party code or configuration unless its license permits reuse and the generated concept records attribution. When the license is absent, unclear, or incompatible, summarize the pattern and cite the source instead.

### 6. Build a claim ledger

Before writing Markdown, reduce the evidence packets to a claim ledger:

- concept identifier
- exact claim
- claim class: API, behavior, documented guidance, or illustrative pattern
- source role
- supporting immutable citation
- confidence: direct, corroborated, or inferred
- version boundary
- unresolved conflict or limitation

Drop claims that do not improve the concept. Keep inferred claims clearly labelled in the final document or omit them.

### 7. Write as the root agent

Create or update OKF documents under `catalog/` according to `references/okf-profile.md`.

Rules:

- one independently useful concept per file
- structural Markdown over long prose
- package, schema, behavior, documentation guidance, and examples are separate concepts when each is useful alone
- preserve existing unknown frontmatter fields
- add natural-language cross-links, not a generic link dump
- add a numbered `# Citations` section for externally sourced claims
- update affected `index.md` files for progressive disclosure
- update `log.md` only with high-level knowledge changes
- identify third-party examples as community examples and name their originating repository
- distinguish copied examples, adapted examples, and summarized patterns

Do not copy large documentation passages. Summarize and cite.

### 8. Apply the Upjet evidence gate

For every Upjet managed-resource concept, require all of these before publishing a Terraform relationship:

- Crossplane group, version, and kind
- Upjet configuration or generated metadata naming the Terraform resource
- matching Terraform provider source, schema, or official documentation
- explicit notes for Upjet or Crossplane transformations and additions

When any link is missing, record the mapping as unresolved. Do not infer it from names.

### 9. Validate deterministically

Validate the three OKF v0.1 conformance rules:

1. Every non-reserved Markdown file has parseable YAML frontmatter.
2. Every concept frontmatter has a non-empty `type`.
3. Reserved `index.md` and `log.md` files follow their specified structures.

Also check:

- source lock entries exist for all generated concepts
- evidence citations contain immutable commit SHAs
- cited files and line anchors resolve when network access is available
- internal Markdown links are valid; report broken links as warnings because OKF permits them
- no concept contains unresolved placeholders presented as facts
- official documentation claims retain their version scope
- third-party examples are labelled as illustrative and are not used alone for general behavior claims
- copied or adapted third-party material includes verified license information and attribution

Use an installed OKF linter when available, but do not add or install dependencies without the user's approval. Always retain the three core checks as the minimum validation gate.

### 10. Review once

After deterministic validation passes, use `okf-reviewer` on the changed concepts and their claim ledger. Do not invoke the reviewer while blocking validation errors remain.

Fix blocking findings as the root or parent agent, rerun targeted validation, and report remaining warnings explicitly.

## Token and model policy

Shared rules:

- Keep at most three direct research agents active at once.
- Use one final high-reasoning review over changed concepts, not over all source repositories.
- Prefer targeted searches, schemas, tests, documentation sections, and configured example paths over recursive repository reads.
- Batch related third-party example repositories instead of assigning one agent per repository.
- Return summaries and evidence references, never raw exploration output.
- Reuse source locks, evidence packets, and unchanged concepts across runs.

Codex model selection:

- Use `gpt-5.6-luna` with low reasoning for inventory and routing.
- Use `gpt-5.6-terra` with medium reasoning for normal source interpretation.
- Use flagship `gpt-5.6` with high reasoning only for ambiguous Upjet-to-Terraform mappings.
- Use `gpt-5.6-terra` with high reasoning for the final review.

Pi model selection:

- Project agents intentionally do not pin a provider-specific model identifier. They inherit the model selected for the Pi session.
- Use the role-specific `thinking` levels declared in `.pi/agents/`.
- Configure local or hosted models outside this repository so the workflow remains portable across Pi providers.
- Use a stronger model or higher reasoning only for ambiguous Upjet mappings and the final evidence review.

## Completion report

Report:

- concepts created, updated, or removed
- pinned source commits used
- source roles used for material claims
- validation results
- reviewer status
- unresolved mappings, conflicts, licensing questions, and permitted broken links
- the narrowest next source batch, when more coverage is requested
