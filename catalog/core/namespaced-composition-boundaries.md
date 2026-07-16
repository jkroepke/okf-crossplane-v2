---
type: concept
title: Namespaced composition boundaries
description: "Crossplane v2 scope enforcement with PR #6588 release and source proof."
resource: https://github.com/crossplane/crossplane/pull/6588
tags: [crossplane, composition, namespaces, multitenancy]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - internal/controller/apiextensions/composite/composition_functions.go
  - internal/controller/apiextensions/composite/composition_render.go
  - internal/controller/apiextensions/composite/composition_functions_test.go
crossplane_release: v2.3.3
feature_state: Stable
feature_state_basis: Stable by repository default because selected released implementation and tests contain no explicit non-stable label and no relevant served alpha or beta API defining this controller behavior.
project_history_researched_at: 2026-07-16T00:00:00Z
---

# Overview

Crossplane v2.3.3 deliberately confines resources composed by a namespaced
composite resource (XR). A namespaced XR cannot compose a cluster-scoped
resource. If a function supplies a different namespace for a namespaced
composed resource, Crossplane reports `NamespaceOverridden` and uses the XR's
namespace instead.[1][2][3] Released unit and end-to-end tests cover the
rejection.[4][5]

Merged Crossplane PR #6588 introduced this guard. Its merge commit is contained
in Crossplane v2.0.0, and the selected v2.3.3 source retains the same
implementation.[6][7][8] The PR explains the intended Kubernetes
owner-reference rationale, but the released controller code and tests—not the
PR description—establish the behavior documented here.

Open issue #6759 reports that this boundary blocks tenant XRs that must manage
resources in centralized infrastructure namespaces. The complete human-authored
thread also describes Ingress placement, shared Kafka users and credentials,
cross-namespace reads, and composition-enforced security boundaries.[11] These
are user reports and proposals, not proof of supported behavior or an accepted
Crossplane roadmap.

# Behavior

The main implementation entrypoint is
`internal/controller/apiextensions/composite/composition_functions.go`.
For a newly desired resource with no namespace, it checks whether the XR has a
namespace and uses API discovery to determine whether the target kind is
namespaced. A cluster-scoped target produces a composition error before
metadata is rendered.[1] Rendering then sets every composed resource namespace
to the XR namespace when the XR is namespaced.[2] Observation also looks up
namespaced composed resources in the XR namespace.[9]

This has a narrow but important consequence: a cluster-scoped XRD produces a
cluster-scoped XR, whose namespace is empty. The rejection predicate and the
forced namespace assignment therefore do not run. The renderer explicitly
states that such an XR may compose a cluster-scoped resource or a resource in
any namespace.[2] This is a code-derived explanation of the guard; it does not
make a cluster-scoped target namespaced or grant any additional RBAC.

The thread's maintainer rationale is that cross-namespace controller ownership
and references run against Kubernetes conventions.[10] Other participants report
that the same-namespace rule complicates central service namespaces and tenant
security boundaries, and propose retaining legacy modes, composing a
cluster-scoped XR, or wrapping the target in provider-kubernetes `Object`.[11]
The issue remains open and is labelled `enhancement` and `composition` as of the
research timestamp.

# Limitations

- Issue #6759's cross-namespace `ExtraResources` report is retained as a report;
  this source batch did not establish its exact released Core fetch boundary.
- Claims, deprecated XRD v1, and legacy v1 XR semantics were excluded. The
  legacy workaround appears only as project-history context.

# Relationships

See [cross-namespace synchronization patterns](cross-namespace-synchronization-patterns.md)
for provider-kubernetes and community-controller tradeoffs that operate without
changing this Core boundary.

# Citations

[1] [Namespaced-XR enforcement before apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L515)
[2] [Rendered namespace override](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L74-L96)
[3] [Namespace override warning and event](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L518-L530)
[4] [Released unit tests for namespaced desired resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions_test.go#L580-L640)
[5] [Released end-to-end cluster-resource rejection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_compositions_test.go#L311-L329)
[6] [PR #6588](https://github.com/crossplane/crossplane/pull/6588)
[7] [PR #6588 merge implementation](https://github.com/crossplane/crossplane/blob/b22c2bb24d30ef2c199e198353e33402484efed3/internal/controller/apiextensions/composite/composition_functions.go#L441-L462)
[8] [v2.0.0 release containment](https://github.com/crossplane/crossplane/compare/b22c2bb24d30ef2c199e198353e33402484efed3...b639502e2f93680ff83417a0f517ec459ce079cc)
[9] [Namespaced composed-resource observation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L778-L810)
[10] [Maintainer comment on Kubernetes ownership conventions](https://github.com/crossplane/crossplane/issues/6759#issuecomment-3235190860)
[11] [Open issue #6759 and complete discussion](https://github.com/crossplane/crossplane/issues/6759)
