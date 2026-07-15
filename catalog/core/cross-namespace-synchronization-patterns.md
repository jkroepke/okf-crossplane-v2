---
type: pattern
title: Cross-namespace synchronization patterns
description: Source-backed tradeoffs among provider-kubernetes and community replication controllers for working around Crossplane's namespaced-composition boundary.
resource: https://github.com/crossplane-contrib/provider-kubernetes
tags: [crossplane, composition, namespaces, synchronization, provider-kubernetes]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/provider-kubernetes
source_tag: v1.2.1
source_commit: 0ea671a4dab090ff3b14877d35086f1950fa35e3
supporting_source_repositories:
  - emberstack/kubernetes-reflector@d5b9b2f83269cdb94647088a1fcf83b1b0081ff6
  - mittwald/kubernetes-replicator@44dc6db78c584771832a84a41cd06a1701a39fc0
---

# Synchronization patterns

These options solve different problems; none changes the
[Core boundary](namespaced-composition-boundaries.md).

- provider-kubernetes `Object` fits arbitrary Kubernetes kinds that Crossplane
  should reconcile through a managed-resource wrapper. It exposes the complete
  observed target, but uses an Alpha wrapper API and is not a transparent
  whole-object mirror.
- EmberStack Reflector fits one-way Secret or ConfigMap distribution. It copies
  typed data fields and provides no arbitrary-object or status feedback.
- mittwald kubernetes-replicator fits push or pull replication of its supported
  built-in kinds. It uses type-specific fields and cleanup and provides no
  arbitrary-object or status feedback.

# provider-kubernetes Object

provider-kubernetes v1.2.1 serves Alpha `Object` APIs. An `Object` embeds the
desired target under `spec.forProvider.manifest` and exposes the observed target
under `status.atProvider.manifest`.[1] The namespaced controller parses the
embedded manifest and reads the target using that manifest's namespace and
name; it does not substitute the wrapper namespace. With an in-cluster
`ProviderConfig`, the target may therefore be in another namespace when RBAC
permits it.[2][3]

`references[].patchesFrom` can read a field from a named control-plane object,
including an explicitly namespaced source, and patch it into the target
manifest.[4][5] This supports selected-field synchronization, but the release
does not expose a generic “mirror this whole source object” primitive. Without
the explicitly Alpha watch feature, changes are found by periodic reconciliation;
the default poll interval is ten minutes.[6]

The user's status advantage is real but narrower than “replicated back.” On
observation, the provider serializes the complete live target into the wrapper
`Object.status.atProvider.manifest`; it does not write target status into the
original object referenced by `patchesFrom`.[7] Secret data is also stored in
wrapper status by default unless `--sanitize-secrets=true` is enabled.[7][8]

# Community replication controllers

Reflector v10.0.59 uses annotations for manually declared or automatically
created Secret and ConfigMap mirrors. Namespace names, regular expressions, or
namespace label selectors can choose destinations.[9] It copies only the
typed data fields and deletes automatic mirrors when their source or eligibility
disappears; it is not an arbitrary-object controller.[10]

kubernetes-replicator v2.12.4 supports annotation-driven push and pull patterns
for Secrets, ConfigMaps, Roles, RoleBindings, and ServiceAccounts.[11] Its
controllers copy kind-specific fields rather than whole objects: for example,
Secret data, ConfigMap data and binary data, or ServiceAccount image-pull
secrets.[12] Push targets are removed when their source is deleted, while pull
targets retain the object and have replicated fields removed.[13]

Both controllers are a more natural fit than an `Object` wrapper when the goal
is one-way distribution of one of their supported built-in kinds. Neither can
manage the arbitrary custom resources discussed in issue #6759 or return their
status to Crossplane. Copying Secrets also broadens their exposure, and both
default charts grant cluster-wide access to the resource types they manage.[14][15]

# Limitations

- provider-kubernetes force-applies target fields by default. Coexistence with
  other field managers must be evaluated for the target resource.[16]
- The community controllers are third-party illustrative patterns, not
  Crossplane-endorsed recommendations.
- Reflector is MIT licensed and kubernetes-replicator is Apache-2.0. No source
  or configuration was copied or adapted here.[17][18]

# Relationships

These patterns operate around the
[namespaced composition boundary](namespaced-composition-boundaries.md); they
do not change its Core enforcement.

# Citations

[1] [provider-kubernetes Object desired and observed manifests](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L77-L99)
[2] [Namespaced controller target parsing and lookup](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L368-L407)
[3] [In-cluster ProviderConfig example](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/examples/cluster/provider/config-in-cluster.yaml#L1-L8)
[4] [Object reference and field-patch API](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L31-L75)
[5] [Control-plane reference resolution](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L684-L729)
[6] [Polling and Alpha watch defaults](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L97)
[7] [Observed-target serialization and Secret sanitization](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L509-L530)
[8] [Secret sanitization flag default](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L93)
[9] [Reflector namespace selection and annotations](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/README.md#L77-L93)
[10] [Reflector Secret field-copy implementation](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/ES.Kubernetes.Reflector/Mirroring/SecretMirror.cs#L21-L49)
[11] [kubernetes-replicator supported kinds and replication modes](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/README.md#L1-L19)
[12] [kubernetes-replicator typed controller registration](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/main.go#L95-L123)
[13] [kubernetes-replicator source-deletion lifecycle](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/replicate/common/generic-replicator.go#L503-L618)
[14] [Reflector default ClusterRole](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/helm/reflector/templates/clusterRole.yaml#L1-L16)
[15] [kubernetes-replicator default RBAC](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/deploy/helm-chart/kubernetes-replicator/templates/rbac.yaml#L15-L75)
[16] [provider-kubernetes server-side apply ownership](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/syncer.go#L68-L140)
[17] [Reflector MIT license](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/LICENSE#L1-L20)
[18] [kubernetes-replicator Apache-2.0 license](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/LICENSE.txt#L66-L128)
