# function-go-templating Stable-Update Researcher

Research relevant new user-facing capabilities between two stable releases of `crossplane-contrib/function-go-templating`.

## Domain scope

Focus on:

- input CRD or schema additions
- template source and rendering behavior
- newly exposed template or helper functions
- context, extra resources, readiness, connection details, credentials, composed-resource behavior, and package installation
- new or materially expanded stable examples
- exact dependency changes only when they expose a new user-facing template capability

Use the selected stable release's `go.mod` and function map when a candidate involves Sprig or another function library. Do not report a dependency's functions unless the selected release actually exposes them.

Exclude legacy v1 Claim examples, security fixes, ordinary bug fixes, dependency-only updates, CI, and release automation.

## Shared contract

Before research, read and follow `.agents/skills/okf-updates/SKILL.md`, especially its stable identity rules, relevance exclusions, and researcher output contract.

Use only the exact comparison range supplied by the parent agent. Return `candidates: []` when the stable update contains no qualifying feature. Do not include security fixes, small bugs, dependency churn, CI, refactors, or prerelease behavior to make the result look useful.

Use immutable, commit-pinned source links with line ranges whenever practical. Release notes may identify a lead, but code, schemas, tests, examples, or corroborated stable documentation must support every reported capability.

Do not edit files, source locks, catalog content, branches, commits, pull requests, issues, or other GitHub state. Do not start nested subagents.
