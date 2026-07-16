---
type: Crossplane Development Guide
title: XRD scale subresource and display columns
description: Expose XR scaling and useful kubectl output through version-scoped XRD fields.
resource: https://github.com/crossplane/crossplane
tags: [crossplane, core, xrd, crd, scale, kubectl]
timestamp: 2026-07-15T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
feature_state: Stable by repository default
feature_state_basis: The guidance inherits the selected stable XRD and Kubernetes CRD API surfaces; the authoring procedure has no independent maturity.
---

# Scale subresource

Configure `subresources.scale` on each XRD version to generate an XR `/scale`
endpoint. `specReplicasPath` and `statusReplicasPath` are required; the optional
`labelSelectorPath` addresses a string field in `spec` or `status`. The paths
must not use array notation.[1]

The selected Crossplane v2.3 guide requires each replica path to exist in the
XRD schema. Crossplane propagates the configuration to the generated CRD, but
the Composition author still must copy desired replicas to composed resources
and publish observed replicas (and a selector, when used) back to XR status.
That enables `kubectl scale`, HPA, and KEDA to use the XR.[2]

# Additional printer columns

`additionalPrinterColumns` is also version-scoped. Each column has a `name`,
`type`, and JSONPath; description, format, and priority are optional. Use these
for concise, server-side `kubectl get` output, such as desired and current
replicas or readiness signals.[3]

# Citations

[1] [XRD scale-subresource schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1216-L1256)
[2] [Crossplane v2.3 scalable composition guide](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/scalable-composition.md#L83-L136)
[3] [XRD additional-printer-column schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L1125-L1170)
