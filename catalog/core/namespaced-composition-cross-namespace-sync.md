---
type: concept
title: Namespaced composition boundaries and cross-namespace synchronization
description: "Crossplane v2 same-namespace enforcement, the open issue #6759 report, and source-backed tradeoffs among provider-kubernetes and community replication controllers."
resource: https://github.com/crossplane/crossplane/issues/6759
tags: [crossplane, composition, namespaces, multitenancy, synchronization]
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

# Synchronization patterns

These options solve different problems; none changes the Core boundary.

- provider-kubernetes `Object` fits arbitrary Kubernetes kinds that Crossplane
  should reconcile through a managed-resource wrapper. It exposes the complete
  observed target, but uses an Alpha wrapper API and is not a transparent
  whole-object mirror.
- EmberStack Reflector fits one-way Secret or ConfigMap distribution. It copies
  typed data fields and provides no arbitrary-object or status feedback.
- mittwald kubernetes-replicator fits push or pull replication of its supported
  built-in kinds. It uses type-specific fields and cleanup and provides no
  arbitrary-object or status feedback.

## provider-kubernetes Object

provider-kubernetes v1.2.1 serves Alpha `Object` APIs. An `Object` embeds the
desired target under `spec.forProvider.manifest` and exposes the observed target
under `status.atProvider.manifest`.[9] The namespaced controller parses the
embedded manifest and reads the target using that manifest's namespace and
name; it does not substitute the wrapper namespace. With an in-cluster
`ProviderConfig`, the target may therefore be in another namespace when RBAC
permits it.[10][11]

`references[].patchesFrom` can read a field from a named control-plane object,
including an explicitly namespaced source, and patch it into the target
manifest.[12][13] This supports selected-field synchronization, but the release
does not expose a generic “mirror this whole source object” primitive. Without
the explicitly Alpha watch feature, changes are found by periodic reconciliation;
the default poll interval is ten minutes.[14]

The user's status advantage is real but narrower than “replicated back.” On
observation, the provider serializes the complete live target into the wrapper
`Object.status.atProvider.manifest`; it does not write target status into the
original object referenced by `patchesFrom`.[15] Secret data is also stored in
wrapper status by default unless `--sanitize-secrets=true` is enabled.[15][16]

## Community replication controllers

Reflector v10.0.59 uses annotations for manually declared or automatically
created Secret and ConfigMap mirrors. Namespace names, regular expressions, or
namespace label selectors can choose destinations.[17] It copies only the
typed data fields and deletes automatic mirrors when their source or eligibility
disappears; it is not an arbitrary-object controller.[18]

kubernetes-replicator v2.12.4 supports annotation-driven push and pull patterns
for Secrets, ConfigMaps, Roles, RoleBindings, and ServiceAccounts.[19] Its
controllers copy kind-specific fields rather than whole objects: for example,
Secret data, ConfigMap data and binary data, or ServiceAccount image-pull
secrets.[20] Push targets are removed when their source is deleted, while pull
targets retain the object and have replicated fields removed.[21]

Both controllers are a more natural fit than an `Object` wrapper when the goal
is one-way distribution of one of their supported built-in kinds. Neither can
manage the arbitrary custom resources discussed in issue #6759 or return their
status to Crossplane. Copying Secrets also broadens their exposure, and both
default charts grant cluster-wide access to the resource types they manage.[22][23]

# Limitations

- Issue #6759's cross-namespace `ExtraResources` report is retained as a report;
  this source batch did not establish its exact released Core fetch boundary.
- provider-kubernetes force-applies target fields by default. Coexistence with
  other field managers must be evaluated for the target resource.[24]
- The community controllers are third-party illustrative patterns, not
  Crossplane-endorsed recommendations.
- Reflector is MIT licensed and kubernetes-replicator is Apache-2.0. No source
  or configuration was copied or adapted here.[25][26]
- Claims, deprecated XRD v1, and legacy v1 XR semantics were excluded. The
  legacy workaround appears only as project-history context.

# Citations

[1] [Namespaced-XR enforcement before apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L500-L530)
[2] [Rendered namespace override](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L74-L96)
[3] [Namespace override warning and event](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L518-L530)
[4] [Released unit tests for namespaced desired resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions_test.go#L580-L640)
[5] [Released end-to-end cluster-resource rejection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_compositions_test.go#L311-L329)
[6] [Open issue #6759 and complete discussion](https://github.com/crossplane/crossplane/issues/6759)
[7] [Namespaced composed-resource observation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L778-L810)
[8] [Maintainer comment on Kubernetes ownership conventions](https://github.com/crossplane/crossplane/issues/6759#issuecomment-3235190860)
[9] [provider-kubernetes Object desired and observed manifests](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L77-L99)
[10] [Namespaced controller target parsing and lookup](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L368-L407)
[11] [In-cluster ProviderConfig example](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/examples/cluster/provider/config-in-cluster.yaml#L1-L8)
[12] [Object reference and field-patch API](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L31-L75)
[13] [Control-plane reference resolution](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L684-L729)
[14] [Polling and Alpha watch defaults](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L97)
[15] [Observed-target serialization and Secret sanitization](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L509-L530)
[16] [Secret sanitization flag default](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L93)
[17] [Reflector namespace selection and annotations](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/README.md#L77-L93)
[18] [Reflector Secret field-copy implementation](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/ES.Kubernetes.Reflector/Mirroring/SecretMirror.cs#L21-L49)
[19] [kubernetes-replicator supported kinds and replication modes](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/README.md#L1-L19)
[20] [kubernetes-replicator typed controller registration](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/main.go#L95-L123)
[21] [kubernetes-replicator source-deletion lifecycle](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/replicate/common/generic-replicator.go#L503-L618)
[22] [Reflector default ClusterRole](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/helm/reflector/templates/clusterRole.yaml#L1-L16)
[23] [kubernetes-replicator default RBAC](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/deploy/helm-chart/kubernetes-replicator/templates/rbac.yaml#L15-L75)
[24] [provider-kubernetes server-side apply ownership](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/syncer.go#L68-L140)
[25] [Reflector MIT license](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/LICENSE#L1-L20)
[26] [kubernetes-replicator Apache-2.0 license](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/LICENSE.txt#L66-L128)
