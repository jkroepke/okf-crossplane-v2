---
type: Crossplane Development Guide
title: Develop a Crossplane v2 Composition
description: An evidence-bounded route through XR API design, provider selection, function ordering, security, identity, readiness, testing, and packaging.
resource: https://docs.crossplane.io/v2.3/composition/compositions/
tags: [crossplane, composition, composition-authoring, development, starter-guide]
timestamp: 2026-07-16T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml
  - cluster/crds/apiextensions.crossplane.io_compositions.yaml
  - apis/apiextensions/v1/composition_common.go
  - apis/apiextensions/v2/xrd_types.go
  - cmd/crossplane/core/core.go
  - cluster/charts/crossplane/templates/deployment.yaml
  - internal/xfn/required_resources.go
  - internal/xfn/function_runner.go
  - internal/controller/apiextensions/composite/composition_functions.go
  - internal/controller/apiextensions/composite/composition_render.go
  - internal/controller/apiextensions/composite/api.go
supporting_sources:
  - repository: crossplane/docs
    commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
    paths:
      - content/v2.3/composition/compositions.md
      - content/v2.3/guides/connection-details-composition.md
      - content/v2.3/managed-resources/usages.md
  - repository: crossplane/cli
    commit: ef9b974770a45e085aacee3b2cdda6284ab6cf51
    paths:
      - cmd/crossplane/render/xr/cmd.go
      - cmd/crossplane/render/load.go
  - repository: crossplane/crossplane-runtime
    commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
    paths:
      - pkg/xcrd/crd.go
      - pkg/xcrd/composite.go
  - repository: crossplane-contrib/function-go-templating
    commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
    paths:
      - fn.go
  - repository: crossplane-contrib/function-auto-ready
    commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
    paths:
      - fn.go
      - healthchecks/secret.go
      - healthchecks/registry.go
  - repository: crossplane-contrib/function-sequencer
    commit: 8ee29b46b7b9491fb307cf6caf339541a8d93422
    paths:
      - fn.go
  - repository: crossplane-contrib/provider-kubernetes
    commit: 0ea671a4dab090ff3b14877d35086f1950fa35e3
    paths:
      - apis/namespaced/object/v1alpha1/types.go
      - internal/controller/namespaced/object/object.go
feature_state: Not stated by selected sources
---

# Purpose and evidence boundary

Use this route when the task is to develop a Crossplane v2 Composition. It
connects the catalog's release-pinned concepts; it is not a universal runnable
Composition. Exact managed-resource GVKs, fields, credentials, connection-detail
keys, and provider behavior must come from the provider release installed in
the target environment.

The guide itself has no product maturity label. Each linked API or capability
retains its own feature state.

# 1. Define the platform API

Start with the [composite resource model](core/composite-resource-model.md),
then define a current
[CompositeResourceDefinition v2](core/composite-resource-definition.md).
Choose namespace scope deliberately, model only the human-orderable contract,
and apply [OpenAPI](core/xrd-openapi-schema.md),
[CEL validation](core/xrd-cel-validation.md), collection semantics, and
[tenant admission security](core/tenant-xr-api-security.md) before exposing the
API.

An XRD version requires `name`, `served`, and `referenceable`. The API contract
says exactly one version is referenceable and it must also be served;
Crossplane maps it to the generated XR CRD's storage version.[1][2]

A [Composition](core/composition.md) targets that XR GVK exactly:

```yaml
spec:
  compositeTypeRef:
    apiVersion: <xrd.spec.group>/<referenceable-version.name>
    kind: <xrd.spec.names.kind>
```

Do not substitute an XRD or CRD name for these two fields. The controller
compares the reconciled XR GVK to the reference exactly.[3][4][15]

# 2. Select concrete provider APIs

Use [provider implementation families and selection](providers/provider-landscape.md)
to identify the actual package and API family. Then inspect its exact installed
CRD with [provider CRD schema discovery](providers/crd-schema-discovery.md).
Do not infer compatibility or an Upjet-to-Terraform mapping from similar names.

Record the Provider package, ProviderConfig choice, managed-resource GVKs, and
whether [explicit MR activation](core/minimal-managed-resource-activation.md)
is required. Keep ProviderConfig selection in the Composition unless the
platform intentionally exposes and constrains that choice in the XR API.

This route cannot select those provider-specific facts without a target
provider and release. Treat their absence as a required project input, not a
catalog default.

# 3. Design the pipeline by outcome

Functions run in declared order and pass accumulated desired state and context
forward.[5] Choose a pattern by the outcome it changes:

| Need | Use | Outcome and boundary |
| --- | --- | --- |
| Render or transform desired resources | A resource-producing function such as [function-go-templating](functions/function-go-templating/index.md) | Adds complete desired objects under stable logical keys. |
| Decide readiness from an already-rendered resource's own observation | [Manual readiness](functions/function-go-templating/patterns/manual-readiness.md) or [function-auto-ready](functions/function-auto-ready/readiness.md), including its [built-in checks](functions/function-auto-ready/built-in-health-checks.md) and optional [Alpha CEL rules](functions/function-auto-ready/cel-health-checks.md) | Changes readiness; it should not change whether the desired object exists. Manual readiness sets an explicit decision; auto-ready derives one from the matched observed composed resource.[9][17] |
| Decide readiness from a controller-created object outside `.observed.resources` | [Non-composed-resource readiness](functions/function-go-templating/patterns/non-composed-resource-readiness.md), with the [Sveltos ClusterSummary](functions/function-go-templating/patterns/sveltos-clustersummary-readiness.md) as a specialization | Fetches the object through the Alpha ExtraResources directive and translates its documented status into explicit readiness on a complete desired composed resource. Core performs the read, so grant the Core service account—not the Function pod—the required RBAC.[6][7][12] |
| Choose readiness for a provider-kubernetes `Object` wrapper | [provider-kubernetes Object readiness](functions/function-go-templating/patterns/provider-kubernetes-object-readiness.md) | Separates wrapper creation or update success from the wrapped application's usable state; the selected namespaced Object API is Alpha.[18] |
| Publish consumer-visible XR status or connection references | [Strict status and connection publication](functions/function-go-templating/patterns/safe-status-and-connection-publication.md) | Gates the consumer contract on producer readiness and required data-key completeness. Resource or Secret existence alone is insufficient.[16][19] |
| Delay the first appearance of one exceptional successor | [Readiness-gated template staging](functions/function-go-templating/patterns/readiness-gated-staging.md) | Changes desired-resource introduction; retain every successor after it is observed. |
| Express a declared or branching introduction graph | [function-sequencer](functions/function-sequencer/sequencing.md) | Filters only unobserved successors and retains observed ones. |
| Protect deletion or order deletion | [Usage and ClusterUsage](core/usages-and-clusterusages.md), optionally sequencer deletion rules | Creates pre-existing deletion-protection relationships; it does not schedule creation or wait for readiness. Audit mixed scopes because Function pipelines do not run during XR deletion.[14] |

These patterns can apply the same broad principle—wait for a prerequisite—but
produce different outcomes. Readiness evaluation, consumer publication,
desired-resource membership, and deletion protection are separate control
planes. Do not exchange them merely because their prose descriptions all
mention readiness or ordering.

For environment-driven pipelines, use the
[environment, templating, and readiness route](functions/environment-config-pipeline.md)
and assign one owner to each shared context key.

# 4. Separate security principals and scopes

Review four authorization planes independently:

| Operation | Principal or boundary |
| --- | --- |
| Submit and update namespaced XRs | Tenant identity, namespace RBAC, and admission policy. |
| Fetch Function required resources such as ExtraResources | The Crossplane Core Deployment service account. Core performs the Kubernetes `Get` or `List`; the Function pod does not.[6][7][12] |
| Apply Function-produced composed resources | The Crossplane Core service account, using the separate composed-resource write path.[8] |
| Reconcile an external resource | The selected Provider controller identity and ProviderConfig credentials. |

Use [composed-resource RBAC](core/composed-resource-rbac.md) for Core grants and
[namespaced composition boundaries](core/namespaced-composition-boundaries.md)
before designing any cross-namespace behavior. A template-side namespace
filter does not narrow an earlier cluster-wide list or its RBAC requirement.

# 5. Keep identity, readiness, and publication distinct

A composed object has a logical desired-map key, a Kubernetes identity, and—if
it is a managed resource—possibly a provider-side external identity. Read
[composed-resource identity and replacement](core/composed-resource-identity-and-replacement.md)
before changing names or immutable fields.

For function-go-templating, its annotation selects the logical desired-map
key. Crossplane later persists the Core composition-resource annotation on the
actual object; neither annotation is `metadata.name`.[9][10][13]

For credentials, existence is not completeness. function-auto-ready's built-in
Secret check treats an observed Secret as ready on existence, while a consumer
publication gate may require particular keys and producer readiness.[16] Use the
[strict status and connection publication pattern](functions/function-go-templating/patterns/safe-status-and-connection-publication.md)
when completeness gates the XR contract.

# 6. Lay out, render, and test

Use the [reference project layout](core/composition-project-layout.md) to keep
the XRD, Composition, example XR, Function objects, provider setup, and test
fixtures distinct. The CLI's Functions input accepts Function objects only.[11]

Render locally with
[Crossplane CLI](cli/local-composition-rendering.md), including initial and
observed-resource stages. Add [xprin assertion suites](tools/xprin-test-suites.md)
when repeatable output assertions are useful. Offline rendering is not a
substitute for Kubernetes admission, provider behavior, credentials, or a live
reconciliation smoke test.

# 7. Package only after the contract is coherent

Use a [Configuration package](core/configurations/index.md) to distribute the
XRD, Composition, and package dependencies after the API, provider, pipeline,
and tests agree. Package revision activation controls installation lifecycle;
it does not validate provider-specific semantics or prove a rollback procedure.

# Evidence gaps that require project-specific proof

Do not fill these gaps by guesswork:

- a complete runnable manifest set for the selected provider and credentials;
- the target cluster's apply and live smoke-test procedure;
- Configuration build, registry, and promotion commands for the delivery system;
- provider-specific schemas, connection-detail keys, external names, and adoption behavior;
- security policy for cluster-scoped EnvironmentConfig data in a multi-tenant platform; and
- an integration fixture proving the exact selected Function package set together.

# Citations

[1] [XRD v2 required version fields](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1108-L1266)

[2] [Referenceable version mapped to generated CRD storage](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/crd.go#L158-L168)

[3] [Composition type-reference schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L58-L89)

[4] [XRD referenceable GVK derivation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L287-L298)

[5] [Function pipeline ordering](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L205-L251)

[6] [Required-resource fetch loop and Kubernetes selectors](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L227)

[7] [Required-resource fetcher wired to the Core client](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)

[8] [Core composed-resource apply path](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L615-L658)

[9] [function-go-templating desired-map key handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L336-L350)

[10] [Core composition-resource annotation key](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)

[11] [CLI Functions-only loader](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/load.go#L89-L113)

[12] [Core Deployment service-account selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/charts/crossplane/templates/deployment.yaml#L41-L56) and [Function gRPC invocation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/function_runner.go#L90-L166)

[13] [Core persists the logical resource key on the rendered object](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L98-L100)

[14] [Function pipelines do not run during XR deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L143-L148)

[15] [Composition compatibility filter compares the reconciled XR GVK](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/api.go#L267-L280)

[16] [Secret existence check and explicit readiness preservation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/secret.go#L7-L13), [`alwaysReady`](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L27-L32), and [explicit readiness preservation](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)

[17] [function-auto-ready matches desired and observed resources, preserves explicit decisions, then evaluates unspecified readiness](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L102-L193)

[18] [provider-kubernetes Object readiness policies](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/namespaced/object/v1alpha1/types.go#L114-L148) and [derived readiness evaluation](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L534-L599)

[19] [Official connection-details template guards absent observations and connection keys](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/connection-details-composition.md#L296-L317)
