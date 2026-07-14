---
type: concept
title: Grant Crossplane access to composed Kubernetes resources
description: Crossplane is not authorized for every Kubernetes resource kind by default; operators grant additional composed-resource access with an aggregated ClusterRole.
resource: https://docs.crossplane.io/v2.3/composition/compositions/#grant-access-to-composed-resources
tags: [crossplane, core, composition, rbac, security]
timestamp: 2026-07-14T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/docs
source_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
source_paths:
  - content/v2.3/composition/compositions.md
  - content/v2.3/guides/pods.md
feature_state: Stable by repository default
---

# Overview

Crossplane uses its service account to create and manage the composed resources
returned by a Composition function pipeline.[1] That service account does not
have unrestricted access to every Kubernetes resource kind by default.

The default permission scope covers resources installed by Providers
(managed resources), resources defined by XRDs (composite resources), and
some Kubernetes kinds Crossplane needs for its own operation, such as
`Deployment`.[2] The documentation does not provide an exhaustive list of
those built-in kinds.

# Grant additional access

Before a Composition can manage another resource kind, create a Kubernetes
`ClusterRole` containing the required API groups, resources, and verbs. Add
this label so Kubernetes aggregates the new permissions into Crossplane's
primary `ClusterRole`:[3]

```yaml
metadata:
  labels:
    rbac.crossplane.io/aggregate-to-crossplane: "true"
```

The official example grants all verbs on the plural resource `clusters` in
the `postgresql.cnpg.io` API group so Crossplane can compose CloudNativePG
clusters.[4] Treat that manifest as an example, not as a minimum-permissions
template: the selected documentation does not enumerate the least-privilege
verbs needed for every reconciliation case.

# RBAC manager

Crossplane installs and enables its RBAC manager by default.[5] It
automatically grants the Crossplane service account access to managed and
composite resources and separately creates and binds roles for Provider
service accounts.[6]

If the RBAC manager is disabled, operators must manually grant the Crossplane
service account access to every kind it should compose, including managed and
composite resources.[7] The Helm value `rbacManager.deploy: false` disables it
at installation time; after installation, the documented procedure is to
delete the `crossplane-rbac-manager` Deployment.[5]

# Relationships

A [Composition](composition.md) defines the desired composed resources. This
concept describes the controller-side authorization Crossplane needs to apply
them. Crossplane controller permissions and Provider controller permissions
are distinct, even though the default RBAC manager helps configure both.[6]

# Limitations

Current v2.3 guidance uses an aggregated Kubernetes `ClusterRole`, not a
`ControllerConfig`, for this grant. The documentation establishes the
supported operator workflow but does not enumerate Crossplane's complete
default allowlist or the minimum verbs for arbitrary kinds.

The workflow is Stable by repository default because the selected current
documentation contains no explicit non-stable label and it is not tied to a
served alpha or beta Crossplane API.

# Citations

[1] [Crossplane creates function-produced composed resources with its service account](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L277-L280)
[2] [Default composed-resource permission scope](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L282-L288)
[3] [Aggregated ClusterRole procedure and required label](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L290-L321)
[4] [CloudNativePG ClusterRole example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L299-L316)
[5] [RBAC manager default and disable procedures](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L206-L227)
[6] [RBAC manager responsibilities](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L246-L260)
[7] [Manual grants required when the RBAC manager is disabled](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L324-L333)
