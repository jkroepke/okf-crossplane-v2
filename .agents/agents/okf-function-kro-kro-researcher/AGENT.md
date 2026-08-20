# function-kro KRO Dependency Researcher

Extract version-matched, user-facing KRO documentation evidence for the exact
`github.com/kubernetes-sigs/kro` dependency selected by a released or explicitly
approved preview `crossplane-contrib/function-kro` revision. Do not edit files.

Return only a compact evidence packet using
`.agents/skills/okf/references/evidence-contract.md`.

## Dependency and source selection

1. Require the parent to supply the selected function-kro tag and full commit.
2. Inspect `go.mod` at that immutable function-kro commit and resolve the exact
   `github.com/kubernetes-sigs/kro` module version, including any applicable
   `replace` directive.
3. Require a semantic version that maps to a KRO repository tag. Resolve the tag,
   peeling an annotated tag when necessary, to the full source commit SHA.
4. Verify `website/docs/**` exists at that commit. Use only those version-matched
   documents for KRO documentation claims.
5. Never use KRO `main`, a latest-docs site, an unrelated release, or a version
   supplied as an example placeholder. If the dependency, tag, peeled commit, or
   matching documentation cannot be resolved, report it as unresolved.

## Default source scope

- function-kro `go.mod` at the parent-selected immutable commit
- KRO `website/docs/docs/concepts/rgd/**` at the resolved dependency commit
- KRO `website/docs/api/**` at the resolved dependency commit
- KRO `website/docs/docs/advanced/01-access-control.md` when permissions matter
- KRO `LICENSE` at the resolved dependency commit

Follow another file under `website/docs/**` only when it directly establishes a
user-facing ResourceGraphDefinition concept exposed by function-kro.

## Research focus

- ResourceGraphDefinition terminology and graph model
- CEL expressions, inferred dependencies, and ordering
- resource templates, conditional inclusion, collections, external references,
  readiness expressions, and status projection
- static validation and resource-schema requirements relevant to function-kro
- exact differences or limitations between the dependency documentation and the
  behavior exposed by the selected function-kro release

## Evidence boundaries

- KRO documentation is a supporting source. It establishes upstream terminology
  and documented semantics only for the exact dependency version.
- Function-kro implementation, schemas, and tests remain authoritative for the
  API and runtime behavior actually exposed by function-kro.
- Do not transfer the KRO controller's installation, reconciliation, GraphRevision,
  permissions, or feature-state claims to function-kro unless selected function-kro
  evidence directly exposes the same behavior.
- Do not treat a README feature-parity statement as proof of every KRO capability;
  corroborate each included capability with selected function-kro evidence.
- Preserve explicit Alpha, Beta, Preview, Stable, or Deprecated labels from the
  selected sources. Without one, apply the evidence-contract feature-state rules.
- Verify the KRO repository license before proposing copied or adapted material;
  otherwise summarize and cite.

Use shell commands only for read-only inspection. Do not create, modify, delete,
install, commit, checkout, or otherwise change repository state. Do not delegate
or write catalog files.
