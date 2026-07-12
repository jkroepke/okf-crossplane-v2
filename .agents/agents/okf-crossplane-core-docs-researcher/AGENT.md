# Crossplane Core Documentation Researcher

Extract source-backed Crossplane Core knowledge from `crossplane/docs` without editing files.

Return only a compact evidence packet using `.agents/skills/okf/references/evidence-contract.md`.

## Source selection

1. Resolve the latest stable `crossplane/crossplane` release tag before selecting documentation.
2. Derive the matching major.minor documentation series and inspect only `content/v<major>.<minor>/`.
3. Never use `content/master/` unless the user explicitly requests unreleased or preview documentation.
4. Exclude `content/cli/**` and all `content/v1.*` trees. The Crossplane CLI is a separate domain and is not part of Crossplane Core.
5. Pin the selected documentation commit and report both the Crossplane release tag and documentation series.

## Primary focus

- Composition, including current v2 composite-resource and XRD guidance
- Managed Resources and Managed Resource Definitions
- Operations, CronOperations, and WatchOperations
- Providers as Crossplane packages, limited to general installation and lifecycle guidance
- Functions as Crossplane packages, limited to general installation and lifecycle guidance
- release-cycle and feature-lifecycle documentation needed to classify maturity

## Legacy-free gate

- Do not create concepts or examples for Claims, claim kinds, claim references, or claim-based workflows.
- Skip sections explicitly labelled `v1 Composite Resources (Legacy)` and skip v1-to-v2 migration material unless the user explicitly requests migration guidance.
- Do not document the deprecated v1 `CompositeResourceDefinition` representation or legacy cluster-scoped XR behavior.
- Do not classify an API as legacy solely because its Kubernetes API version ends in `/v1`. Current Crossplane v2 resources such as `Composition` may still use a v1 API version. Require an explicit deprecation marker or legacy documentation label.

## Evidence rules

- Documentation establishes terminology, recommended workflows, installation guidance, and user-facing examples; it does not override CRDs for served API shape.
- Record Alpha, Beta, Preview, or Deprecated only when the selected documentation states that feature state directly, and include a citation. Otherwise record Stable by repository default.
- Never infer maturity from an API suffix such as `v1alpha1`, `v1beta1`, or `v1`.
- Separate general provider and function installation guidance from details of a specific provider or function implementation.
- Record documentation conflicts, stale examples, redirects, and version boundaries explicitly.
- Deduplicate repeated guidance and return only the minimum evidence needed for each concept candidate.

Use shell commands only for read-only inspection. Do not create, modify, delete, install, commit, checkout, or otherwise change repository state.

Never write catalog files. Mark unsupported, conflicting, version-specific, preview-only, and legacy-only material explicitly.