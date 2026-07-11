# Evidence packet contract

Subagents return evidence to the root agent. They do not write OKF documents.

Use this compact Markdown structure:

```markdown
## Scope
- Repository: owner/name
- Commit: full SHA
- Source role: primary | official-documentation | supporting | third-party-example
- Requested area: path, package, command, API, documentation section, example, or resource batch
- Selected release: stable tag, documentation series, or explicitly requested preview revision
- Legacy exclusions applied: exact exclusions relevant to this packet

## Concept candidates
### Stable concept identifier
- Type: proposed OKF type
- Title: proposed title
- Summary: one sentence, source-backed
- Crossplane version scope: exact release or major.minor documentation series
- Feature state: Alpha | Beta | Stable | Deprecated | Not stated by selected sources
- Feature-state evidence: commit-pinned citation or `not stated`
- Claims:
  - Claim text
    - Class: API | behavior | documented-guidance | illustrative-pattern
    - Evidence: commit-pinned URL with line range
    - Source role: primary | official-documentation | supporting | third-party-example
    - Confidence: direct | corroborated | inferred
- Schema sources:
  - path and purpose
- Examples:
  - path, origin, and what it demonstrates
- Relationships:
  - target concept and prose relationship
- Limitations or conflicts:
  - unresolved issue, version boundary, source disagreement, repository-specific choice, or legacy-only material that was excluded

## Source inventory
- path — authority role and reason it is relevant

## Licensing
- copied or adapted material: none | details
- verified license and attribution requirements

## Excluded legacy material
- path or section — Claims | deprecated XRD v1 | legacy v1 XR semantics | explicitly labelled legacy

## Unresolved
- exact question and the missing evidence
```

Rules:

- Use `direct` only when the cited source directly supports the claim. Confidence does not replace source authority.
- Use `corroborated` when independent code, tests, examples, or documentation agree.
- Use `inferred` only for a clearly labelled conclusion that is useful but not explicitly stated.
- Primary sources establish API shape and runtime behavior.
- Official documentation establishes documented guidance and user-facing terminology. Record version scope and conflicts with implementation.
- Resolve the latest stable Crossplane release before researching Crossplane Core unless the user explicitly requests another release or preview content.
- Never infer Alpha, Beta, or Stable from API version names such as `v1alpha1`, `v1beta1`, or `v1`. Cite an explicit feature-state statement or use `Not stated by selected sources`.
- Do not treat every `apiextensions.crossplane.io/v1` resource as legacy. Require explicit deprecation metadata or a legacy label. Current Crossplane v2 resources may still use a v1 Kubernetes API version.
- Exclude Claims, deprecated CompositeResourceDefinition v1, and legacy v1 composite-resource semantics from legacy-free catalog work.
- A third-party example may directly support a claim about its own implementation, but not a general claim about Crossplane behavior or recommended practice.
- Corroborate reusable third-party patterns with primary sources or official documentation.
- Do not include copied or adapted third-party material without verified license information and attribution requirements.
- Include no raw logs, full files, or broad repository summaries.
- Keep each packet bounded to the assigned scope.
