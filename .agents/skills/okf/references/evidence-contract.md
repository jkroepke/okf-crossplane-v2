# Evidence packet contract

Subagents return evidence to the root agent. They do not write OKF documents.

Use this compact Markdown structure:

```markdown
## Scope
- Repository: owner/name
- Commit: full SHA when the source is release content or historical design
- Source role: primary | official-documentation | historical-design | supporting | project-history | third-party-example
- Requested area: path, package, command, API, documentation section, design question, example, issue/PR theme, or resource batch
- Selected release: stable tag, documentation series, or explicitly requested preview revision
- Research timestamp: required for project-history evidence
- Design document status: required for historical-design evidence
- Legacy exclusions applied: exact exclusions relevant to this packet

## Concept candidates
### Stable concept identifier
- Type: proposed OKF type
- Title: proposed title
- Summary: one sentence, source-backed
- Crossplane version scope: exact release or major.minor documentation series
- Feature state: Alpha | Beta | Preview | Stable | Deprecated
- Feature-state basis: explicit commit-pinned label; served `v1alpha*` or `v1beta*` API version; or `Stable by repository default because selected sources contain no explicit non-stable label and no relevant served alpha or beta API version`
- Claims:
  - Claim text
    - Class: API | behavior | documented-guidance | historical-context | release-history | reported-limitation | proposal | illustrative-pattern
    - Evidence: commit-pinned URL with line range, or direct issue/PR URL with snapshot metadata
    - Source role: primary | official-documentation | historical-design | supporting | project-history | third-party-example
    - Confidence: direct | corroborated | inferred
- Schema sources:
  - path and purpose
- Examples:
  - path, origin, and what it demonstrates
- Historical design:
  - document path, status, revision, stated inaccuracies, and what current evidence corroborates or contradicts
- Project history:
  - issue or PR number, state, human author, timestamps, selected-release relationship, and concise relevance
- Relationships:
  - target concept and prose relationship
- Limitations or conflicts:
  - unresolved issue, version boundary, source disagreement, repository-specific choice, or legacy-only material that was excluded

## Source inventory
- path, issue, or pull request — authority role and reason it is relevant

## Licensing
- copied or adapted material: none | details
- verified license and attribution requirements

## Excluded legacy material
- path or section — Claims | deprecated XRD v1 | legacy v1 XR semantics | explicitly labelled legacy

## Excluded automation activity
- bot or app account and excluded item count, without reproducing low-signal item details

## Unresolved
- exact question and the missing evidence
```

Rules:

- Use `direct` only when the cited source directly supports the claim. Confidence does not replace source authority.
- Use `corroborated` when independent code, tests, examples, or documentation agree.
- Use `inferred` only for a clearly labelled conclusion that is useful but not explicitly stated.
- Primary sources establish API shape and runtime behavior.
- Official documentation establishes documented guidance and user-facing terminology. Record version scope and conflicts with implementation.
- Historical-design sources establish only historical intent, rationale, conceptual models, alternatives, and tradeoffs for a specific already-known feature.
- Never use historical-design sources for general feature discovery, current API shape, runtime behavior, supported guidance, release inclusion, or feature maturity.
- Record the design document status and every prominent warning that it is partially implemented, superseded, semi-defunct, or otherwise inaccurate.
- Qualify every design-derived current fact with selected stable implementation, schema, test, or matching stable documentation evidence. Without corroboration, report it only as historical design intent or unresolved context.
- Resolve the latest stable Crossplane release before researching Crossplane Core unless the user explicitly requests another release or preview content.
- Preserve explicit Alpha, Beta, Preview, Stable, and Deprecated labels from selected current sources.
- A relevant served `v1alpha*` API is an Alpha stability ceiling and a relevant served `v1beta*` API is a Beta stability ceiling. Never record either as Stable.
- When an explicit Stable label conflicts with a served alpha or beta API version, classify the API as Alpha or Beta and record the source conflict.
- When no explicit label exists, use Alpha for `v1alpha*`, Beta for `v1beta*`, and Stable only when no relevant served alpha or beta API version exists.
- Never use `v1` alone as evidence of Stable; it only permits the repository Stable default when no other selected evidence indicates a non-stable state.
- Never derive feature state from a design document or its Speculative, Draft, Accepted, or Defunct status.
- Do not treat every `apiextensions.crossplane.io/v1` resource as legacy. Require explicit deprecation metadata or a legacy label. Current Crossplane v2 resources may still use a v1 Kubernetes API version.
- Exclude Claims, deprecated CompositeResourceDefinition v1, and legacy v1 composite-resource semantics from legacy-free catalog work.
- Project-history evidence must record the research timestamp because issue and pull-request state can change.
- Exclude bot- and app-authored issues, pull requests, comments, and reviews from project-history evidence.
- An open issue supports only that a problem or behavior was reported. An open or unmerged pull request supports only that a change was proposed.
- A merged pull request establishes inclusion in a selected release only when its merge commit is proven to be contained in that release tag.
- A closed issue does not imply that the issue was fixed. Require a linked change and selected-release containment before stating resolution.
- Project-history evidence cannot independently establish API shape, runtime behavior, feature maturity, or recommendations. Corroborate those claims with released source, tests, schemas, or official documentation.
- A third-party example may directly support a claim about its own implementation, but not a general claim about Crossplane behavior or recommended practice.
- Corroborate reusable third-party patterns with primary sources or official documentation.
- Do not include copied or adapted third-party material without verified license information and attribution requirements.
- Include no raw logs, full files, or broad repository summaries.
- Keep each packet bounded to the assigned scope.
