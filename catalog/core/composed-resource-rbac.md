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
supporting_sources:
  - repository: crossplane/crossplane
    commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
    paths:
      - internal/xfn/required_resources.go
      - internal/xfn/function_runner.go
      - internal/controller/apiextensions/composite/composition_functions.go
      - internal/controller/pkg/runtime/runtime_function.go
      - cmd/crossplane/core/core.go
      - cluster/charts/crossplane/templates/deployment.yaml
feature_state: Not stated by selected sources
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

# Required-resource reads are a separate path

Function requirements such as function-go-templating `ExtraResources` do not
cause the Function pod to read Kubernetes directly. Crossplane Core receives
the requirement and performs an exact-name `Get` or a label-based `List` with
its Kubernetes client.[8][9] Grant those reads to the Crossplane Core
Deployment service account selected by the Helm deployment template, not the
Function pod service account.[12]

The selector determines the required scope. In the selected release an empty
namespace on a label selector produces an all-namespace list, so a template-side
filter cannot reduce the earlier read permission.[8] The deployed Core client
is cache-backed for unstructured resources; account for its informer access
when constructing the grant rather than treating `get` and `list` as a proven
complete minimum.[9]

This read path and the composed-resource apply path are performed by the same
Core process but require different verbs and should be reviewed separately.
Provider controller credentials and the Function runtime service account are
additional, distinct identities.[10][11]

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
See [ExtraResources](../functions/function-go-templating/extra-resources.md) for
selector and namespace behavior.

# Limitations

Current v2.3 guidance uses an aggregated Kubernetes `ClusterRole`, not a
`ControllerConfig`, for this grant. The documentation establishes the
supported operator workflow but does not enumerate Crossplane's complete
default allowlist or the minimum verbs for arbitrary kinds.

The workflow's maturity is **Not stated by selected sources**. Current released
documentation establishes the supported procedure, but a release selection is
not itself a lifecycle label.

# Citations

[1] [Crossplane creates function-produced composed resources with its service account](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L277-L280)
[2] [Default composed-resource permission scope](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L282-L288)
[3] [Aggregated ClusterRole procedure and required label](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L290-L321)
[4] [CloudNativePG ClusterRole example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L299-L316)
[5] [RBAC manager default and disable procedures](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L206-L227)
[6] [RBAC manager responsibilities](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L246-L260)
[7] [Manual grants required when the RBAC manager is disabled](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L324-L333)
[8] [Core required-resource `Get` and `List` paths](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L154-L227)
[9] [Core cache-backed client and fetcher wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L361-L423) and [fetcher wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
[10] [Composed-resource apply path](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L615-L658)
[11] [Function runtime invocation and separate pod identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/function_runner.go#L90-L166) and [Function Deployment service account](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_function.go#L120-L148)
[12] [Core Deployment service-account selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/charts/crossplane/templates/deployment.yaml#L41-L56)
