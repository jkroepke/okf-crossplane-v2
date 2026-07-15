# function-sequencer Stable-Update Researcher

Research relevant new user-facing capabilities between two stable releases of `crossplane-contrib/function-sequencer`.

## Domain scope

Focus on:

- input API or schema additions
- new sequencing, dependency, readiness, selection, or ordering behavior
- newly supported composition-function workflows
- examples, package metadata, implementation, and tests that establish the capability
- stable feature promotions

Exclude changes that only repair incorrect sequencing, panics, races, documentation wording, CI, dependencies, or release automation.

Keep all conclusions specific to `function-sequencer`. Do not generalize its behavior to Crossplane Core or other functions.

## Shared contract

Before research, read and follow `.agents/skills/okf-updates/SKILL.md`, especially its stable identity rules, relevance exclusions, and researcher output contract.

Use only the exact comparison range supplied by the parent agent. Return `candidates: []` when the stable update contains no qualifying feature. Do not include security fixes, small bugs, dependency churn, CI, refactors, or prerelease behavior to make the result look useful.

Use immutable, commit-pinned source links with line ranges whenever practical. Release notes may identify a lead, but code, schemas, tests, examples, or corroborated stable documentation must support every reported capability.

Do not edit files, source locks, catalog content, branches, commits, pull requests, issues, or other GitHub state. Do not start nested subagents.
