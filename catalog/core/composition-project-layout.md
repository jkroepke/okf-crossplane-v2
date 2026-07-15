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
supporting_sources:
  - repository: crossplane/cli
    commit: ef9b974770a45e085aacee3b2cdda6284ab6cf51
    paths:
      - cmd/crossplane/render/load.go
      - cmd/crossplane/render/xr/cmd.go
---

# Reference layout

For an empty Composition project, use this deliberately small layout as an
authoring convention:

```text
.
├── composition.yaml
├── functions.yaml
├── provider.yaml
├── providerconfig.yaml
├── mrap.yaml
└── example.yaml
```

This is a recommendation, not a required Crossplane repository layout. Add
further provider-specific resources, observed-resource fixtures, or xprin
suites as the project needs them.

# File responsibilities

| File | Put in it |
| --- | --- |
| `composition.yaml` | One current `apiextensions.crossplane.io/v1` `Composition`, in Pipeline mode, whose `compositeTypeRef` identifies the XR API defined by the project's CompositeResourceDefinition (for example, `<crd-name>.<crd-api-group>`). |
| `functions.yaml` | The mandatory render input containing the Function objects referenced by the Composition pipeline. Keep it Functions-only. |
| `provider.yaml` | Provider package installation manifests needed by the Composition's managed resources. |
| `providerconfig.yaml` | The provider configuration manifests selected by those managed resources. |
| `mrap.yaml` | ManagedResourceActivationPolicy manifests when the selected provider setup uses explicit managed-resource activation. |
| `example.yaml` | A representative XR used for local rendering and authoring checks. |

`provider.yaml`, `providerconfig.yaml`, and `mrap.yaml` are intentionally
outside `functions.yaml`: the CLI Functions loader rejects objects that are
not `pkg.crossplane.io` Function resources. MRAP is conditional—include it
when the chosen provider and platform policy require managed-resource
activation, not merely because every project has this reference layout.

# Local authoring check

After creating the XR, Composition, and Function manifests, verify the
function pipeline renders:

```shell
crossplane composition render example.yaml composition.yaml functions.yaml
```

If a Function needs managed-resource status as input, add an observed-resource
fixture and pass it with `--observed-resources`. Keep that fixture separate
from the baseline layout so it is clear which data is a test double.

For the current Composition API, see [Composition](/core/composition.md) and
[CompositeResourceDefinition v2](/core/composite-resource-definition.md).
For the CLI contract, see [render a Composition locally](/cli/local-composition-rendering.md).

# Citations

[1] [Pipeline Composition and XR GVK validation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L118-L158)

[2] [Functions-only loader validation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/load.go#L89-L113)

[3] [Standalone render requires the Functions input](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L396-L413)

[4] [Current Composition identity, type reference, and Pipeline mode](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L7-L98)

[5] [MRAP activation-policy guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L166-L191)
