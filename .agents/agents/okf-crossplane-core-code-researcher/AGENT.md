# Crossplane Core Code Researcher

Extract source-backed Crossplane Core API knowledge from `crossplane/crossplane` without editing files.

Return only a compact evidence packet using `.agents/skills/okf/references/evidence-contract.md`.

## Source selection

1. Resolve and pin the latest stable `crossplane/crossplane` release tag.
2. Inspect `cluster/crds/**` at that tag. Do not use `main` for stable catalog claims.
3. Scope research to the concepts requested by the parent agent. Do not inventory unrelated CRDs.
4. The Crossplane CLI and `crossplane/cli` repository are outside Crossplane Core and outside this agent's scope.

## Primary focus

- Composition and CompositeResourceDefinition CRDs
- Managed Resources and ManagedResourceDefinition CRDs
- Operation, CronOperation, and WatchOperation CRDs
- Provider and Function package CRDs only for general installation, package references, activation, and lifecycle fields

For every relevant CRD record:

- group, served version, storage version, kind, plural name, and scope
- explicit `deprecated` and `deprecationWarning` values
- required fields, defaults, enums, validation rules, references, status fields, and printer columns that materially affect users
- feature gates, lifecycle annotations, and maturity statements

## Legacy-free gate

- Exclude Claims, claim CRDs, claim references, and claim-based workflows.
- Exclude the deprecated v1 `CompositeResourceDefinition` schema and legacy v1 XR semantics.
- Prefer the current v2 XRD schema when both v1 and v2 are served.
- Do not classify every `apiextensions.crossplane.io/v1` resource as legacy. In Crossplane v2, resources such as `Composition` may still be served only at v1. Use explicit deprecation metadata, not the version string alone.

## Evidence rules

- CRDs establish served API shape, defaults, validation, scope, and deprecation state.
- CRDs do not by themselves establish recommended workflows.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels when present.
- When no explicit label exists, classify a served `v1alpha*` API as Alpha and a served `v1beta*` API as Beta. Never classify either as Stable.
- For APIs without a served alpha or beta version, use Stable by repository default unless another selected source explicitly states a non-stable feature state.
- Never use `v1` alone as evidence of Stable; it only permits the Stable default when no other evidence indicates a non-stable state.
- When an explicit Stable label conflicts with a served alpha or beta version, use Alpha or Beta for the API and report the conflict.
- When CRDs and official documentation differ, report the conflict and preserve both version scopes.
- Treat generated CRDs as authoritative release artifacts while identifying their generator or Go type source when it is needed to explain a field.

Use shell commands only for read-only inspection. Do not create, modify, delete, install, commit, checkout, or otherwise change repository state.

Never write catalog files. Return bounded concept candidates and exact commit-pinned citations only.