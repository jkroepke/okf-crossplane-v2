# Catalog Update Log

## 2026-07-18
* **Update**: Added a Composition-authoring default that prefers the Upjet AWS, Azure, and GCP providers for new work while retaining already-used non-Upjet providers unless a tested, resource-by-resource migration is explicitly planned.
* **Creation**: Documented how to retrieve Crossplane provider-published connection Secret keys from release-pinned implementation sources, distinguishing destination-only CRD fields from `AdditionalConnectionDetailsFn` behavior and preserving conditional-key boundaries.
* **Update**: Extended provider connection-detail retrieval with the typed `managed.ConnectionDetails` and runtime-publisher path used by provider-sql, separating it from Upjet-based Crossplane provider configuration.

## 2026-07-16
* **Reorganization**: Kept readiness concepts atomic while expanding the Composition developer route by outcome, grouping function-go-templating patterns by the state they change, and renaming the Sveltos specialization so it cannot be mistaken for the generic non-composed-resource pattern.
* **Update**: Taught the Crossplane v2 OKF skill to retrieve the Composition developer starter as the primary routing concept for Composition authoring and substantial review tasks.
* **Review**: Added an evidence-bounded Composition developer starter route and cross-concept links across API design, provider schema selection, functions, security, readiness, identity, testing, and packaging.
* **Correction**: Replaced the incorrect XRD v2 `storage` authoring field with `referenceable` and corrected the Composition `compositeTypeRef` formula.
* **Correction**: Assigned ExtraResources read RBAC to the Crossplane Core service account and separated required-resource reads from composed-resource writes and Function runtime identity.
* **Consistency**: Scoped feature-state defaults to their owning API or capability; unlabelled non-API packages, helpers, and implementation behavior now remain Not stated.
* **Cross-concept review**: Distinguished readiness, desired-resource introduction, and deletion protection; documented Secret existence versus key completeness and shared environment-context ownership.
* **Validation**: Replaced directory links with explicit indexes and pinned remaining released-source citations to immutable commits.
* **Creation**: Proved composed-resource name preservation under a stable logical key, bounded immutable-field recreation claims, and added staged create-before-delete replacement guidance.
* **Creation**: Added complete function-sequencer v0.6.0 Input property coverage, explicit UsageVersion mixed-scope safety, and post-release `createOnly` boundaries.
* **Update**: Cross-linked Core Usage/ClusterUsage scope guidance with function-sequencer issue #114 and generated-reference limitations.
* **Update**: Added local validation schema-coverage triage for built-in Kubernetes resources, non-Crossplane custom resources, and community CRD catalog discovery boundaries.
* **Creation**: Added release-pinned function-sequencer knowledge covering declared desired-resource sequencing, observed-successor retention, Input controls, and XR Events; clarified that manual template readiness does not sequence resource introduction.
* **Creation**: Added readiness-gated staged resource introduction for function-go-templating, distinguishing reconciliation-round admission and retention from provider-side ordering.
* **Creation**: Added Go-template whitespace-boundary guidance for staged, multi-document function-go-templating output, including initial and fully observed render verification.
* **Correction**: Clarified that the XRD `referenceable` version, rather than an XRD `storage` field, determines the generated CRD storage version; confirmed a referenceable `v1alpha1` renders as `storage: true`.
* **Update**: Added release-contained PR #6588 source and test proof for the namespaced-XR cluster-scoped-resource rejection.
* **Creation**: Added provider-kubernetes Object wrapper readiness and Secret-status boundaries, including Alpha API scope, derived-condition limits, and random-secret churn risk.
* **Update**: Added dependency-gating, dynamic collection identity, and base64-safe connection-data guidance; excluded Claim-based workflows from this v2 pattern.
* **Creation**: Added a strict function-go-templating pattern that gates database XR status and connection references on observed composed-resource readiness, distinguishes Kubernetes names from managed-resource external names, and excludes legacy v1 connection output.
* **Update**: Added a template-side namespace-result filter for `ExtraResources` label lookups, including an early-stop Go-template variable pattern for use after the scan; it cannot scope the earlier cluster-wide list or reduce its RBAC requirement.
* **Creation**: Added an Alpha External Secrets Operator PushSecret pattern for publishing selected platform-team Kubernetes Secret data to configured external secret stores, including Vault and AWS examples.
* **Update**: Extended provider-family guidance with Upbound's pinned official-provider installation, monolith ownership, shared-family dependency, and offline-resolution boundaries.
* **Creation**: Added provider CRD schema discovery guidance for version-addressed Upbound API routes, pinned source-tree fallbacks, and AWS package-identity boundaries.
* **Creation**: Added Crossplane CLI local Composition rendering guidance, including Docker runtime requirements, Functions-only input handling, and observed-resource status fixtures.
* **Creation**: Added an XR-focused xprin assertion-suite reference and a recommended empty-project manifest layout for Composition authoring.

## 2026-07-15
* **Creation**: Added the accepted controlled-rollout design as historical context and separated its proposed Function-revision API from selected-release behavior proved by schemas and controller code.
* **Update**: Clarified that generated managed-resource references are Provider- and field-specific, documented explicit observed-status composition fallbacks, and bounded server-side-apply ownership and re-resolution behavior.
* **Update**: Added explicit ProviderConfig selection and central-account least-privilege guidance.
* **Creation**: Added a release-pinned Upjet-to-Terraform provenance and example-adaptation evidence chain.
* **Update**: Added MRAP default-activation, additive-overlap, one-way activation, and minimal-activation policy guidance.
* **Creation**: Added evidence-backed AWS provider-family package identification and the v2.3 modern namespaced managed-resource group convention.
* **Creation**: Established the provider catalog foundation: implementation families, AWS migration/selection boundaries, and Provider package revision activation scope.
* **Creation**: Added tenant XR API-group and admission-security guidance, including organization-specific example conventions.
* **Creation**: Added focused XRD-backed CRD authoring guidance for OpenAPI schemas, CEL validation, unknown data, version evolution, and scale/display subresources.
* **Update**: Verified the XRD v2 Composition selection fields: documented default selection, automatic or manual revision policy, and immutable enforced Composition override behavior.
* **Reorganization**: Separated namespaced Composition enforcement from cross-namespace synchronization patterns and moved real-time Composition and Management Policies project history into dedicated references.
* **Reorganization**: Grouped the Core index by domain and moved function-go-templating readiness and external-query examples under a dedicated patterns index.

## 2026-07-14
* **Creation**: Added manual composed-resource readiness patterns and a release-pinned Sveltos Profile-to-ClusterSummary ExtraResources example.
* **Creation**: Added release-pinned EnvironmentConfig knowledge covering the
  retained Beta API, the v1.18 removal of native Composition integration,
  function-environment-configs v0.7.2 selection and merge behavior, and the
  environment-to-template-to-readiness pipeline.
* **Correction**: Clarified from function-go-templating v0.12.2 conversion
  code and tests that ExtraResources `matchLabels` works for cluster-scoped
  resources; the defect is lost namespace scoping, which turns `matchLabels`
  plus `namespace` into an all-namespace list subject to RBAC.
* **Creation**: Documented Crossplane's default composed-resource permission boundary, aggregated ClusterRole grant procedure, and RBAC-manager implications.
* **Update**: Clarified the one-way effects of deleting or narrowing a ManagedResourceActivationPolicy, the related report in issue #6984, and the dedicated MRAP page's missing explicit warning.
* **Update**: Clarified with function and Crossplane Core implementation evidence that function-go-templating ExtraResources zero-match lookups are non-fatal and do not impose a minimum result count.
* **Creation**: Documented Beta real-time composition watches, TTL-driven reconciliation, required-resource refresh boundaries, and six related issue reports with released-fix provenance.
* **Creation**: Documented the Crossplane v2 namespaced-composition boundary reported in issue #6759 and compared provider-kubernetes, Reflector, and kubernetes-replicator synchronization patterns.
* **Creation**: Added a provider-opentofu and function-go-templating pattern for external queries, including static Function credential limits in multi-tenant pipelines.
* **Update**: Added the Management Policies GA tracker, grouped known limitation reports, and selected-release containment for implemented policy combinations.
* **Update**: Expanded function-go-templating issue #579 with its version scope, reported failure mode, proposed workarounds, and unresolved current-release applicability.
* **Creation**: Documented the absence of native Composition health status and the evidence boundaries of Argo CD Lua and Flux CEL health customizations.
* **Creation**: Added Crossplane Core Usage and ClusterUsage deletion protection, scope semantics, and current mixed namespace/cluster limitations.
* **Creation**: Added a release-pinned function-auto-ready v0.7.0 knowledge set covering package use, readiness ordering, Kubernetes health checks, Beta input, and Alpha CEL customizations.
* **Creation**: Added the Crossplane v2 function-go-templating pattern for aggregating observed connection details into an explicitly composed Kubernetes Secret.
* **Update**: Documented function-go-templating Context semantics and the Crossplane v2 compatibility boundary of all special meta kinds.
* **Update**: Documented exact function-go-templating helper semantics and added a dedicated ExtraResources capability reference.

## 2026-07-12
* **Update**: Expanded provider-agnostic Managed Resource knowledge with anatomy, reconciliation lifecycle, policies, identity safety, references, ProviderConfig, controls, conditions, and MR activation APIs.
* **Creation**: Added the two-role Crossplane Functions model, distinguishing composition functions from Alpha operation functions and documenting direct, scheduled, and watched invocation.
* **Creation**: Added a v2.3.3-pinned summary of the Composition Functions specification, explicitly separated from operation functions.
* **Creation**: Added Crossplane Configuration package concepts covering package contents, installation, revisions, dependencies, and authoring metadata.
* **Creation**: Established a Crossplane Core v2.3.3 foundation covering composite resources, XRDs, Composition pipelines, managed resources, and MRDs.
* **Creation**: Added a legacy-free, release-pinned function-go-templating v0.12.2 knowledge set with schema, behavior, helper, Sprig, and project-history concepts.
