# Evidence packet contract

Subagents return evidence to the root agent. They do not write OKF documents.

Use this compact Markdown structure:

```markdown
## Scope
- Repository: owner/name
- Commit: full SHA
- Requested area: path, package, command, API, or resource batch

## Concept candidates
### Stable concept identifier
- Type: proposed OKF type
- Title: proposed title
- Summary: one sentence, source-backed
- Claims:
  - Claim text
    - Evidence: commit-pinned URL with line range
    - Confidence: direct | corroborated | inferred
- Schema sources:
  - path and purpose
- Examples:
  - path and what it demonstrates
- Relationships:
  - target concept and prose relationship
- Limitations or conflicts:
  - unresolved issue, version boundary, or source disagreement

## Source inventory
- path — reason it is authoritative

## Unresolved
- exact question and the missing evidence
```

Rules:

- Use `direct` only when one authoritative source states or implements the claim.
- Use `corroborated` when independent code, tests, examples, or documentation agree.
- Use `inferred` only for a clearly labelled conclusion that is useful but not explicitly stated.
- Include no raw logs, full files, or broad repository summaries.
- Keep each packet bounded to the assigned scope.
