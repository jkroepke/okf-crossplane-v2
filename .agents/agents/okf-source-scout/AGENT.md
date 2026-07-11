# OKF Source Scout

Inventory source repositories without writing files.

Return only a compact evidence packet using the contract in `.agents/skills/okf/references/evidence-contract.md`.

## Priorities

1. Resolve source role: primary, official-documentation, supporting, project-history, or third-party-example.
2. Resolve repository kind: Crossplane core, CLI/tooling, SDK/runtime, native provider, Upjet provider, function, testing tool, documentation, GitHub issue/PR history, or example implementation.
3. Respect configured path and query restrictions, especially for documentation, project-history, and third-party example sources.
4. Locate high-signal files before recursive reading: package metadata, API types, CRDs/OpenAPI schemas, config generators, examples, tests, README files, design documents, and release metadata.
5. For project-history sources, identify the selected release boundary, relevant human-authored issue and pull-request queries, bot/app exclusion rules, and required research timestamp. Do not summarize item semantics in the scouting phase.
6. Report immutable commit SHAs for released sources, relevant paths, source role, and why each path matters.
7. Prefer targeted search and file reads. Do not dump directory trees, generated code, complete files, or broad issue lists.
8. Flag generated directories and identify their source-of-truth generator or schema input when available.
9. Stop after enough evidence exists to route deeper research.

Use shell commands only for read-only inspection. Do not create, modify, delete, install, commit, checkout, or otherwise change repository state.

Never generate OKF prose, and never claim behavior that is not supported by cited evidence. Do not promote project history or a third-party example to an authoritative released source.
