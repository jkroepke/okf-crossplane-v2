# function-tag-manager User Researcher

Extract source-backed, user-facing knowledge for
`crossplane-contrib/function-tag-manager` without editing files.

Return only a compact evidence packet using
`.agents/skills/okf/references/evidence-contract.md`.

## Release selection

1. Discover releases and tags at research time.
2. Select the highest stable semantic-version tag, excluding drafts,
   prereleases, release candidates, beta tags, alpha tags, and moving branches.
3. Resolve the selected tag and immediately preceding stable tag to full commit
   SHAs when available, and record the selected release date.
4. Cite released source only through immutable commits.
5. If no stable semantic-version tag exists, report the source as unresolved;
   never fall back to `main`.

## Default source scope at the selected tag

- `README.md`
- `package/crossplane.yaml`
- `package/input/tag-manager.fn.crossplane.io_managedtags.yaml`
- `input/**`
- `fn.go`
- `fn_test.go`
- `filter.go`
- `filter_test.go`
- `filters/**`
- `tags.go`
- `tags_test.go`
- `main.go`
- `examples/**`
- `go.mod`
- `LICENSE`

Follow renamed or split files only when they directly establish the same
user-visible package, input, tag-management behavior, supported-resource
filter, or example semantics.

## Research focus

- installation, Function reference, pipeline placement, and prerequisites
- the complete `ManagedTags` input schema, validation, source types, policies,
  and defaults
- exact add, ignore, remove, and conflict-resolution behavior, including the
  desired and observed fields the function reads or changes
- Composition environment input and the earlier pipeline behavior required to
  populate it
- per-resource opt-out annotation behavior, legacy-label compatibility, and
  precedence when both are present
- the exact AWS and Azure Upjet managed resources admitted by the selected
  release's generated filters, including cluster-scoped and namespace-scoped
  variants when selected source establishes them
- response results, errors, skips, and limitations visible to composition
  authors
- runnable, legacy-free examples, their prerequisites, and observable output
- selected release compatibility evidence and feature-state labels

## Evidence boundaries

- Use implementation, generated input schema, filters, and tests to establish
  runtime behavior and supported API shape.
- Use README and examples to establish documented workflows and user-facing
  terminology.
- Cross-check the README, Go input types, generated input schema, and runtime
  switches. Preserve any disagreement explicitly instead of silently choosing
  one representation.
- Treat generated provider filters as release-specific allowlists. Do not infer
  support for a provider, resource, scope, or provider version from tag-field
  naming or general cloud behavior.
- Do not claim that ignored tags are unmanaged by Crossplane in general.
  Describe only how this function copies selected observed values into desired
  state before later pipeline or provider processing.
- Keep this function's tag merge order distinct from Crossplane Core pipeline
  ordering and provider-side reconciliation semantics.
- Treat the legacy skip label only as compatibility behavior when selected
  source establishes it; recommend the annotation only when selected source
  does so.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1
  behavior, and legacy v1 composite-resource semantics.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels. Without
  one, apply the feature-state rules in the evidence contract to the owning API
  or capability; do not transfer the input API's state to the Function package.
- Verify the repository license before proposing copied or adapted material;
  otherwise summarize and cite.

Use shell commands only for read-only inspection. Do not create, modify, delete,
install, commit, checkout, or otherwise change repository state. Do not inspect
another composition function repository. Do not delegate or write catalog files.
