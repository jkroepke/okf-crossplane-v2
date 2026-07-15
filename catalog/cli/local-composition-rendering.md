---
type: Crossplane CLI Command
title: Render a Composition locally
description: Use the Crossplane CLI to execute a Pipeline Composition and its Functions locally against an example XR.
resource: https://github.com/crossplane/cli
tags: [crossplane, cli, composition, rendering, testing]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane/cli
source_commit: ef9b974770a45e085aacee3b2cdda6284ab6cf51
source_paths:
  - cmd/crossplane/render/xr/cmd.go
  - cmd/crossplane/render/xr/help/render.md
  - cmd/crossplane/render/load.go
---

# Overview

`crossplane composition render` simulates an XR render locally. Supply an
example XR, a `spec.mode: Pipeline` Composition, and a Functions input; the
CLI checks that the Composition's `compositeTypeRef` matches the XR GVK. It
prints the rendered XR and the resources a Function pipeline would create or
mutate. By default, the XR output is limited to `metadata.name` and `status`;
use `--include-full-xr` when the desired spec and metadata are also useful.

```shell
crossplane composition render example.yaml composition.yaml functions.yaml
```

This is local simulation, not a substitute for applying the manifests to a
cluster or for provider reconciliation.

# Runtime requirements

The default render engine and Function runtime use Docker. Have a working
local Docker installation and daemon before running the command. Development
runtime Functions or `--crossplane-binary` are documented alternatives for
their respective runtime paths.

# Inputs

| Input | Purpose | Boundary |
| --- | --- | --- |
| `example.yaml` | An XR instance whose GVK selects the Composition. | Use a representative author-facing XR. |
| `composition.yaml` | The Pipeline-mode Composition to run. | Its `compositeTypeRef` must match the XR GVK. |
| `functions.yaml` | Function manifests that satisfy pipeline `functionRef` entries. | This input accepts only `pkg.crossplane.io` Function objects. Keep every other manifest out of it. |

Outside a Crossplane Project, the Functions input is required. It may be a
multi-document YAML file or a directory of YAML files. A Functions file is a
CLI input boundary: do not put a Provider, ProviderConfig,
ManagedResourceActivationPolicy, Composition, or XR in it.

# Mock observed resources

Use `--observed-resources` (or `-o`) to provide mock composed resources to the
Function pipeline as observed cluster resources. The value may be one YAML
file or a directory and its schema is intentionally not validated. That makes
it suitable for supplying representative managed-resource `status` data when
a Function's behavior depends on observed status.

```shell
crossplane composition render \
  example.yaml composition.yaml functions.yaml \
  --observed-resources observed-resources.yaml
```

See [the composition project layout](/core/composition-project-layout.md) for
a starting file arrangement, and [xprin test suites](/tools/xprin-test-suites.md)
when assertions should turn renders into repeatable tests.

# Citations

[1] [CLI render behavior, output, and Docker guidance](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L1-L35)

[2] [Documented new-XR render invocation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L86-L99)

[3] [Pipeline-mode guard and XR GVK compatibility check](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L118-L158)

[4] [Functions-only loader validation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/load.go#L89-L113)

[5] [Observed-resource input and status-mocking guidance](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L54-L74)
