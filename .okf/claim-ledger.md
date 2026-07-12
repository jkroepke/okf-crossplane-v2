---
type: Evidence Ledger
title: function-go-templating v0.12.2 claim ledger
---

# Scope

Selected release `v0.12.2` at `0a1e6d386f4363fae257ddbfb5b497416370e830`; supporting Sprig `v3.3.0` at `e708470d529a10ac1a3f02ab6fdd339b65958372`. Feature state is **Not stated by selected sources** for every concept. Claims, deprecated XRD v1, legacy v1 XR semantics, and the README section explicitly labelled `v1 Composite Resources (Legacy)` were excluded.

# Claims

All claims have function scope v0.12.2 unless a narrower version is stated.

| Concept | Exact claim | Class | Source role | Confidence | Evidence |
|---|---|---|---|---|---|
| package | A pipeline references the installed Function name and supplies a v1beta1 GoTemplate input. | API | primary | direct | [README L9-L44](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L9-L44) |
| package | This catalog selected v0.12.2 and pinned its commit. | release-history | primary | direct | [commit 0a1e6d3](https://github.com/crossplane-contrib/function-go-templating/commit/0a1e6d386f4363fae257ddbfb5b497416370e830) and source lock |
| input | The generated CRD serves/stores v1beta1, requires `source`, and defines the six input fields. | API | primary | direct | [CRD L8-L94](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L94) |
| input | Inline requires exactly one of `template` and `templates`. | API | primary | direct | [CRD L56-L69](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L56-L69) |
| input | Default delimiters are `{{` and `}}`; `options` is top-level. | API | primary | direct | [CRD L31-L42](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L31-L42), [L80-L85](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L80-L85) |
| input | Inline, FileSystem, and Environment load templates as documented. | documented-guidance | primary | direct | [README L46-L59](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L59) |
| request-data | Templates receive observed/desired state, context, and extra resources. | behavior | primary | direct | [README L60-L73](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73) |
| request-data | Context and ExtraResources special resources update pipeline context. | behavior | primary | direct | [README L159-L277](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L277) |
| request-data | `getCredentialData` returns named request credential bytes. | behavior | primary | direct | [function_maps.go L166-L177](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L177) |
| rendered-output | Resource-name and readiness annotations control composed-resource identity and readiness reporting. | behavior | primary | direct | [function_maps.go L101-L103](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103), [README L124-L147](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L124-L147) |
| rendered-output | v2 connection details use an explicitly composed Secret. | documented-guidance | primary | direct | [README L101-L122](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L101-L122) |
| rendered-output | Same-type output can update status or create a composed resource; recursion must terminate through another composition. | behavior/guidance | primary | direct | [README L279-L350](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L279-L350) |
| template-functions | The selected function map adds eleven named helpers; `include` has a recursion bound. | API/behavior | primary | direct | [function_maps.go L24-L55](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L55), [L105-L121](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L105-L121) |
| template-functions | Sprig v3.3.0 is required; `env` and `expandenv` are removed. | API/behavior | primary | direct | [go.mod L5-L10](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L10), [function_maps.go L56-L62](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62) |
| sprig | Exposed Sprig groups cover data shaping, collections, encoding, paths, dates, SemVer, crypto, randomness, and network. | documented-guidance | supporting, availability gated by primary | corroborated | [Sprig index L3-L25](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/index.md#L3-L25), [function map L56-L62](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62) |
| sprig | Current-time, random, and DNS helpers are non-hermetic. | behavior | supporting | direct | [functions.go L67-L94](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/functions.go#L67-L94) |
| project-history | PR #580 is the sole commit from v0.12.1 to v0.12.2 and is contained in the selected release. | release-history | project-history corroborated by released source | corroborated | [comparison](https://github.com/crossplane-contrib/function-go-templating/compare/v0.12.1...v0.12.2), [released go.mod](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod) |
| project-history | Issues #579, #536, #535, #501, #61, and #40 are older-version or unverified reports, not v0.12.2 facts. | reported-limitation | project-history | direct as reports | Direct issue URLs in `project-history.md`; researched 2026-07-12 |
| project-history | PR #592 is post-release main-branch development and open PR #593 is a proposal, neither part of v0.12.2. | proposal | project-history | direct | Direct PR URLs in `project-history.md`; researched 2026-07-12 |

# Unresolved

- Runtime source-to-field validation is outside the selected generated schema scope.
- The only bundled FileSystem example is legacy-only, so no runnable v2 FileSystem example is retained.
- No open report was shown to reproduce on v0.12.2.
- README nests `options` under `inline`, conflicting with the generated CRD; catalog follows the generated schema.
- Bundled installation examples pin v0.11.5 and use varying Function object names; catalog uses selected v0.12.2 and requires name matching.

# Crossplane Core v2.3.3

Selected Core release `v2.3.3` at `09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d`; matching official documentation series `v2.3` at `f1315464e35d40d25a28e4c15b6725b0e21adf91`.

| Concept | Exact claim | Class | Source role | Confidence | Evidence |
|---|---|---|---|---|---|
| composite-resource-model | An XR represents a set of Kubernetes resources; an XRD defines its API and a Composition defines composed resources. | documented-guidance | official-documentation | direct | [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resources.md#L7-L35) |
| composite-resource-definition | XRD v2 is cluster-scoped; names, group, scope, versions, serving, storage, and update policy follow the cited CRD schema. | API | primary | direct | [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L702-L1368) |
| composite-resource-definition | Namespaced scope is the v2 default and is recommended for most XRDs. | documented-guidance | official-documentation | direct | [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/composite-resource-definitions.md#L500-L530) |
| composition | Current Composition is a non-deprecated cluster-scoped v1 API with Pipeline mode and bounded, uniquely named Function steps. | API | primary | direct | [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L273) |
| managed-resources | A Provider defines and manages concrete MR APIs and their external resources. | documented-guidance | official-documentation | direct | [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L7-L47) |
| managed-resource-definition | MRD is Alpha; its schema defines API identity, scope, versions, activation state, and status. | API and documented-guidance | primary and official-documentation | corroborated | [maturity](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-definitions.md#L1-L6), [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_managedresourcedefinitions.yaml#L7-L512) |

## Core limitations and exclusions

- Feature state is `Not stated by selected sources` for the XR model, XRD, Composition, and managed resources generally. Alpha applies only to MRD; Beta applies only to `managementPolicies`.
- Claims, claim references, deprecated XRD v1 schema, legacy v1 XR semantics, `LegacyCluster`, migration guidance, and legacy connection-secret workflows are excluded.
- Some v2.3 XRD documentation examples use the deprecated `/v1` XRD API; the catalog records the conflict and uses the released v2 CRD for API shape.
- Concrete managed-resource schemas and controller behavior require separately pinned provider sources.
- The generator and Go source-of-truth types for the released generated Core CRDs were not established in this bounded source batch.

# Crossplane Configurations v2.3.3

| Concept | Exact claim | Class | Source role | Confidence | Evidence |
|---|---|---|---|---|---|
| configuration-package | A Configuration is a portable OCI package containing XRDs and Compositions and declaring package dependencies. | documented-guidance | official-documentation | direct | [contents](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L8-L20), [dependency metadata](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L440-L451) |
| configuration | Configuration is a cluster-scoped, served/stored `pkg.crossplane.io/v1` API requiring a qualified package reference and exposing package controls and status. | API | primary | direct | [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurations.yaml#L7-L249) |
| configuration | Installation is registry-based; revision activation defaults automatic; constraints and dependency resolution are enforced by default. | documented-guidance | official-documentation | direct | [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L87-L338) |
| configuration-revision | ConfigurationRevision is a controller-managed, cluster-scoped v1 API with desired state, image, revision number, dependency counts, owned objects, and conditions. | API and behavior | primary | direct | [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_configurationrevisions.yaml#L7-L280) |
| dependencies-and-authoring | Configuration metadata declares Configuration, Function, and Provider dependencies; dependency resolution is enabled by default. | documented-guidance | official-documentation | direct | [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L244-L270), [metadata](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/configurations.md#L425-L472) |
| dependencies-and-authoring | Automatic dependency upgrades and downgrades are Alpha, flag-gated features with documented downgrade risks. | documented-guidance | official-documentation | direct | [maturity](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/get-started/install.md#L96-L120) |

# Crossplane Functions taxonomy and specification

Selected Core release `v2.3.3` at `09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d`; matching documentation `v2.3` at `f1315464e35d40d25a28e4c15b6725b0e21adf91`. The user-selected specification was pinned from `main` at `231dd83a48fe7a4b9c06c8c94735c365f3da40b6` and verified byte-for-byte identical to the v2.3.3 file. Claims, deprecated XRD v1, legacy v1 XR semantics, and CLI material were excluded.

| Concept | Exact claim | Class | Source role | Confidence | Feature state / evidence |
|---|---|---|---|---|---|
| functions-overview | Crossplane defines known `composition` and `operation` function capabilities; a package may declare either or both. | API and documented-guidance | primary and official-documentation | corroborated | Role-specific; [capability types](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/pkg/meta/v1/capabilities.go#L24-L35), [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/operations/operation.md#L59-L94) |
| functions-overview | Both roles use the shared RunFunction RPC, while type-specific state semantics differ. | API | primary | direct | Role-specific; [protocol](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L19-L35) |
| function-package | Function is cluster-scoped; v1 is storage and v1beta1 remains served. | API | primary | direct | Beta ceiling from served v1beta1; [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L7-L41) |
| function-package | Package lifecycle controls and defaults cover pulling, revisions, dependencies, constraints, and runtime configuration. | API | primary | direct | Beta ceiling; [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L79-L167) |
| composition-functions | Composition functions continuously reconcile XR state through ordered steps and must preserve desired state from prior steps. | behavior | official-documentation, corroborated by primary protocol/runtime | corroborated | Stable by repository default; [docs](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L601-L631) |
| composition-functions | Composition pipeline has 1–99 unique steps with function references and optional input, credentials, and requirements. | API | primary | direct | Stable by repository default; [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L100-L258) |
| operation-functions | Operation runs once to completion, begins without observed XR state, and requires operation capability on referenced functions. | behavior | primary and official-documentation | corroborated | Alpha from v1alpha1 and explicit docs; [runtime](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L86-L299) |
| operation-functions | Operation output resources are applied without owner references; retry and status are represented by the Operation API. | behavior and API | primary and official-documentation | corroborated | Alpha; [apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/ops/operation/reconciler.go#L347-L389), [CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L234-L341) |
| scheduled-and-watched-operations | CronOperation schedules Operation templates; WatchOperation creates them after selected resource changes. | API and behavior | primary and official-documentation | corroborated | Alpha from served v1alpha1; [Cron CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_cronoperations.yaml#L7-L90), [Watch CRD](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_watchoperations.yaml#L7-L100) |
| composition-function-specification | The specification normatively defines composition-function RPC serving, tag/TTL handling, desired-state constraints, results, configuration, packaging, and runtime assumptions. | API and documented-guidance | primary specification | direct | Composition role Stable by repository default; [specification](https://github.com/crossplane/crossplane/blob/231dd83a48fe7a4b9c06c8c94735c365f3da40b6/contributing/specifications/functions.md#L1-L109) |

## Function limitations and conflicts

- The general v2.3 Functions page and Function CRD description use composition-only framing; released capability metadata, protocol, Operations docs, and APIs establish the two-role model.
- The Composition Functions specification is explicitly composition-scoped. Potentially shared clauses are not asserted as normative operation-function requirements without separate evidence.
- Its `v1beta1` service-version example is stale relative to the current v1 protocol and v1-first runner fallback; the protocol source is authoritative.
- Whether an individual package supports composition, operation, or both requires its immutable package metadata; no current ecosystem inventory is claimed.
- No project-history or third-party-example evidence was used in this batch.

## Configuration limitations and exclusions

- Overall Configuration, ConfigurationRevision, base dependency resolution, and authoring maturity is `Not stated by selected sources`; Alpha applies only to automatic dependency upgrade and downgrade features.
- Configuration and revision pull/state values are defined by Go constants but are not all encoded as CRD OpenAPI enums.
- No rollback-specific field or status was found, so rollback procedure and reconciliation are not claimed.
- CLI command syntax is excluded from Core. Claims, deprecated XRD v1, and legacy v1 XR semantics were outside this source batch.
- The documentation's initial package-content summary omits some dependency kinds listed later; the catalog preserves the explicit Configuration, Function, and Provider dependency list.
- The v2.3 Configuration page and installation page name different automatic-downgrade enablement settings; the catalog records the conflict and does not prescribe one mechanism.
