# Evidence packet contract

Subagents return evidence to the root agent. They do not write OKF documents.

Use this compact Markdown structure:

```markdown
## Scope
- Repository: owner/name
- Commit: full SHA
- Source role: primary | official-documentation | supporting | third-party-example
- Requested area: path, package, command, API, documentation section, example, or resource batch

## Concept candidates
### Stable concept identifier
- Type: proposed OKF type
- Title: proposed title
- Summary: one sentence, source-backed
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
  - unresolved issue, version boundary, source disagreement, or repository-specific choice

## Source inventory
- path — authority role and reason it is relevant

## Licensing
- copied or adapted material: none | details
- verified license and attribution requirements

## Unresolved
- exact question and the missing evidence
```

Rules:

- Use `direct` only when the cited source directly supports the claim. Confidence does not replace source authority.
- Use `corroborated` when independent code, tests, examples, or documentation agree.
- Use `inferred` only for a clearly labelled conclusion that is useful but not explicitly stated.
- Primary sources establish API shape and runtime behavior.
- Official documentation establishes documented guidance and user-facing terminology. Record version scope and conflicts with implementation.
- A third-party example may directly support a claim about its own implementation, but not a general claim about Crossplane behavior or recommended practice.
- Corroborate reusable third-party patterns with primary sources or official documentation.
- Do not include copied or adapted third-party material without verified license information and attribution requirements.
- Include no raw logs, full files, or broad repository summaries.
- Keep each packet bounded to the assigned scope.
