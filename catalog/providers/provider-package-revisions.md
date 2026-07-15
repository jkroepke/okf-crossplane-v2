---
type: Crossplane Provider
title: Provider package revisions and activation scope
description: The cluster-scoped Provider package lifecycle, parent-scoped active revision rule, and evidence-backed staging boundary.
resource: https://docs.crossplane.io/v2.3/packages/providers/
tags: [crossplane, providers, packages, revisions, upgrades]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [cluster/crds/pkg.crossplane.io_providers.yaml, cluster/crds/pkg.crossplane.io_providerrevisions.yaml, internal/controller/pkg/manager/reconciler.go, internal/controller/pkg/runtime/runtime_provider.go]
feature_state: Stable by repository default
---

# Overview

A `Provider` is a cluster-scoped package API. Updating its `spec.package` installs a new package image and creates a `ProviderRevision`; Crossplane owns those revisions rather than users editing them directly.[1][2]

Exactly one revision of a given `Provider` is Active at a time.[3] The package manager enforces that exclusivity within revisions whose parent-package label matches that `Provider` object, not globally across every Provider in the cluster.[4] Therefore, the statement “only one provider version can be installed per cluster” is too broad: the documentation displays several Active ProviderRevisions for distinct Provider objects.[5]

# Activation and upgrade behavior

`revisionActivationPolicy` defaults to `Automatic`; `Manual` prevents a newly installed revision being activated automatically. `revisionHistoryLimit` defaults to one retained inactive revision.[6] This is the documented single-cluster upgrade control: install a new revision, inspect it, then choose when to activate it.[2][3]

An Active revision applies provider runtime resources, including its Deployment. An inactive revision has its provider Deployment deleted.[7] A provider revision also establishes package API objects; when the relevant feature is enabled, that includes the provider CRDs converted to Managed Resource Definitions.[8]

# Staging and blast radius

The following are directly established:

- Provider, ProviderRevision, and provider API objects are cluster-scoped.[1][9]
- A provider upgrade changes which revision is Active for its parent Provider, and the Active revision controls the provider runtime Deployment.[3][7]

Those facts create a real cluster-wide blast-radius concern for a provider upgrade. They do **not** prove that multiple Kubernetes clusters are mandatory for all staging. Manual activation plus inactive-revision retention supplies a controlled single-cluster upgrade path.[2][6]

Using a separate cluster is a sound operational isolation requirement when staging means simultaneously active, isolated provider controller and API surfaces, or when cluster-wide CRD/controller effects are unacceptable. That last sentence is an inference from the scope and runtime behavior—not a Crossplane requirement stated by the selected sources. The selected sources also do not establish that two differently named Provider objects pointing to different versions of the same package are supported or safe.

# Relationships

Provider-specific API identity and migration risk are covered by [Provider implementation families and selection](provider-landscape.md). Provider-defined managed-resource schemas plug into the shared [Core managed-resource model](/core/managed-resources.md).

# Citations

[1] [Provider cluster scope and package purpose](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providers.yaml#L18-L41)
[2] [Provider upgrade creates a ProviderRevision](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L412-L421)
[3] [One Active revision per Provider](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L435-L442)
[4] [Parent-scoped revision deactivation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/manager/reconciler.go#L305-L401)
[5] [Multiple Active revisions for distinct Provider objects](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L426-L433)
[6] [Revision activation policy and retention defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providers.yaml#L126-L139) and [Manual activation behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L175-L209)
[7] [Active and inactive provider runtime resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_provider.go#L65-L190)
[8] [Provider package API establishment](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/revision/reconciler.go#L646-L664)
[9] [ProviderRevision cluster scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providerrevisions.yaml#L18-L56)
