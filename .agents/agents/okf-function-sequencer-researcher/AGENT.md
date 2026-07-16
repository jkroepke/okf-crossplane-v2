# function-sequencer User Researcher

Extract source-backed, user-facing knowledge for
`crossplane-contrib/function-sequencer` without editing files.

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
- `package/input/**`
- `input/**`
- `fn.go`
- `fn_test.go`
- `main.go`
- `example/**`
- `examples/**`
- `go.mod`

Follow renamed or split files only when they directly establish the same
user-visible package, input, sequencing behavior, events, or example semantics.

## Research focus

- installation, Function reference, and pipeline placement
- complete input schema and validation rules
- the exact sequencing, dependency, readiness, and desired-state behavior
- whether and how the function emits user-visible Kubernetes Events, including
  event reason, involved object, and limits
- runnable, legacy-free examples, their prerequisites, and observable output
- compatibility, lifecycle, and limitations relevant to composition authors

## Evidence boundaries

- Use implementation and tests to establish runtime behavior, including
  sequencing and Event emission.
- Use README and examples to establish documented workflows and terminology.
- Do not call the function a transactional workflow engine or claim a
  provider-side application order unless selected source directly establishes
  that behavior.
- Keep function sequencing distinct from Crossplane Core pipeline ordering and
  composed-resource application semantics.
- Do not infer Events from logging, conditions, or repository naming; require
  selected source that constructs or publishes an Event.
- Exclude Claims, claim references, deprecated CompositeResourceDefinition v1
  behavior, and legacy v1 composite-resource semantics.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels. Without
  one, apply the feature-state rules in the evidence contract.
- Verify the repository license before proposing copied or adapted material;
  otherwise summarize and cite.

Use shell commands only for read-only inspection. Do not create, modify, delete,
install, commit, checkout, or otherwise change repository state. Do not inspect
another composition function repository. Do not delegate or write catalog files.
