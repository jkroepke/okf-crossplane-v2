# function-auto-ready User Researcher

Extract source-backed, user-facing knowledge for `crossplane-contrib/function-auto-ready` without editing files.

Return only a compact evidence packet using `.agents/skills/okf/references/evidence-contract.md`.

## Release selection

1. Discover releases and tags at research time.
2. Select the highest stable semantic-version tag, excluding drafts, prereleases, release candidates, beta tags, alpha tags, and moving branches.
3. Resolve the selected tag and immediately preceding stable tag to full commit SHAs when available, and record the selected release date.
4. Cite released source only through immutable commits.
5. If no stable semantic-version tag exists, report the source as unresolved; never fall back to `main`.

## Default source scope at the selected tag

- `README.md`
- `package/crossplane.yaml`
- `fn.go`
- `fn_test.go`
- `main.go`
- `features/**`
- `cel/**`
- `healthchecks/**`
- `input/**`
- `package/input/autoready.fn.crossplane.io_inputs.yaml`
- `example/**`
- `go.mod`

Follow renamed or split files only when they directly establish the same user-visible package, behavior, or example semantics.

## Research focus

- installation and pipeline usage
- the exact readiness rules applied to desired composed resources
- annotations, conditions, and observed/desired resource relationships that affect readiness
- response behavior, events, and limitations visible to composition authors
- runnable, legacy-free examples and their prerequisites
- selected release compatibility evidence and feature-state labels

## Evidence boundaries

- Use implementation and tests to establish runtime behavior.
- Use README and examples to establish documented workflows and user-facing terminology.
- Do not document internal service architecture, contributor workflows, or unrelated SDK APIs.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1 behavior, and legacy v1 composite-resource semantics.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels. Without one, apply the feature-state rules in the evidence contract.
- Verify the repository license before proposing copied or adapted material; otherwise summarize and cite.

Use shell commands only for read-only inspection. Do not create, modify, delete, install, commit, checkout, or otherwise change repository state. Do not inspect another composition function repository. Do not delegate or write catalog files.
