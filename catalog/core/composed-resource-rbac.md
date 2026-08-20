---
type: concept
title: Grant Crossplane access to composed Kubernetes resources
description: Crossplane is not authorized for every Kubernetes resource kind by default; operators grant additional composed-resource access with an aggregated ClusterRole.
resource: https://docs.crossplane.io/v2.3/composition/compositions/#grant-access-to-composed-resources
tags: [crossplane, core, composition, rbac, security]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: crossplane-creates-function-produced-composed-resources-with-its-service-account
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L277-L280'
    title: 'Crossplane creates function-produced composed resources with its service account'
  - id: default-composed-resource-permission-scope
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L282-L288'
    title: 'Default composed-resource permission scope'
  - id: aggregated-clusterrole-procedure-and-required-label
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L290-L321'
    title: 'Aggregated ClusterRole procedure and required label'
  - id: cloudnativepg-clusterrole-example
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L299-L316'
    title: 'CloudNativePG ClusterRole example'
  - id: rbac-manager-default-and-disable-procedures
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L206-L227'
    title: 'RBAC manager default and disable procedures'
  - id: rbac-manager-responsibilities
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L246-L260'
    title: 'RBAC manager responsibilities'
  - id: manual-grants-required-when-the-rbac-manager-is-disabled
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L324-L333'
    title: 'Manual grants required when the RBAC manager is disabled'
  - id: core-required-resource-get-and-list-paths
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L154-L227'
    title: 'Core required-resource Get and List paths'
  - id: core-cache-backed-client-and-fetcher-wiring
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L361-L423'
    title: 'Core cache-backed client and fetcher wiring'
  - id: fetcher-wiring
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481'
    title: 'fetcher wiring'
  - id: composed-resource-apply-path
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L615-L658'
    title: 'Composed-resource apply path'
  - id: function-runtime-invocation-and-separate-pod-identity
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/function_runner.go#L90-L166'
    title: 'Function runtime invocation and separate pod identity'
  - id: function-deployment-service-account
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_function.go#L120-L148'
    title: 'Function Deployment service account'
  - id: core-deployment-service-account-selection
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/charts/crossplane/templates/deployment.yaml#L41-L56'
    title: 'Core Deployment service-account selection'
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
returned by a Composition function pipeline.[^crossplane-creates-function-produced-composed-resources-with-its-service-account] That service account does not
have unrestricted access to every Kubernetes resource kind by default.

The default permission scope covers resources installed by Providers
(managed resources), resources defined by XRDs (composite resources), and
some Kubernetes kinds Crossplane needs for its own operation, such as
`Deployment`.[^default-composed-resource-permission-scope] The documentation does not provide an exhaustive list of
those built-in kinds.

# Grant additional access

Before a Composition can manage another resource kind, create a Kubernetes
`ClusterRole` containing the required API groups, resources, and verbs. Add
this label so Kubernetes aggregates the new permissions into Crossplane's
primary `ClusterRole`:[^aggregated-clusterrole-procedure-and-required-label]

```yaml
metadata:
  labels:
    rbac.crossplane.io/aggregate-to-crossplane: "true"
```

The official example grants all verbs on the plural resource `clusters` in
the `postgresql.cnpg.io` API group so Crossplane can compose CloudNativePG
clusters.[^cloudnativepg-clusterrole-example] Treat that manifest as an example, not as a minimum-permissions
template: the selected documentation does not enumerate the least-privilege
verbs needed for every reconciliation case.

# Required-resource reads are a separate path

Function requirements such as function-go-templating `ExtraResources` do not
cause the Function pod to read Kubernetes directly. Crossplane Core receives
the requirement and performs an exact-name `Get` or a label-based `List` with
its Kubernetes client.[^core-required-resource-get-and-list-paths][^core-cache-backed-client-and-fetcher-wiring][^fetcher-wiring] Grant those reads to the Crossplane Core
Deployment service account selected by the Helm deployment template, not the
Function pod service account.[^core-deployment-service-account-selection]

The selector determines the required scope. In the selected release an empty
namespace on a label selector produces an all-namespace list, so a template-side
filter cannot reduce the earlier read permission.[^core-required-resource-get-and-list-paths] The deployed Core client
is cache-backed for unstructured resources; account for its informer access
when constructing the grant rather than treating `get` and `list` as a proven
complete minimum.[^core-cache-backed-client-and-fetcher-wiring][^fetcher-wiring]

This read path and the composed-resource apply path are performed by the same
Core process but require different verbs and should be reviewed separately.
Provider controller credentials and the Function runtime service account are
additional, distinct identities.[^composed-resource-apply-path][^function-runtime-invocation-and-separate-pod-identity][^function-deployment-service-account]

# RBAC manager

Crossplane installs and enables its RBAC manager by default.[^rbac-manager-default-and-disable-procedures] It
automatically grants the Crossplane service account access to managed and
composite resources and separately creates and binds roles for Provider
service accounts.[^rbac-manager-responsibilities]

If the RBAC manager is disabled, operators must manually grant the Crossplane
service account access to every kind it should compose, including managed and
composite resources.[^manual-grants-required-when-the-rbac-manager-is-disabled] The Helm value `rbacManager.deploy: false` disables it
at installation time; after installation, the documented procedure is to
delete the `crossplane-rbac-manager` Deployment.[^rbac-manager-default-and-disable-procedures]

# Relationships

A [Composition](composition.md) defines the desired composed resources. This
concept describes the controller-side authorization Crossplane needs to apply
them. Crossplane controller permissions and Provider controller permissions
are distinct, even though the default RBAC manager helps configure both.[^rbac-manager-responsibilities]
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

[^crossplane-creates-function-produced-composed-resources-with-its-service-account]: [Crossplane creates function-produced composed resources with its service account](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L277-L280)
[^default-composed-resource-permission-scope]: [Default composed-resource permission scope](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L282-L288)
[^aggregated-clusterrole-procedure-and-required-label]: [Aggregated ClusterRole procedure and required label](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L290-L321)
[^cloudnativepg-clusterrole-example]: [CloudNativePG ClusterRole example](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L299-L316)
[^rbac-manager-default-and-disable-procedures]: [RBAC manager default and disable procedures](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L206-L227)
[^rbac-manager-responsibilities]: [RBAC manager responsibilities](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/pods.md#L246-L260)
[^manual-grants-required-when-the-rbac-manager-is-disabled]: [Manual grants required when the RBAC manager is disabled](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L324-L333)
[^core-required-resource-get-and-list-paths]: [Core required-resource `Get` and `List` paths](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L154-L227)
[^core-cache-backed-client-and-fetcher-wiring]: [Core cache-backed client and fetcher wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L361-L423) and [fetcher wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
[^fetcher-wiring]: [fetcher wiring](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cmd/crossplane/core/core.go#L476-L481)
[^composed-resource-apply-path]: [Composed-resource apply path](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L615-L658)
[^function-runtime-invocation-and-separate-pod-identity]: [Function runtime invocation and separate pod identity](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/function_runner.go#L90-L166) and [Function Deployment service account](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_function.go#L120-L148)
[^function-deployment-service-account]: [Function Deployment service account](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/pkg/runtime/runtime_function.go#L120-L148)
[^core-deployment-service-account-selection]: [Core Deployment service-account selection](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/charts/crossplane/templates/deployment.yaml#L41-L56)
