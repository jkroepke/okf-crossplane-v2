---
type: pattern
title: Observe Sveltos ClusterSummary deployment status
description: Fetch a Sveltos Profile's deterministic ClusterSummary and evaluate the deployment status of its copied configuration.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, extra-resources, readiness, sveltos]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: extraresources-selector-and-namespace-conversion
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62'
    title: 'ExtraResources selector and namespace conversion'
  - id: getextraresources-lookup
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L154'
    title: 'getExtraResources lookup'
  - id: sveltos-clustersummary-creation-namespace-labels-and-owner-reference
    resource: 'https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/controllers/profile_utils.go#L570-L632'
    title: 'Sveltos ClusterSummary creation, namespace, labels, and owner reference'
  - id: sveltos-deterministic-clustersummary-names
    resource: 'https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/lib/clusterops/clustersummary.go#L83-L104'
    title: 'Sveltos deterministic ClusterSummary names'
  - id: clustersummary-status-and-feature-summary-fields
    resource: 'https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/api/v1beta1/clustersummary_types.go#L43-L80'
    title: 'ClusterSummary status and feature-summary fields'
  - id: provisioned-feature-status
    resource: 'https://github.com/projectsveltos/libsveltos/blob/82cc79ba33929ffd061ee75f106a3bd8b70addcd/api/v1beta1/common_types.go#L413-L443'
    title: 'Provisioned feature status'
  - id: sveltos-complete-deployment-check
    resource: 'https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/controllers/utils.go#L157-L212'
    title: 'Sveltos complete-deployment check'
  - id: label-selection-omits-namespace-while-exact-name-selection-copies-it
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L41-L62'
    title: 'Label selection omits namespace while exact-name selection copies it'
  - id: function-auto-ready-cel-evaluates-only-the-observed-object
    resource: 'https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71'
    title: 'function-auto-ready CEL evaluates only the observed object'
  - id: sveltos-compares-profile-and-clustersummary-configuration-before-accepting-provisioned-status
    resource: 'https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/controllers/profile_utils.go#L147-L185'
    title: 'Sveltos compares Profile and ClusterSummary configuration before accepting provisioned status'
  - id: core-required-resource-fetcher-and-client-wiring
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L227'
    title: 'Core required-resource fetcher and client wiring'
  - id: wiring
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481'
    title: 'wiring'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths: [extraresources.go, function_maps.go, fn.go]
example_source_repository: projectsveltos/addon-controller
example_source_tag: v1.12.0
example_source_commit: b528b72dedf369566470709796d23d93fa1827b1
example_source_paths:
  - api/v1beta1/clustersummary_types.go
  - controllers/profile_utils.go
  - controllers/utils.go
  - lib/clusterops/clustersummary.go
supporting_source_repository: projectsveltos/libsveltos
supporting_source_tag: v1.12.0
supporting_source_commit: 82cc79ba33929ffd061ee75f106a3bd8b70addcd
supporting_source_paths: [api/v1beta1/common_types.go]
crossplane_source_repository: crossplane/crossplane
crossplane_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
crossplane_source_paths: [internal/xfn/required_resources.go, cmd/crossplane/core/core.go]
feature_state: Alpha
feature_state_basis: ExtraResources uses meta.gotemplating.fn.crossplane.io/v1alpha1.
---

# Sveltos pattern

This page specializes the generic
[non-composed-resource readiness pattern](non-composed-resource-readiness.md)
for Sveltos.

The Sveltos example below is an adapted community integration pattern. Sveltos
creates one namespaced `ClusterSummary` for every cluster selected by a
`Profile` or `ClusterProfile`. A namespaced `Profile` summary is named
`p--<profile>-<capi|sveltos>-<cluster>` and lives in the selected cluster's
namespace.[^sveltos-clustersummary-creation-namespace-labels-and-owner-reference][^sveltos-deterministic-clustersummary-names]

# Profile and summary example

Assumptions for this adaptable readiness fragment:

- the composed object is a namespaced `Profile` whose name equals the XR name;
- the XR provides `spec.cluster.name` and `spec.cluster.namespace` for a
  Sveltos cluster;
- the Profile configures at least one of Helm charts, policy references, or
  Kustomize references; and
- the Crossplane Core Deployment service account can `get` Sveltos
  `ClusterSummary` objects in the target namespace; the Function pod does not
  perform this read.[^core-required-resource-fetcher-and-client-wiring][^wiring]

The directive below requests one exact-name required resource, and the helper
reads its returned items from the Function request.[^extraresources-selector-and-namespace-conversion][^getextraresources-lookup]

```gotemplate
{{- $xr := .observed.composite.resource }}
{{- $profileName := $xr.metadata.name }}
{{- $clusterName := $xr.spec.cluster.name }}
{{- $clusterNamespace := $xr.spec.cluster.namespace }}
{{- $summaryName := printf "p--%s-sveltos-%s" $profileName $clusterName }}

{{- $ready := false }}
{{- $summaries := getExtraResources . "sveltosClusterSummary" | default (list) }}
{{- if eq (len $summaries) 1 }}
  {{- $summary := index $summaries 0 }}
  {{- $expectHelm := gt (len ($summary.spec.clusterProfileSpec.helmCharts | default (list))) 0 }}
  {{- $expectResources := gt (len ($summary.spec.clusterProfileSpec.policyRefs | default (list))) 0 }}
  {{- $expectKustomize := gt (len ($summary.spec.clusterProfileSpec.kustomizationRefs | default (list))) 0 }}
  {{- $helmReady := false }}
  {{- $resourcesReady := false }}
  {{- $kustomizeReady := false }}
  {{- $allReportedProvisioned := true }}
  {{- range $feature := ($summary.status.featureSummaries | default (list)) }}
    {{- if ne $feature.status "Provisioned" }}{{ $allReportedProvisioned = false }}{{- end }}
    {{- if and (eq $feature.featureID "Helm") (eq $feature.status "Provisioned") }}{{ $helmReady = true }}{{- end }}
    {{- if and (eq $feature.featureID "Resources") (eq $feature.status "Provisioned") }}{{ $resourcesReady = true }}{{- end }}
    {{- if and (eq $feature.featureID "Kustomize") (eq $feature.status "Provisioned") }}{{ $kustomizeReady = true }}{{- end }}
  {{- end }}
  {{- $hasExpected := or $expectHelm $expectResources $expectKustomize }}
  {{- $expectedReady := and (or (not $expectHelm) $helmReady) (or (not $expectResources) $resourcesReady) (or (not $expectKustomize) $kustomizeReady) }}
  {{- if and $hasExpected $expectedReady $allReportedProvisioned (not $summary.status.failureMessage) }}
    {{- $ready = true }}
  {{- end }}
{{- end }}
---
apiVersion: config.projectsveltos.io/v1beta1
kind: Profile
metadata:
  name: {{ $profileName }}
  namespace: {{ $clusterNamespace }}
  annotations:
    {{ setResourceNameAnnotation "sveltos-profile" }}
    gotemplating.fn.crossplane.io/ready: {{ ternary "True" "False" $ready | quote }}
spec:
  clusterRefs:
    - apiVersion: lib.projectsveltos.io/v1beta1
      kind: SveltosCluster
      name: {{ $clusterName }}
      namespace: {{ $clusterNamespace }}
  # Add the real helmCharts, policyRefs, or kustomizationRefs here.
---
apiVersion: meta.gotemplating.fn.crossplane.io/v1alpha1
kind: ExtraResources
requirements:
  sveltosClusterSummary:
    apiVersion: config.projectsveltos.io/v1beta1
    kind: ClusterSummary
    matchName: {{ $summaryName }}
    namespace: {{ $clusterNamespace }}
```

Sveltos records one entry per feature class under
`status.featureSummaries[]`. `Provisioned` is the successful state.[^clustersummary-status-and-feature-summary-fields][^provisioned-feature-status]
The example matches `Helm`, `Resources`, and `Kustomize` by `featureID`, requires
every configured class, and rejects any reported non-`Provisioned` entry. This
follows Sveltos's per-summary complete-deployment check.[^sveltos-complete-deployment-check] It evaluates the
configuration snapshot already copied into the `ClusterSummary`; it does not
prove that this snapshot matches a just-updated Profile.

# Why exact-name selection is required

Sveltos also labels summaries with profile, cluster name, and cluster type.
However, function-go-templating v0.12.2 returns from label-selector conversion
before copying `namespace`. Namespaced label lookup is therefore not reliable
in this release. Exact-name selection copies the namespace and is the supported
path for this pattern.[^label-selection-omits-namespace-while-exact-name-selection-copies-it]

# Limitations

- This is an adapted Crossplane/Sveltos integration example, not an official
  Sveltos Crossplane example. Validate it with the selected function release
  and a live management cluster; offline rendering needs supplied extra-resource
  observations.
- The abbreviated Profile spec prevents a complete synchronization comparison.
  After a Profile update, a stale ClusterSummary snapshot can transiently pass
  this deployment-status check. Production code that treats this as current
  Profile readiness must render the complete desired Profile spec once and
  require its Helm charts, policy references, and Kustomize references to
  `deepEqual` the corresponding `ClusterSummary.spec.clusterProfileSpec`
  fields before setting readiness true. Sveltos performs this separate sync
  check before its per-summary provisioned check.[^sveltos-compares-profile-and-clustersummary-configuration-before-accepting-provisioned-status]
- The exact-name strategy requires the cluster name and namespace. A
  `ClusterProfile` summary omits the `p--` prefix.[^sveltos-deterministic-clustersummary-names]
- The example treats a zero-feature Profile as not ready and must be updated if
  Sveltos adds another deployable feature class.
- Sveltos's ownership documentation depicts `controller: true`, but v1.12.0
  creation code does not set that owner-reference field. Runtime claims here
  follow the released implementation.[^sveltos-clustersummary-creation-namespace-labels-and-owner-reference]
- function-auto-ready cannot directly evaluate this fetched summary: its CEL
  activation contains only the matched observed composed object.[^function-auto-ready-cel-evaluates-only-the-observed-object]
- Sveltos addon-controller and libsveltos are Apache-2.0 licensed. No source
  code was copied; the example adapts their API and naming contracts.

# Relationships

See [ExtraResources](../extra-resources.md) for fetch and no-match semantics,
[non-composed-resource readiness](non-composed-resource-readiness.md) for the
generic pattern,
[manual readiness](manual-readiness.md) for annotation behavior, and
[function-auto-ready CEL](../../function-auto-ready/cel-health-checks.md) for the
composed-resource-only alternative.

[^extraresources-selector-and-namespace-conversion]: [ExtraResources selector and namespace conversion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62)
[^getextraresources-lookup]: [`getExtraResources` lookup](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L154)
[^sveltos-clustersummary-creation-namespace-labels-and-owner-reference]: [Sveltos ClusterSummary creation, namespace, labels, and owner reference](https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/controllers/profile_utils.go#L570-L632)
[^sveltos-deterministic-clustersummary-names]: [Sveltos deterministic ClusterSummary names](https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/lib/clusterops/clustersummary.go#L83-L104)
[^clustersummary-status-and-feature-summary-fields]: [ClusterSummary status and feature-summary fields](https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/api/v1beta1/clustersummary_types.go#L43-L80)
[^provisioned-feature-status]: [`Provisioned` feature status](https://github.com/projectsveltos/libsveltos/blob/82cc79ba33929ffd061ee75f106a3bd8b70addcd/api/v1beta1/common_types.go#L413-L443)
[^sveltos-complete-deployment-check]: [Sveltos complete-deployment check](https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/controllers/utils.go#L157-L212)
[^label-selection-omits-namespace-while-exact-name-selection-copies-it]: [Label selection omits namespace while exact-name selection copies it](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L41-L62)
[^function-auto-ready-cel-evaluates-only-the-observed-object]: [function-auto-ready CEL evaluates only the observed object](https://github.com/crossplane-contrib/function-auto-ready/blob/ed7886de159af73b9d6976f04f9171ec7a4cb411/cel/resolver.go#L30-L71)
[^sveltos-compares-profile-and-clustersummary-configuration-before-accepting-provisioned-status]: [Sveltos compares Profile and ClusterSummary configuration before accepting provisioned status](https://github.com/projectsveltos/addon-controller/blob/b528b72dedf369566470709796d23d93fa1827b1/controllers/profile_utils.go#L147-L185)
[^core-required-resource-fetcher-and-client-wiring]: [Core required-resource fetcher and client wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L227) and [wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
[^wiring]: [wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
