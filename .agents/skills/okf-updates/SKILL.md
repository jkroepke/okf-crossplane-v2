---
name: okf-updates
description: Explicit-only workflow that detects newer stable releases for selected Crossplane ecosystem sources, delegates release-diff research only for changed component identities, and presents an evidence-backed feature shortlist before any OKF content is changed.
disable-model-invocation: true
metadata:
  version: "1.0"
  license: Apache-2.0
---

# Crossplane OKF update discovery workflow

Run this workflow only after the user explicitly invokes `$okf-updates`, `/skill:okf-updates`, or `/okf-updates`.

This workflow is a read-only discovery and selection stage. It does not edit the catalog, source locks, claim ledger, indexes, logs, agent definitions, branches, or GitHub state.

The root or parent agent owns component identity resolution, delegation decisions, aggregation, and the handoff to the normal `$okf` workflow. Update researchers are read-only and never delegate further.

## Components

Check exactly these configured components unless the requester narrows the scope:

| Component ID | Repository | Current identity in `.okf/sources.lock.yaml` | Latest stable identity | Researcher |
| --- | --- | --- | --- | --- |
| `crossplane-core` | `crossplane/crossplane` | `sources.crossplane.tag` and `commit` | highest stable semantic-version tag and its full commit | `okf-crossplane-core-update-researcher` |
| `crossplane-runtime` | `crossplane/crossplane-runtime` | `sources.crossplane-runtime.tag` and `commit` | highest stable semantic-version tag and its full commit | `okf-crossplane-runtime-update-researcher` |
| `function-sequencer` | `crossplane-contrib/function-sequencer` | `sources.function-sequencer.tag` and `commit` | highest stable semantic-version tag and its full commit | `okf-function-sequencer-update-researcher` |
| `function-go-templating` | `crossplane-contrib/function-go-templating` | `sources.function-go-templating.tag` and `commit` | highest stable semantic-version tag and its full commit | `okf-function-go-templating-update-researcher` |
| `crossplane-docs` | `crossplane/docs` | `sources.crossplane-docs.series` and `commit` | documentation series matching the latest stable Crossplane major.minor plus the newest commit touching `content/v<major>.<minor>/**` | `okf-crossplane-docs-update-researcher` |

Do not infer a component identity from catalog frontmatter, prose, a moving branch, or an agent's memory. The source lock is the only definition of the current identity.

## Stable identity rules

For repositories that publish semantic-version tags:

1. Enumerate tags or releases without starting a subagent.
2. Parse semantic versions numerically.
3. Accept only a complete stable version such as `v2.4.1` or `0.13.0`.
4. Exclude draft releases and any tag with prerelease metadata, including alpha, beta, preview, milestone, release-candidate, snapshot, or development suffixes.
5. Resolve the selected tag to its full commit SHA.
6. Do not fall back to `main`, `master`, a release branch, or a prerelease.
7. A changed commit behind the same stable tag is not a new version. Report it as an integrity conflict and do not delegate until the conflict is understood.

For `crossplane/docs`:

1. Resolve the latest stable Crossplane tag first.
2. Derive `v<major>.<minor>` from that tag.
3. Find the newest commit on the docs default branch that changes files under `content/v<major>.<minor>/**`.
4. The docs identity is the pair `(series, path commit)`.
5. Ignore default-branch commits that do not touch the selected stable series.
6. Documentation changes may describe unreleased behavior. The docs researcher must corroborate every candidate against the latest stable Crossplane release before reporting it as available.

## Identity decision gate

Resolve every requested component before starting any update researcher.

Use these states:

- `CURRENT`: the locked and latest stable identities are equal. Do not start the component researcher.
- `UPDATE_AVAILABLE`: the latest stable identity is newer than the locked identity. Start the component researcher.
- `UNTRACKED`: the component has no lock entry. Treat the latest stable identity as an update candidate and use the immediately preceding stable tag as the bounded comparison baseline when one exists.
- `BLOCKED`: stable identity resolution failed, the lock is malformed, the locked tag cannot be resolved, history is not comparable, or a tag-to-commit integrity conflict exists. Do not start the component researcher.

Never start a researcher for `CURRENT` or `BLOCKED`.

For `UNTRACKED`, do not scan the full repository history. Compare only the immediately preceding stable tag to the latest stable tag. If there is no previous stable tag, inspect the latest stable release notes and the smallest high-signal source set.

## Delegation

Run at most three direct researchers at once. Use a second batch when more than three components changed.

Give each researcher:

- component ID and repository
- locked identity or `UNTRACKED`
- latest stable identity
- exact comparison base and head tags or commits
- release dates when available
- the stable identity rules above
- the feature relevance rules below
- the required output contract

Researchers must use only the assigned repository and comparison range, except where their canonical role explicitly requires stable Crossplane corroboration.

## Relevant feature rules

Report a candidate only when the stable comparison adds a user-facing capability that could improve this OKF bundle, such as:

- a new public API, resource, field, command, interface, helper, template function, input option, or supported workflow
- a new composition, reconciliation, readiness, dependency, rendering, provider-development, or documentation capability
- a previously prerelease capability that becomes available in a stable release
- a new official stable-series guide that explains a released capability not already represented in the catalog

A deprecation or removal is not a feature candidate unless it is inseparable from a replacement capability that should be documented.

Exclude:

- security fixes and vulnerability remediation
- bug fixes, regressions, race fixes, panic fixes, and correctness-only patches
- dependency bumps, generated-file churn, refactoring, test-only work, CI, release automation, build changes, formatting, and typo fixes
- performance changes without a new user-visible capability
- prerelease-only, unreleased, proposed, open-PR, or issue-only behavior
- legacy Crossplane v1 Claims, claim workflows, deprecated XRD v1 semantics, and documentation under `content/v1.*`

Do not turn release-note wording into fact without checking code, schemas, tests, examples, or stable documentation in the assigned comparison.

## Researcher output contract

Each researcher returns one compact packet:

```yaml
component: <component-id>
repository: <owner/name>
from_identity:
  version_or_series: <value-or-UNTRACKED>
  commit: <full-sha-or-null>
to_identity:
  version_or_series: <stable-value>
  commit: <full-sha>
comparison:
  base: <tag-or-sha>
  head: <tag-or-sha>
candidates:
  - title: <short feature title>
    category: <api|workflow|function|sdk|documentation|feature-promotion>
    summary: <what became newly available>
    stable_availability: <release or corroborated docs series>
    okf_fit: <which catalog area or concept would benefit>
    evidence:
      - <immutable commit-pinned file URL with line range, release, or compare reference>
    confidence: <direct|corroborated>
excluded:
  - <short grouped reason, not one line per commit>
uncertainties:
  - <bounded unresolved question>
```

Return `candidates: []` when the new stable version contains no relevant feature. Do not pad the result with bug fixes or housekeeping.

## Aggregate result

The parent agent:

1. Presents the identity state of every checked component.
2. Merges only candidate features from researchers that ran.
3. Deduplicates features documented by both Core and docs without losing either evidence role.
4. Assigns deterministic selection IDs in the form `<component-id>@<stable-identity>:F<two-digits>`.
5. Shows the title, concise summary, OKF fit, stable release, and primary evidence for every candidate.
6. States which changed components had no relevant feature.
7. Does not edit source locks or catalog files during discovery.

Ask the requester to select candidate IDs. Do not select features on the requester's behalf.

## Selected-feature handoff

A requester reply that selects one or more candidate IDs from this explicitly invoked workflow is explicit permission to run the normal OKF update logic for those candidates. No second `$okf` command is required.

Process each selected candidate independently:

1. Preserve the candidate ID, exact stable identity, comparison evidence, and bounded feature scope.
2. Load and follow `.agents/skills/okf/SKILL.md`.
3. Treat one candidate as one `$okf` request. Do not combine multiple selected features into one research/write batch.
4. Create the dedicated branch required by the normal workflow for that single feature.
5. Use the normal domain researchers for semantic research. The update researcher packet is discovery evidence, not sufficient catalog evidence by itself.
6. Update the source lock only in the feature branch when required by the normal workflow.
7. Run deterministic validation, `okf-reviewer`, and `mise run lint`.
8. Commit, push, and open one pull request for that feature.
9. Never include unselected candidates implicitly.

When `function-sequencer` is selected, the normal `$okf` workflow must first create its dedicated semantic researcher and bounded source profile if they still do not exist, because every composition function requires its own normal researcher set.

## Completion report

For discovery, report:

- locked and latest stable identities
- which researchers ran and which were skipped
- candidate IDs and supporting stable evidence
- changed components with no relevant features
- blocked identity checks and why they were blocked
- confirmation that discovery made no catalog or lock changes

For selected-feature processing, use the completion report required by the normal `$okf` workflow for each feature.
