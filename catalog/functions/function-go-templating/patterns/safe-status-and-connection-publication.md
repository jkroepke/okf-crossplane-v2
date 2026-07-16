---
type: pattern
title: Safely publish database status and connection references
description: Gate consumer-facing XR status and connection references on observed composed-resource readiness in a Go template.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, readiness, connection-details, naming]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths: [fn.go, README.md]
documentation_repository: crossplane/docs
documentation_series: v2.3
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths:
  - content/v2.3/composition/compositions.md
  - content/v2.3/guides/connection-details-composition.md
  - content/v2.3/manifests/guides/connection-details-composition/composition-go-templating.yaml
  - content/v2.3/managed-resources/managed-resources.md
supporting_sources:
  - repository: crossplane-contrib/function-auto-ready
    commit: ed7886de159af73b9d6976f04f9171ec7a4cb411
    paths: [healthchecks/secret.go, healthchecks/registry.go, fn.go]
  - repository: crossplane/crossplane-runtime
    commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
    paths: [pkg/meta/meta.go]
  - repository: kubernetes/kubernetes
    commit: 66452049f3d692768c39c797b21b793dce80314e
    paths: [staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types.go]
crossplane_release: v2.3.3
feature_state: Beta
feature_state_basis: The GoTemplate input serves v1beta1, which sets a Beta ceiling.
---

# Overview

For a database Composition, give the rendered database, role, user, and each
extension a stable `gotemplating.fn.crossplane.io/composition-resource-name`,
such as `database`, `role`, or `extension-pgcrypto`. Those values, rather than
Kubernetes `metadata.name`, are the keys under `$.observed.resources` on a
later reconciliation.[1]

Treat the consumer-facing connection Secret and XR status as a single
publication boundary: render valid empty Secret data while observations are
absent, but do not publish an actionable `status.connectionSecret` or other
application-ready status fields until every required composed resource is
ready and the required connection-detail keys are present.[2][3][14] This is a
strict authoring pattern; Crossplane does not automatically make arbitrary XR
status fields conditional on readiness.[4]

If function-auto-ready runs later, do not rely on its built-in Secret check for
this contract: that check marks an observed Secret ready on existence. Set
explicit `Ready=False` until the required keys are present and `Ready=True`
only after the gate passes; auto-ready preserves an earlier explicit result.[13]

# Strict readiness gate

Use the provider's usable-state signal for this gate. For standard managed
resource conditions, `Ready=True` with reason `Available` means the provider
reports the resource ready for use; `Synced=True` means only that reconciliation
succeeded. `Synced=True` alone is therefore not sufficient to publish a
database endpoint, credentials reference, or ready status.[5]

Calculate a boolean from the named observed resources and required
connection-detail keys, then render the XR-status object only inside that
condition. The status object must have the same API version and kind as the
observed XR and **must not** have a composition-resource-name annotation;
function-go-templating treats that form as a status update rather than another
composed resource.[6]

```gotemplate
{{- $databaseReady := eq (.observed.resources.database | getResourceCondition "Ready").Status "True" }}
{{- $roleReady := eq (.observed.resources.role | getResourceCondition "Ready").Status "True" }}
{{- $observedResources := default (dict) .observed.resources }}
{{- $role := default (dict) (get $observedResources "role") }}
{{- $roleDetails := default (dict) (get $role "connectionDetails") }}
{{- $credentialsPresent := hasKey $roleDetails "password" }}
{{- if and $databaseReady $roleReady $credentialsPresent }}
---
apiVersion: plattform.example.com/v1alpha1
kind: MySQLDatabase
metadata:
  name: {{ .observed.composite.resource.metadata.name }}
status:
  ready: true
  connectionSecret: example-connection-secret
{{- end }}
```

Also guard each connection-detail lookup before copying it into a Secret: the
observed map, named resource, and its connection details can all be absent on
the first reconciliation.[2][3] Do not replace those checks with unconditional
`gotemplating.fn.crossplane.io/ready: "True"`; that assertion bypasses the
observed readiness contract.[4]

# Dependency and collection patterns

Only defer a dependent resource until the prerequisite observation contains a
value that the dependent resource actually needs. For example, defer a Secret
that needs a role password until that named role is `Ready=True` and the
password exists. A database whose `owner` is a user-supplied, static role name
does not automatically need that gate; the selected SQL provider's reference
and retry behavior must establish whether it does.[11]

Once a long-lived composed resource has been introduced, keep rendering its
complete desired object on every reconciliation. Readiness is a separate
decision: set its explicit readiness to `False` while a prerequisite is not
usable rather than omitting the desired object merely because a transient
condition changed. Crossplane deletes a composed resource that a function
previously added but no longer returns in desired state, unless that omission is
intentional.[12]

For a list such as database extensions, derive both a stable composition
resource name (for example, `extension-<logical-id>`) and a deterministic,
Kubernetes-compatible object name. Validate or normalize XR-supplied logical
IDs before using them in `metadata.name`; ensure the derived names cannot
collide after normalization. The resource-name annotation must also remain
stable across reconciliations, otherwise its observed state cannot be joined
reliably.[1][12]

# Connection-data handling

Observed `connectionDetails` values are already base64-encoded. Copy them
directly into `Secret.data`; when constructing a derived URI, decode only the
required component, compose the URI, and encode the final value once. Do not
double-encode an observed password or treat the presence of a password as proof
that the producer is ready.[3][5]

Keep sensitive connection material in a composed Kubernetes `Secret`, not in
XR status. The status gate should publish the Secret *reference* only after
the Secret has the required data. This catalog excludes Claim-based workflows,
so a template that reads `spec.claimRef` needs a non-Claim v2 equivalent before
it can be included.[3]

# Kubernetes and external names

Give every composite resource a Kubernetes object identity: normally a valid
`metadata.name`, or `generateName` when generated naming is intended. Kubernetes
requires a name for resource creation unless the server generates one from that
prefix.[7] Use that identity only to derive Kubernetes-compatible names, for
example for an aggregate Secret. It is distinct from a function
composition-resource name and from a provider-side identifier.[8]

Keep every composed Kubernetes object's `metadata.name` Kubernetes-compatible.
When a **managed resource's** provider-side identity cannot or should not equal
that name, set `crossplane.io/external-name` on that managed resource if its
specific provider supports the annotation. Providers commonly default their
external identity to the Kubernetes name, but the accepted format and adoption
behavior remain provider-specific. The annotation is not a generic XR naming
mechanism and cannot make an invalid Kubernetes `metadata.name` valid.[9][10]

# Scope boundaries

- Concrete provider resource shapes, condition semantics, connection-detail
  keys, and ProviderConfig behavior require separately selected and pinned
  provider releases.
- For a generated extension list, make both the Kubernetes object name and the
  composition-resource name deterministic and collision-free; sanitize or hash
  input when it is not Kubernetes-name compatible.
- Keeping inline OpenTofu or Terraform HCL in a separate module is an authoring
  choice, not a Crossplane requirement. If both template languages are used,
  define clear ownership and escaping boundaries.

# Citations

[1] [Named rendered-resource handling](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L341-L350) and [resource-name helper](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L393-L408)
[2] [Function request observed-state snapshot](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L650-L673)
[3] [v2 connection-details initial-state guard](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/connection-details-composition.md#L296-L317)
[4] [Function pipeline readiness and XR status mutation scope](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L675-L703)
[5] [Managed-resource Ready and Synced condition meanings](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L854-L924)
[6] [Composite-status rendering behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L279-L313)
[7] [Kubernetes ObjectMeta name and generateName semantics](https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types.go#L109-L134)
[8] [Composite-resource name in observed state](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L650-L669)
[9] [Documented external-name behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L506-L568)
[10] [Runtime external-name annotation definition](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/meta/meta.go#L34-L39)
[11] [Provider-defined managed-resource settings boundary](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L24-L59)
[12] [Crossplane desired-state copy and deletion behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L675-L729)
[13] [Secret registers the existence-only check](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/secret.go#L7-L13), [`alwaysReady` returns true](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/healthchecks/registry.go#L27-L32), and [explicit readiness is preserved](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/fn.go#L133-L179)
[14] [Official aggregate Secret starts with empty data](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/manifests/guides/connection-details-composition/composition-go-templating.yaml#L53-L67)
