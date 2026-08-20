---
type: Crossplane Provider
title: Provider package revisions and activation scope
description: The cluster-scoped Provider package lifecycle, parent-scoped active revision rule, and evidence-backed staging boundary.
resource: https://docs.crossplane.io/v2.3/packages/providers/
tags: [crossplane, providers, packages, revisions, upgrades]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: provider-cluster-scope-and-package-purpose
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providers.yaml#L18-L41'
    title: 'Provider cluster scope and package purpose'
  - id: provider-upgrade-creates-a-providerrevision
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L412-L421'
    title: 'Provider upgrade creates a ProviderRevision'
  - id: one-active-revision-per-provider
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L435-L442'
    title: 'One Active revision per Provider'
  - id: parent-scoped-revision-deactivation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/manager/reconciler.go#L305-L401'
    title: 'Parent-scoped revision deactivation'
  - id: multiple-active-revisions-for-distinct-provider-objects
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L426-L433'
    title: 'Multiple Active revisions for distinct Provider objects'
  - id: revision-activation-policy-and-retention-defaults
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providers.yaml#L126-L139'
    title: 'Revision activation policy and retention defaults'
  - id: manual-activation-behavior
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L175-L209'
    title: 'Manual activation behavior'
  - id: active-and-inactive-provider-runtime-resources
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_provider.go#L65-L190'
    title: 'Active and inactive provider runtime resources'
  - id: provider-package-api-establishment
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/revision/reconciler.go#L646-L664'
    title: 'Provider package API establishment'
  - id: providerrevision-cluster-scope
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providerrevisions.yaml#L18-L56'
    title: 'ProviderRevision cluster scope'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/pkg.crossplane.io_providers.yaml
  - cluster/crds/pkg.crossplane.io_providerrevisions.yaml
  - internal/controller/pkg/manager/reconciler.go
  - internal/controller/pkg/runtime/runtime_provider.go
  - internal/controller/pkg/revision/reconciler.go
documentation_repository: crossplane/docs
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths:
  - content/v2.3/packages/providers.md
feature_state: Stable by repository default
feature_state_basis: Provider and ProviderRevision each serve only v1 in the selected release, with no explicit non-stable label or deprecation metadata; v1 alone is not used as proof.
---

# Overview

A `Provider` is a cluster-scoped package API. Updating its `spec.package` installs a new package image and creates a `ProviderRevision`; Crossplane owns those revisions rather than users editing them directly.[^provider-cluster-scope-and-package-purpose][^provider-upgrade-creates-a-providerrevision]

Exactly one revision of a given `Provider` is Active at a time.[^one-active-revision-per-provider] The package manager enforces that exclusivity within revisions whose parent-package label matches that `Provider` object, not globally across every Provider in the cluster.[^parent-scoped-revision-deactivation] Therefore, the statement “only one provider version can be installed per cluster” is too broad: the documentation displays several Active ProviderRevisions for distinct Provider objects.[^multiple-active-revisions-for-distinct-provider-objects]

# Activation and upgrade behavior

`revisionActivationPolicy` defaults to `Automatic`; `Manual` prevents a newly installed revision being activated automatically. `revisionHistoryLimit` defaults to one retained inactive revision.[^revision-activation-policy-and-retention-defaults][^manual-activation-behavior] This is the documented single-cluster upgrade control: install a new revision, inspect it, then choose when to activate it.[^provider-upgrade-creates-a-providerrevision][^one-active-revision-per-provider]

The selected v2.3 documentation does not state the exact supported mutation or
command for that manual activation step. Do not infer direct ProviderRevision
editing, a `desiredState` patch, a parent-policy toggle, or package reapply from
the existence of the policy alone; resolve the current supported promotion
workflow before operational use.

An Active revision applies provider runtime resources, including its Deployment. An inactive revision has its provider Deployment deleted.[^active-and-inactive-provider-runtime-resources] A provider revision also establishes package API objects; when the relevant feature is enabled, that includes the provider CRDs converted to Managed Resource Definitions.[^provider-package-api-establishment]

# Staging and blast radius

The following are directly established:

- Provider, ProviderRevision, and provider API objects are cluster-scoped.[^provider-cluster-scope-and-package-purpose][^providerrevision-cluster-scope]
- A provider upgrade changes which revision is Active for its parent Provider, and the Active revision controls the provider runtime Deployment.[^one-active-revision-per-provider][^active-and-inactive-provider-runtime-resources]

Those facts create a real cluster-wide blast-radius concern for a provider upgrade. They do **not** prove that multiple Kubernetes clusters are mandatory for all staging. Manual activation plus inactive-revision retention supplies a controlled single-cluster upgrade path.[^provider-upgrade-creates-a-providerrevision][^revision-activation-policy-and-retention-defaults][^manual-activation-behavior]

Using a separate cluster is a sound operational isolation requirement when staging means simultaneously active, isolated provider controller and API surfaces, or when cluster-wide CRD/controller effects are unacceptable. That last sentence is an inference from the scope and runtime behavior—not a Crossplane requirement stated by the selected sources. The selected sources also do not establish that two differently named Provider objects pointing to different versions of the same package are supported or safe.

# Relationships

Provider-specific API identity and migration risk are covered by [Provider implementation families and selection](provider-landscape.md). Provider-defined managed-resource schemas plug into the shared [Core managed-resource model](/core/managed-resources.md).

[^provider-cluster-scope-and-package-purpose]: [Provider cluster scope and package purpose](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providers.yaml#L18-L41)
[^provider-upgrade-creates-a-providerrevision]: [Provider upgrade creates a ProviderRevision](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L412-L421)
[^one-active-revision-per-provider]: [One Active revision per Provider](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L435-L442)
[^parent-scoped-revision-deactivation]: [Parent-scoped revision deactivation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/manager/reconciler.go#L305-L401)
[^multiple-active-revisions-for-distinct-provider-objects]: [Multiple Active revisions for distinct Provider objects](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L426-L433)
[^revision-activation-policy-and-retention-defaults]: [Revision activation policy and retention defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providers.yaml#L126-L139) and [Manual activation behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L175-L209)
[^manual-activation-behavior]: [Manual activation behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/providers.md#L175-L209)
[^active-and-inactive-provider-runtime-resources]: [Active and inactive provider runtime resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_provider.go#L65-L190)
[^provider-package-api-establishment]: [Provider package API establishment](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/revision/reconciler.go#L646-L664)
[^providerrevision-cluster-scope]: [ProviderRevision cluster scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_providerrevisions.yaml#L18-L56)
