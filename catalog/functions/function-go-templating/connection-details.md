---
type: function
title: Compose connection details with function-go-templating
description: Aggregate observed connection details into a composed Kubernetes Secret.
resource: https://docs.crossplane.io/latest/guides/connection-details-composition/
tags: [crossplane, composition-function, connection-details, secret]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
documentation_repository: crossplane/docs
documentation_series: v2.3
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
crossplane_release: v2.3.3
feature_state: Beta
---

# Overview

Crossplane v2 does not use the legacy `CompositeConnectionDetails` pseudo-resource.
With `function-go-templating`, a Composition instead renders an ordinary Kubernetes
`Secret` as a named composed resource. The Secret aggregates connection details
observed from other composed resources.[1][2]

The `GoTemplate` input API is Beta because the selected function release serves `gotemplating.fn.crossplane.io/v1beta1`.[3]

# Flow

1. Each managed resource writes its provider connection details to its own Secret through `spec.writeConnectionSecretToRef`, or another composed Kubernetes resource exposes the required values.[1]
2. Assign every rendered source resource a stable `gotemplating.fn.crossplane.io/composition-resource-name` annotation. These names become keys under `$.observed.resources` on later reconciliations.[4]
3. Render a Kubernetes `Secret` and assign it its own stable composition resource name, such as `connection-secret`. The `setResourceNameAnnotation` helper emits the required annotation.[2][5]
4. Populate `Secret.data` from the named observed resources. Values in observed
   `connectionDetails` are already base64-encoded and can be copied directly;
   other values must be base64-encoded, for example with `b64enc`.[1][2]

The guide lets the XR consumer select the aggregate Secret name through `.spec.writeConnectionSecretToRef.name`. This is an example API convention, not automatic v2 connection-secret publication.[4]

# Reconciliation safety

Composed resources and their connection details are absent during initial
reconciliation. The template must still emit valid YAML before
`$.observed.resources` and its named entries exist. The guide emits an empty
`data: {}` until observed resources are available.[1][4]

Guard every resource and field that the template indexes when its presence is not guaranteed. The function README's minimal nil-map guard does not prove that a particular named resource or connection-detail key exists.[2]

# Boundaries

- The aggregate object is a normal composed Kubernetes `Secret`; it is not a legacy composite connection secret.[1][2]
- Connection-detail keys and availability are provider-specific. The guide's AWS `AccessKey` resources illustrate the pattern but are not required by it.[1][4]
- The guide pins function-go-templating v0.11.2, while this catalog uses the selected stable v0.12.2 release. The v0.12.2 schema and behavior corroborate the documented pattern.[3][6]
- A later readiness function may be useful, but it is separate from connection-detail aggregation.[4]

# Relationships

See [Request data and context](request-data.md) for the complete template request
and [Rendered output](rendered-output.md) for composed-resource identity and
readiness. [Template functions](template-functions.md) documents
`setResourceNameAnnotation` and the exposed Sprig helpers.

# Citations

[1] [Crossplane v2.3 connection-details guide](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/connection-details-composition.md#L227-L315)
[2] [function-go-templating v2 connection-details guidance](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L101-L122)
[3] [GoTemplate v1beta1 generated CRD](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L22)
[4] [Official function-go-templating Composition manifest](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/manifests/guides/connection-details-composition/composition-go-templating.yaml#L20-L66)
[5] [Resource-name annotation helper](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103)
[6] [Guide-selected function package](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/manifests/guides/connection-details-composition/fn-go-templating.yaml#L1-L6)
