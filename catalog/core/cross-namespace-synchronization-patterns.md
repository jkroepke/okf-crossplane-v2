---
type: pattern
title: Cross-namespace synchronization patterns
description: Source-backed tradeoffs among provider-kubernetes and community replication controllers for working around Crossplane's namespaced-composition boundary.
resource: https://github.com/crossplane-contrib/provider-kubernetes
tags: [crossplane, composition, namespaces, synchronization, provider-kubernetes]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: provider-kubernetes-object-desired-and-observed-manifests
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L77-L99'
    title: 'provider-kubernetes Object desired and observed manifests'
  - id: namespaced-controller-target-parsing-and-lookup
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L368-L407'
    title: 'Namespaced controller target parsing and lookup'
  - id: in-cluster-providerconfig-example
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/examples/cluster/provider/config-in-cluster.yaml#L1-L8'
    title: 'In-cluster ProviderConfig example'
  - id: object-reference-and-field-patch-api
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L31-L75'
    title: 'Object reference and field-patch API'
  - id: control-plane-reference-resolution
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L684-L729'
    title: 'Control-plane reference resolution'
  - id: polling-and-alpha-watch-defaults
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L97'
    title: 'Polling and Alpha watch defaults'
  - id: observed-target-serialization-and-secret-sanitization
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L509-L530'
    title: 'Observed-target serialization and Secret sanitization'
  - id: secret-sanitization-flag-default
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L93'
    title: 'Secret sanitization flag default'
  - id: reflector-namespace-selection-and-annotations
    resource: 'https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/README.md#L77-L93'
    title: 'Reflector namespace selection and annotations'
  - id: reflector-secret-field-copy-implementation
    resource: 'https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/ES.Kubernetes.Reflector/Mirroring/SecretMirror.cs#L21-L49'
    title: 'Reflector Secret field-copy implementation'
  - id: kubernetes-replicator-supported-kinds-and-replication-modes
    resource: 'https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/README.md#L1-L19'
    title: 'kubernetes-replicator supported kinds and replication modes'
  - id: kubernetes-replicator-typed-controller-registration
    resource: 'https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/main.go#L95-L123'
    title: 'kubernetes-replicator typed controller registration'
  - id: kubernetes-replicator-source-deletion-lifecycle
    resource: 'https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/replicate/common/generic-replicator.go#L503-L618'
    title: 'kubernetes-replicator source-deletion lifecycle'
  - id: reflector-default-clusterrole
    resource: 'https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/helm/reflector/templates/clusterRole.yaml#L1-L16'
    title: 'Reflector default ClusterRole'
  - id: kubernetes-replicator-default-rbac
    resource: 'https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/deploy/helm-chart/kubernetes-replicator/templates/rbac.yaml#L15-L75'
    title: 'kubernetes-replicator default RBAC'
  - id: provider-kubernetes-server-side-apply-ownership
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/syncer.go#L68-L140'
    title: 'provider-kubernetes server-side apply ownership'
  - id: reflector-mit-license
    resource: 'https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/LICENSE#L1-L20'
    title: 'Reflector MIT license'
  - id: kubernetes-replicator-apache-2-0-license
    resource: 'https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/LICENSE.txt#L66-L128'
    title: 'kubernetes-replicator Apache-2.0 license'
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
under `status.atProvider.manifest`.[^provider-kubernetes-object-desired-and-observed-manifests] The namespaced controller parses the
embedded manifest and reads the target using that manifest's namespace and
name; it does not substitute the wrapper namespace. With an in-cluster
`ProviderConfig`, the target may therefore be in another namespace when RBAC
permits it.[^namespaced-controller-target-parsing-and-lookup][^in-cluster-providerconfig-example]

`references[].patchesFrom` can read a field from a named control-plane object,
including an explicitly namespaced source, and patch it into the target
manifest.[^object-reference-and-field-patch-api][^control-plane-reference-resolution] This supports selected-field synchronization, but the release
does not expose a generic “mirror this whole source object” primitive. Without
the explicitly Alpha watch feature, changes are found by periodic reconciliation;
the default poll interval is ten minutes.[^polling-and-alpha-watch-defaults]

The user's status advantage is real but narrower than “replicated back.” On
observation, the provider serializes the complete live target into the wrapper
`Object.status.atProvider.manifest`; it does not write target status into the
original object referenced by `patchesFrom`.[^observed-target-serialization-and-secret-sanitization] Secret data is also stored in
wrapper status by default unless `--sanitize-secrets=true` is enabled.[^observed-target-serialization-and-secret-sanitization][^secret-sanitization-flag-default]

# Community replication controllers

Reflector v10.0.59 uses annotations for manually declared or automatically
created Secret and ConfigMap mirrors. Namespace names, regular expressions, or
namespace label selectors can choose destinations.[^reflector-namespace-selection-and-annotations] It copies only the
typed data fields and deletes automatic mirrors when their source or eligibility
disappears; it is not an arbitrary-object controller.[^reflector-secret-field-copy-implementation]

kubernetes-replicator v2.12.4 supports annotation-driven push and pull patterns
for Secrets, ConfigMaps, Roles, RoleBindings, and ServiceAccounts.[^kubernetes-replicator-supported-kinds-and-replication-modes] Its
controllers copy kind-specific fields rather than whole objects: for example,
Secret data, ConfigMap data and binary data, or ServiceAccount image-pull
secrets.[^kubernetes-replicator-typed-controller-registration] Push targets are removed when their source is deleted, while pull
targets retain the object and have replicated fields removed.[^kubernetes-replicator-source-deletion-lifecycle]

Both controllers are a more natural fit than an `Object` wrapper when the goal
is one-way distribution of one of their supported built-in kinds. Neither can
manage the arbitrary custom resources discussed in issue #6759 or return their
status to Crossplane. Copying Secrets also broadens their exposure, and both
default charts grant cluster-wide access to the resource types they manage.[^reflector-default-clusterrole][^kubernetes-replicator-default-rbac]

# Limitations

- provider-kubernetes force-applies target fields by default. Coexistence with
  other field managers must be evaluated for the target resource.[^provider-kubernetes-server-side-apply-ownership]
- The community controllers are third-party illustrative patterns, not
  Crossplane-endorsed recommendations.
- Reflector is MIT licensed and kubernetes-replicator is Apache-2.0. No source
  or configuration was copied or adapted here.[^reflector-mit-license][^kubernetes-replicator-apache-2-0-license]

# Relationships

These patterns operate around the
[namespaced composition boundary](namespaced-composition-boundaries.md); they
do not change its Core enforcement.

[^provider-kubernetes-object-desired-and-observed-manifests]: [provider-kubernetes Object desired and observed manifests](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L77-L99)
[^namespaced-controller-target-parsing-and-lookup]: [Namespaced controller target parsing and lookup](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/namespaced/object/object.go#L368-L407)
[^in-cluster-providerconfig-example]: [In-cluster ProviderConfig example](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/examples/cluster/provider/config-in-cluster.yaml#L1-L8)
[^object-reference-and-field-patch-api]: [Object reference and field-patch API](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/apis/cluster/object/v1alpha2/types.go#L31-L75)
[^control-plane-reference-resolution]: [Control-plane reference resolution](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L684-L729)
[^polling-and-alpha-watch-defaults]: [Polling and Alpha watch defaults](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L97)
[^observed-target-serialization-and-secret-sanitization]: [Observed-target serialization and Secret sanitization](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/object.go#L509-L530)
[^secret-sanitization-flag-default]: [Secret sanitization flag default](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/cmd/provider/main.go#L84-L93)
[^reflector-namespace-selection-and-annotations]: [Reflector namespace selection and annotations](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/README.md#L77-L93)
[^reflector-secret-field-copy-implementation]: [Reflector Secret field-copy implementation](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/ES.Kubernetes.Reflector/Mirroring/SecretMirror.cs#L21-L49)
[^kubernetes-replicator-supported-kinds-and-replication-modes]: [kubernetes-replicator supported kinds and replication modes](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/README.md#L1-L19)
[^kubernetes-replicator-typed-controller-registration]: [kubernetes-replicator typed controller registration](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/main.go#L95-L123)
[^kubernetes-replicator-source-deletion-lifecycle]: [kubernetes-replicator source-deletion lifecycle](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/replicate/common/generic-replicator.go#L503-L618)
[^reflector-default-clusterrole]: [Reflector default ClusterRole](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/src/helm/reflector/templates/clusterRole.yaml#L1-L16)
[^kubernetes-replicator-default-rbac]: [kubernetes-replicator default RBAC](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/deploy/helm-chart/kubernetes-replicator/templates/rbac.yaml#L15-L75)
[^provider-kubernetes-server-side-apply-ownership]: [provider-kubernetes server-side apply ownership](https://github.com/crossplane-contrib/provider-kubernetes/blob/0ea671a4dab090ff3b14877d35086f1950fa35e3/internal/controller/cluster/object/syncer.go#L68-L140)
[^reflector-mit-license]: [Reflector MIT license](https://github.com/emberstack/kubernetes-reflector/blob/d5b9b2f83269cdb94647088a1fcf83b1b0081ff6/LICENSE#L1-L20)
[^kubernetes-replicator-apache-2-0-license]: [kubernetes-replicator Apache-2.0 license](https://github.com/mittwald/kubernetes-replicator/blob/44dc6db78c584771832a84a41cd06a1701a39fc0/LICENSE.txt#L66-L128)
