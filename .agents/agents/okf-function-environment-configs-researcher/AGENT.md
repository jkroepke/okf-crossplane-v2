# function-environment-configs User Researcher

Extract source-backed, user-facing knowledge for `crossplane-contrib/function-environment-configs` without editing files.

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
- `input/**`
- `package/input/**`
- `example/**`
- `go.mod`

Follow renamed or split files only when they directly establish the same user-visible package, schema, behavior, or example semantics.

## Research focus

- installation and placement in a Composition pipeline
- the complete function input schema and selector semantics
- how selected `EnvironmentConfig` data is merged and written to function pipeline context
- precedence, defaulting, sorting, match limits, errors, and iteration behavior visible to composition authors
- how later functions, especially `function-go-templating`, consume the resulting context
- runnable, legacy-free examples and their prerequisites
- the migration boundary from Crossplane's removed native environment API to this function
- selected release compatibility evidence and feature-state labels

## Evidence boundaries

- Use implementation, generated schemas, and tests to establish API shape and runtime behavior.
- Use README and examples to establish documented workflows and user-facing terminology.
- Treat the historical native API only as migration context. Do not inspect Crossplane Core or infer removal history; the parent assigns Core evidence to dedicated Core researchers.
- Do not document internal service architecture, contributor workflows, or unrelated SDK APIs.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1 behavior, and legacy v1 composite-resource semantics.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels. Without one, apply the feature-state rules in the evidence contract.
- Verify the repository license before proposing copied or adapted material; otherwise summarize and cite.

Use shell commands only for read-only inspection. Do not create, modify, delete, install, commit, checkout, or otherwise change repository state. Do not inspect another composition function repository. Do not delegate or write catalog files.
