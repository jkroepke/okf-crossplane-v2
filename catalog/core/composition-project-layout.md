---
type: Crossplane Development Guide
title: Reference layout for a Composition project
description: A small manifest layout that keeps Composition authoring inputs distinct from the CLI Functions-only render input.
tags: [crossplane, composition, authoring, cli, project-layout]
timestamp: 2026-07-16T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/apiextensions.crossplane.io_compositions.yaml
  - cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml
  - apis/apiextensions/v2/xrd_types.go
supporting_sources:
  - repository: crossplane/cli
    commit: ef9b974770a45e085aacee3b2cdda6284ab6cf51
    paths:
      - cmd/crossplane/render/load.go
      - cmd/crossplane/render/xr/cmd.go
      - cmd/crossplane/render/xr/help/render.md
  - repository: crossplane/docs
    commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
    paths:
      - content/v2.3/managed-resources/managed-resource-activation-policies.md
feature_state: Not stated by selected sources
---

# Reference layout

Use this deliberately small layout only when the Composition project contains
no files and the user has not provided other layout instructions:

```text
.
├── definition.yaml
├── composition.yaml
├── functions.yaml
├── provider.yaml
├── providerconfig.yaml
├── mrap.yaml
├── example.yaml
└── tests/
    └── observed-resources.yaml
```

This is a recommendation, not a required Crossplane repository layout. Add
further provider-specific resources, observed-resource fixtures, or xprin
suites as the project needs them.

# File responsibilities

| File | Put in it |
| --- | --- |
| `definition.yaml` | One current `apiextensions.crossplane.io/v2` CompositeResourceDefinition defining the XR group, names, scope, versions, and schema.[7] |
| `composition.yaml` | One current `apiextensions.crossplane.io/v1` `Composition`, in Pipeline mode. Set `compositeTypeRef.apiVersion` to `<xrd.spec.group>/<referenceable-version.name>` and `compositeTypeRef.kind` to `xrd.spec.names.kind`.[4][6] |
| `functions.yaml` | The mandatory Functions-only input for the standalone file-based render command shown below. Project-mode rendering may discover Functions through project metadata instead.[2][3] |
| `provider.yaml` | Provider package installation manifests needed by the Composition's managed resources. |
| `providerconfig.yaml` | The provider configuration manifests selected by those managed resources. |
| `mrap.yaml` | ManagedResourceActivationPolicy manifests when the selected provider setup uses explicit managed-resource activation.[5] |
| `example.yaml` | A representative XR used for local rendering and authoring checks. |
| `tests/observed-resources.yaml` | Optional render fixture for a later reconciliation stage. Keep it separate from desired manifests and pass it with `--observed-resources`.[8] |
| `tests/` | Optional assertion suites, for example xprin tests over initial and observed render stages. |

`provider.yaml`, `providerconfig.yaml`, and `mrap.yaml` are intentionally
outside `functions.yaml`: the CLI Functions loader rejects every non-Function
kind. A `pkg.crossplane.io/v1` `Provider` is still rejected; sharing the API
group with a Function does not make it a valid Functions input. Keep Provider
package installation manifests in `provider.yaml`. MRAP is conditional—include
it when the chosen provider and platform policy require managed-resource
activation, not merely because every project has this reference layout.

# Local authoring check

After creating the XR, Composition, and Function manifests, verify the
function pipeline renders:

```shell
crossplane composition render example.yaml composition.yaml functions.yaml
```

The CLI validates Pipeline mode and XR GVK compatibility before rendering.[1]

If a Function needs managed-resource status as input, add
`tests/observed-resources.yaml` and pass it with `--observed-resources`. Keep
that fixture separate from desired manifests so it is clear which data is a
test double.

For the current Composition API, see [Composition](/core/composition.md) and
[CompositeResourceDefinition v2](/core/composite-resource-definition.md).
For the CLI contract, see [render a Composition locally](/cli/local-composition-rendering.md).
Before choosing concrete managed-resource fields, use
[provider selection](/providers/provider-landscape.md) and
[provider CRD schema discovery](/providers/crd-schema-discovery.md). Review
[managed-resource activation](/core/minimal-managed-resource-activation.md),
[composed-resource RBAC](/core/composed-resource-rbac.md), and
[identity and replacement](/core/composed-resource-identity-and-replacement.md)
before a live apply. The
[Composition developer starter guide](/composition-developer-starter.md)
connects these decisions and the
[xprin test-suite model](/tools/xprin-test-suites.md).

# Citations

[1] [Pipeline Composition and XR GVK validation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L118-L158)

[2] [Functions-only loader validation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/load.go#L89-L113)

[3] [Standalone render requires the Functions input](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L396-L413)

[4] [Current Composition identity, type reference, and Pipeline mode](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L98)

[5] [MRAP activation-policy guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L166-L191)

[6] [XRD referenceable GVK derivation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v2/xrd_types.go#L287-L298)

[7] [Current XRD v2 identity and schema](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositeresourcedefinitions.yaml#L702-L1266)

[8] [CLI observed-resource fixtures](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L54-L74)
