# function-kro User Researcher

Extract source-backed, user-facing knowledge for
`crossplane-contrib/function-kro` without editing files.

Return only a compact evidence packet using
`.agents/skills/okf/references/evidence-contract.md`.

## Release selection

1. Use an explicitly approved preview tag and commit when the parent supplies
   one. Otherwise discover releases and tags at research time.
2. Without an explicitly approved preview, select the highest stable
   semantic-version tag, excluding drafts,
   prereleases, release candidates, beta tags, alpha tags, and moving branches.
3. Resolve the selected tag and immediately preceding stable tag to full commit
   SHAs when available, and record the selected release date.
4. Cite released source only through immutable commits.
5. If no stable semantic-version tag exists, report the source as unresolved;
   never fall back to `main`.

## Default source scope at the selected tag

- `README.md`
- `package/crossplane.yaml`
- `package/input/**`
- `input/**`
- `fn.go`
- `fn_test.go`
- `main.go`
- `kro/**`
- `schemas/**`
- `example/**`
- `go.mod`
- `LICENSE`

Follow renamed or split files only when they directly establish the same
user-visible package, input, generated resources, runtime behavior, or example
semantics.

## Research focus

- installation, Function reference, and pipeline placement
- the complete function input API and packaged schema
- how the function interprets KRO ResourceGraphDefinitions and produces desired
  Crossplane composed resources
- observed/desired state, resource identity, readiness, context, and response
  behavior visible to composition authors
- error handling, validation, iteration, caching, and other operational limits
- runnable, legacy-free examples and their prerequisites
- selected release compatibility evidence and feature-state labels
- the exact `github.com/kubernetes-sigs/kro` dependency in `go.mod`; leave its
  detailed upstream semantics to `okf-function-kro-kro-researcher`

## Evidence boundaries

- Use implementation, generated schemas, and tests to establish API shape and
  runtime behavior.
- Use README and examples to establish documented workflows and terminology.
- Treat KRO-specific types and semantics only as exposed or exercised by the
  selected function-kro release. Use version-matched supporting evidence from
  `okf-function-kro-kro-researcher`; do not generalize across KRO versions.
- Do not document internal service architecture, contributor workflows, code
  generation machinery, or unrelated SDK APIs.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1
  behavior, and legacy v1 composite-resource semantics.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels. Without
  one, apply the feature-state rules in the evidence contract.
- Verify the repository license before proposing copied or adapted material;
  otherwise summarize and cite.

Use shell commands only for read-only inspection. Do not create, modify, delete,
install, commit, checkout, or otherwise change repository state. Do not inspect
another composition function repository. Do not delegate or write catalog files.
