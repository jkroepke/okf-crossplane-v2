---
type: concept
title: Namespaced composition boundaries
description: "Crossplane v2 scope enforcement with PR #6588 release and source proof."
resource: https://github.com/crossplane/crossplane/pull/6588
tags: [crossplane, composition, namespaces, multitenancy]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: namespaced-xr-enforcement-before-apply
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L515'
    title: 'Namespaced-XR enforcement before apply'
  - id: rendered-namespace-override
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L74-L96'
    title: 'Rendered namespace override'
  - id: namespace-override-warning-and-event
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L518-L530'
    title: 'Namespace override warning and event'
  - id: released-unit-tests-for-namespaced-desired-resources
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions_test.go#L580-L640'
    title: 'Released unit tests for namespaced desired resources'
  - id: released-end-to-end-cluster-resource-rejection
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_compositions_test.go#L311-L329'
    title: 'Released end-to-end cluster-resource rejection'
  - id: pr-6588
    resource: 'https://github.com/crossplane/crossplane/pull/6588'
    title: 'PR #6588'
  - id: pr-6588-merge-implementation
    resource: 'https://github.com/crossplane/crossplane/blob/b22c2bb24d30ef2c199e198353e33402484efed3/internal/controller/apiextensions/composite/composition_functions.go#L441-L462'
    title: 'PR #6588 merge implementation'
  - id: v2-0-0-release-containment
    resource: 'https://github.com/crossplane/crossplane/compare/b22c2bb24d30ef2c199e198353e33402484efed3...b639502e2f93680ff83417a0f517ec459ce079cc'
    title: 'v2.0.0 release containment'
  - id: namespaced-composed-resource-observation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L778-L810'
    title: 'Namespaced composed-resource observation'
  - id: maintainer-comment-on-kubernetes-ownership-conventions
    resource: 'https://github.com/crossplane/crossplane/issues/6759#issuecomment-3235190860'
    title: 'Maintainer comment on Kubernetes ownership conventions'
  - id: open-issue-6759-and-complete-discussion
    resource: 'https://github.com/crossplane/crossplane/issues/6759'
    title: 'Open issue #6759 and complete discussion'
  - id: core-required-resource-exact-name-and-label-fetch-paths
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L154-L227'
    title: 'Core required-resource exact-name and label fetch paths'
  - id: function-go-templating-namespace-conversion-boundary
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L41-L62'
    title: 'function-go-templating namespace conversion boundary'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - internal/controller/apiextensions/composite/composition_functions.go
  - internal/controller/apiextensions/composite/composition_render.go
  - internal/controller/apiextensions/composite/composition_functions_test.go
supporting_source_repository: crossplane-contrib/function-go-templating
supporting_source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
supporting_source_paths: [extraresources.go]
crossplane_release: v2.3.3
feature_state: Not stated by selected sources
feature_state_basis: Selected released implementation and tests establish current controller behavior, but do not state a lifecycle label.
project_history_researched_at: 2026-07-16T00:00:00Z
---

# Overview

Crossplane v2.3.3 deliberately confines resources composed by a namespaced
composite resource (XR). A namespaced XR cannot compose a cluster-scoped
resource. If a function supplies a different namespace for a namespaced
composed resource, Crossplane reports `NamespaceOverridden` and uses the XR's
namespace instead.[^namespaced-xr-enforcement-before-apply][^rendered-namespace-override][^namespace-override-warning-and-event] Released unit and end-to-end tests cover the
rejection.[^released-unit-tests-for-namespaced-desired-resources][^released-end-to-end-cluster-resource-rejection]

Merged Crossplane PR #6588 introduced this guard. Its merge commit is contained
in Crossplane v2.0.0, and the selected v2.3.3 source retains the same
implementation.[^pr-6588][^pr-6588-merge-implementation][^v2-0-0-release-containment] The PR explains the intended Kubernetes
owner-reference rationale, but the released controller code and tests—not the
PR description—establish the behavior documented here.

Open issue #6759 reports that this boundary blocks tenant XRs that must manage
resources in centralized infrastructure namespaces. The complete human-authored
thread also describes Ingress placement, shared Kafka users and credentials,
cross-namespace reads, and composition-enforced security boundaries.[^open-issue-6759-and-complete-discussion] These
are user reports and proposals, not proof of supported behavior or an accepted
Crossplane roadmap.

# Behavior

The main implementation entrypoint is
`internal/controller/apiextensions/composite/composition_functions.go`.
For a newly desired resource with no namespace, it checks whether the XR has a
namespace and uses API discovery to determine whether the target kind is
namespaced. A cluster-scoped target produces a composition error before
metadata is rendered.[^namespaced-xr-enforcement-before-apply] Rendering then sets every composed resource namespace
to the XR namespace when the XR is namespaced.[^rendered-namespace-override] Observation also looks up
namespaced composed resources in the XR namespace.[^namespaced-composed-resource-observation]

This has a narrow but important consequence: a cluster-scoped XRD produces a
cluster-scoped XR, whose namespace is empty. The rejection predicate and the
forced namespace assignment therefore do not run. The renderer explicitly
states that such an XR may compose a cluster-scoped resource or a resource in
any namespace.[^rendered-namespace-override] This is a code-derived explanation of the guard; it does not
make a cluster-scoped target namespaced or grant any additional RBAC.

The thread's maintainer rationale is that cross-namespace controller ownership
and references run against Kubernetes conventions.[^maintainer-comment-on-kubernetes-ownership-conventions] Other participants report
that the same-namespace rule complicates central service namespaces and tenant
security boundaries, and propose retaining legacy modes, composing a
cluster-scoped XR, or wrapping the target in provider-kubernetes `Object`.[^open-issue-6759-and-complete-discussion]
The issue remains open and is labelled `enhancement` and `composition` as of the
research timestamp.

# Required-resource boundary

Function required resources are fetched by Crossplane Core separately from
composed-resource rendering. Exact-name selectors call `Get` with the supplied
namespace; label selectors call `List`, and an empty namespace lists across
namespaces.[^core-required-resource-exact-name-and-label-fetch-paths] This fetch path is not constrained by the namespaced-XR
composed-resource namespace override described above.

For function-go-templating v0.12.2, only exact-name ExtraResources conversion
copies the requested namespace. Its label path returns without the namespace,
so Core receives an empty namespace and lists across namespaces, subject to
the Crossplane Core service account's RBAC.[^function-go-templating-namespace-conversion-boundary] Issue #6759 remains only a
report; the selected released code establishes this narrower fetch behavior.

# Limitations

- Required-resource reads do not authorize cross-namespace composed-resource
  writes and do not weaken the same-namespace rendering guard.
- Claims, deprecated XRD v1, and legacy v1 XR semantics were excluded. The
  legacy workaround appears only as project-history context.

# Relationships

See [cross-namespace synchronization patterns](cross-namespace-synchronization-patterns.md)
for provider-kubernetes and community-controller tradeoffs that operate without
changing this Core boundary. See
[ExtraResources](../functions/function-go-templating/extra-resources.md) for the
function-specific selector limitation.

[^namespaced-xr-enforcement-before-apply]: [Namespaced-XR enforcement before apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L515)
[^rendered-namespace-override]: [Rendered namespace override](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L74-L96)
[^namespace-override-warning-and-event]: [Namespace override warning and event](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L518-L530)
[^released-unit-tests-for-namespaced-desired-resources]: [Released unit tests for namespaced desired resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions_test.go#L580-L640)
[^released-end-to-end-cluster-resource-rejection]: [Released end-to-end cluster-resource rejection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_compositions_test.go#L311-L329)
[^pr-6588]: [PR #6588](https://github.com/crossplane/crossplane/pull/6588)
[^pr-6588-merge-implementation]: [PR #6588 merge implementation](https://github.com/crossplane/crossplane/blob/b22c2bb24d30ef2c199e198353e33402484efed3/internal/controller/apiextensions/composite/composition_functions.go#L441-L462)
[^v2-0-0-release-containment]: [v2.0.0 release containment](https://github.com/crossplane/crossplane/compare/b22c2bb24d30ef2c199e198353e33402484efed3...b639502e2f93680ff83417a0f517ec459ce079cc)
[^namespaced-composed-resource-observation]: [Namespaced composed-resource observation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L778-L810)
[^maintainer-comment-on-kubernetes-ownership-conventions]: [Maintainer comment on Kubernetes ownership conventions](https://github.com/crossplane/crossplane/issues/6759#issuecomment-3235190860)
[^open-issue-6759-and-complete-discussion]: [Open issue #6759 and complete discussion](https://github.com/crossplane/crossplane/issues/6759)
[^core-required-resource-exact-name-and-label-fetch-paths]: [Core required-resource exact-name and label fetch paths](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L154-L227)
[^function-go-templating-namespace-conversion-boundary]: [function-go-templating namespace conversion boundary](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L41-L62)
