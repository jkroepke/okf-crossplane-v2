---
name: okf
description: Explicit-only workflow that builds or updates a source-backed Open Knowledge Format catalog for Crossplane core, providers, functions, SDKs, tools, official documentation, and examples. Never invoke implicitly; the user must invoke `$okf`, `/skill:okf`, or `/okf`.
disable-model-invocation: true
metadata:
  version: "1.3"
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
- Pi model configuration guidance lives in `.pi/README.md`.
- Pi users may invoke the shared skill with `/skill:okf` or use the project prompt `/okf`.
- Runtime-specific agents use the same `okf-*` role names and must preserve the same read-only evidence contract.
- Every dedicated role must exist as a matching Codex and Pi agent set.
- The root or parent agent remains the only writer regardless of runtime.

## Workflow

### 1. Bound the work

Create the smallest useful source and concept set. Do not process every repository or every managed resource unless the user explicitly requests full coverage.

For incremental work, inspect existing catalog concepts and source locks first. Regenerate only concepts affected by changed source paths or dependencies.

### 2. Pin sources

Resolve every selected repository to a full commit SHA before extracting knowledge. Record the resolved commits in `.okf/sources.lock.yaml` or update the existing lock file.

Never cite a moving branch in generated knowledge. A repository homepage may be used as the frontmatter `resource`, but evidence citations must be immutable.

For Crossplane Core, resolve the latest stable Crossplane release first. Use Core CRDs from that release tag and the matching `crossplane/docs` `content/v<major>.<minor>/` series. Do not use `content/master/`, `content/cli/**`, or `content/v1.*` for stable Core concepts.

### 3. Scout cheaply

Use `okf-source-scout` for repository classification and high-signal path discovery.

Batch repositories by source kind. Do not spawn one agent per repository. Prefer one scout task for up to five related repositories or one changed-source batch.

Scout official documentation and third-party examples separately from implementation repositories so their authority roles remain explicit in the evidence packet.

Skip scouting when existing locks and evidence already identify the relevant files and their source paths have not changed.

### 4. Research only what needs semantics

Use the narrowest matching researcher:

- `okf-crossplane-core-docs-researcher` for current stable Crossplane Core documentation, terminology, workflows, lifecycle states, and general provider or function installation guidance.
- `okf-crossplane-core-code-researcher` for current stable Crossplane Core CRDs under `cluster/crds`.
- `okf-function-go-templating-researcher` for `crossplane-contrib/function-go-templating`, limited by default to `README.md` and `example/**`.
- `okf-crossplane-researcher` for CLI, runtime, SDKs, tools, native providers, testing tools, examples, and domains without a dedicated researcher.
- `okf-upjet-researcher` only for Upjet provider concepts that require Terraform correlation. Give it an explicit provider service or managed-resource batch.

Run the Core docs and Core code researchers together when a concept needs both user-facing guidance and exact served API shape.

Every composition function must have its own dedicated Codex and Pi agent set. Add that bounded agent set and source profile before generating knowledge for a function that does not have one.

The Crossplane CLI is a separate catalog domain and is not part of Crossplane Core.

For third-party example repositories, restrict research to the configured paths. Extract concrete patterns, relationships, and use cases without treating the repository as proof of general Crossplane behavior.

Run independent read-heavy research in parallel, with at most three direct agents. Wait for all required evidence packets before writing. Never allow subagents to spawn subagents.

### 5. Apply source authority

Use evidence according to its source role:

- Primary implementation sources, API types, generated schemas, tests, and package metadata establish API shape and runtime behavior.
- Official Crossplane documentation establishes documented terminology, guidance, supported workflows, lifecycle states, and user-facing examples. When documentation conflicts with implementation or schemas, record the conflict and prefer implementation evidence for runtime behavior.
- Supporting sources provide background that is relevant only to their domain, such as Upjet generation or Terraform resource behavior.
- Third-party examples are illustrative. They may establish what that repository implements, but they must not be the sole evidence for Crossplane API semantics, runtime behavior, compatibility, security properties, or recommended practices.

Never infer Alpha, Beta, or Stable from an API version suffix. Use direct feature-state evidence or state `Not stated by selected sources`.

Do not treat every `apiextensions.crossplane.io/v1` resource as legacy. Require explicit deprecation metadata or an explicit legacy label.

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
- Crossplane release or documentation series
- feature state and its evidence, or `Not stated by selected sources`
- legacy exclusions applied
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
- exclude Claims, deprecated CompositeResourceDefinition v1, legacy v1 XR semantics, and sections explicitly labelled `v1 Composite Resources (Legacy)`
- keep current APIs that use `/v1` when they are not deprecated
- keep Crossplane CLI content outside the Core catalog section

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
- Core concepts record the selected stable release and matching documentation series
- feature states have direct evidence and are not inferred from API version names
- legacy-free output excludes Claims, deprecated XRD v1, legacy v1 XR semantics, and explicitly labelled legacy sections
- current non-deprecated APIs are not excluded only because they use `/v1`
- Crossplane CLI content is not categorized as Core
- each function concept uses its dedicated function agent and bounded source profile
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
- Use one final evidence review over changed concepts, not over all source repositories.
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

- Project agents intentionally do not pin a provider-specific model identifier or thinking level. They inherit the model and supported capabilities selected for the Pi session.
- Configure local or hosted models outside this repository so the workflow remains portable across Pi providers.
- Non-thinking coding models such as Qwen3-Coder-Next can run every project agent without incompatible reasoning controls.
- Use a stronger or different model for ambiguous Upjet mappings and the final evidence review when one is available.
- Follow `.pi/README.md` for local Qwen3-Coder-Next configuration guidance.

## Completion report

Report:

- concepts created, updated, or removed
- pinned source commits used
- selected Crossplane release and documentation series for Core work
- source roles used for material claims
- feature-state evidence or `Not stated by selected sources`
- legacy material excluded
- validation results
- reviewer status
- unresolved mappings, conflicts, licensing questions, and permitted broken links
- the narrowest next source batch, when more coverage is requested
