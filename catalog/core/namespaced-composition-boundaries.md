---
type: concept
title: Namespaced composition boundaries
description: "Crossplane v2 same-namespace enforcement and the open issue #6759 report."
resource: https://github.com/crossplane/crossplane/issues/6759
tags: [crossplane, composition, namespaces, multitenancy]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - internal/controller/apiextensions/composite/composition_functions.go
  - internal/controller/apiextensions/composite/composition_render.go
crossplane_release: v2.3.3
feature_state: Stable
feature_state_basis: Stable by repository default because selected released implementation and tests contain no explicit non-stable label and no relevant served alpha or beta API defining this controller behavior.
project_history_researched_at: 2026-07-14T18:41:12+02:00
---

# Overview

Crossplane v2.3.3 deliberately confines resources composed by a namespaced
composite resource (XR). A namespaced XR cannot compose a cluster-scoped
resource. If a function supplies a different namespace for a namespaced
composed resource, Crossplane reports `NamespaceOverridden` and uses the XR's
namespace instead.[1][2][3] Released unit and end-to-end tests cover both
rules.[4][5]

Open issue #6759 reports that this boundary blocks tenant XRs that must manage
resources in centralized infrastructure namespaces. The complete human-authored
thread also describes Ingress placement, shared Kafka users and credentials,
cross-namespace reads, and composition-enforced security boundaries.[6] These
are user reports and proposals, not proof of supported behavior or an accepted
Crossplane roadmap.

# Behavior

The main implementation entrypoint is
`internal/controller/apiextensions/composite/composition_functions.go`.
Before applying a desired resource, it rejects a cluster-scoped kind for a
namespaced XR and warns when a desired namespace differs.[1] Rendering then
sets the composed resource namespace to the XR namespace.[2] Observation also
looks up namespaced composed resources in the XR namespace.[7]

The thread's maintainer rationale is that cross-namespace controller ownership
and references run against Kubernetes conventions.[8] Other participants report
that the same-namespace rule complicates central service namespaces and tenant
security boundaries, and propose retaining legacy modes, composing a
cluster-scoped XR, or wrapping the target in provider-kubernetes `Object`.[6]
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

[1] [Namespaced-XR enforcement before apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L530)
[2] [Rendered namespace override](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L74-L96)
[3] [Namespace override warning and event](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L518-L530)
[4] [Released unit tests for namespaced desired resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions_test.go#L580-L640)
[5] [Released end-to-end cluster-resource rejection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_compositions_test.go#L311-L329)
[6] [Open issue #6759 and complete discussion](https://github.com/crossplane/crossplane/issues/6759)
[7] [Namespaced composed-resource observation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L778-L810)
[8] [Maintainer comment on Kubernetes ownership conventions](https://github.com/crossplane/crossplane/issues/6759#issuecomment-3235190860)
