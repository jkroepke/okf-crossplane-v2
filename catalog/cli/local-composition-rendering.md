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
  - cmd/crossplane/validate/cmd.go
  - cmd/crossplane/validate/help/validate.md
  - pkg/validate/validate.go
supporting_sources:
  - repository: CustomResourceDefinition/catalog
    commit: 0584c9f7e6eaef8367cd65e59266d8ad49764f0c
    paths:
      - README.md
project_history_repository: crossplane/cli
project_history_items: [pull/148, issues/195]
project_history_researched_at: 2026-07-16T00:00:00Z
feature_state: Not stated by selected sources
---

# Overview

`crossplane composition render` simulates an XR render locally. Supply an
example XR, a `spec.mode: Pipeline` Composition, and a Functions input; the
CLI checks that the Composition's `compositeTypeRef` matches the XR GVK. It
prints the rendered XR and the resources a Function pipeline would create or
mutate. By default, the XR output is limited to `metadata.name` and `status`;
use `--include-full-xr` when the desired spec and metadata are also useful.[1][2][3]

```shell
crossplane composition render example.yaml composition.yaml functions.yaml
```

This is local simulation, not a substitute for applying the manifests to a
cluster or for provider reconciliation.

# Runtime requirements

The default render engine and Function runtime use Docker. Have a working
local Docker installation and daemon before running the command. Development
runtime Functions or `--crossplane-binary` are documented alternatives for
their respective runtime paths.[1]

# Inputs

| Input | Purpose | Boundary |
| --- | --- | --- |
| `example.yaml` | An XR instance whose GVK selects the Composition. | Use a representative author-facing XR. |
| `composition.yaml` | The Pipeline-mode Composition to run. | Its `compositeTypeRef` must match the XR GVK. |
| `functions.yaml` | Function manifests that satisfy pipeline `functionRef` entries. | This input accepts only `pkg.crossplane.io` Function objects. Keep every other manifest out of it. |

Outside a Crossplane Project, the Functions input is required. It may be a
multi-document YAML file or a directory of YAML files. A Functions file is a
CLI input boundary: do not put a Provider, ProviderConfig,
ManagedResourceActivationPolicy, Composition, or XR in it.[4][13]

## Strict Functions-only rule

`functions.yaml` is **not** a general package manifest file. It must contain
only `Function` objects. In particular, this otherwise familiar package object
is incompatible with `crossplane composition render` when placed in
`functions.yaml`:

```text
apiVersion: pkg.crossplane.io/v1
kind: Provider
```

The loader rejects it because its kind is `Provider`, even though it uses the
same `pkg.crossplane.io` API group as a Function. Put Provider package
installation manifests in `provider.yaml`; leave `functions.yaml` for the
Function objects named by pipeline `functionRef` entries. A non-Function
object in the Functions input makes the render command fail.

# Mock observed resources

Use `--observed-resources` (or `-o`) to provide mock composed resources to the
Function pipeline as observed cluster resources. The value may be one YAML
file or a directory and its resource definition is intentionally not validated. That makes
it suitable for supplying representative managed-resource `status` data when
a Function's behavior depends on observed status.[5]

```shell
crossplane composition render \
  example.yaml composition.yaml functions.yaml \
  --observed-resources observed-resources.yaml
```

See [the composition project layout](/core/composition-project-layout.md) for
a starting file arrangement, and [xprin test suites](/tools/xprin-test-suites.md)
when assertions should turn renders into repeatable tests.

# Full render-and-validate round trip

For a stronger local check, render the full XR and then validate every emitted
document against the XRD and Provider definition extensions. Use one spelling of
the full-XR flag; `-x` is the short form of `--include-full-xr`.

```shell
crossplane composition render --include-full-xr \
  example.yaml composition.yaml functions.yaml | \
  crossplane resource validate --error-on-missing-schemas \
    --crossplane-image=xpkg.crossplane.io/crossplane/crossplane:stable \
    definition.yaml,provider.yaml -
```

`--include-full-xr` writes the XR together with rendered composed resources to
standard output. `resource validate` treats `definition.yaml,provider.yaml` as
definition extensions and `-` as the rendered-resource stream. The
`--error-on-missing-schemas` flag makes a missing definition fail the command, so a
successful round trip has no missing-definition diagnostics and zero validation
failures.[6][7][8]

## Definition-coverage triage

`crossplane resource validate` builds its offline validators from XRDs and
CRDs supplied as extensions or unpacked from Crossplane packages. It does not
load Kubernetes built-in resource definitions. A rendered core `v1` resource such
as a `Secret` therefore reports a missing CRD/XRD by design; it is a coverage
gap, not evidence that the built-in resource needs a CRD.[10]

For a non-Crossplane custom GVK that is missing from the XRD/provider definition
set, look up the normalized Group, Kind, and version in the community
`CustomResourceDefinition/catalog` `main` branch. A hit establishes only that
a community CRD definition exists; supply that
definition as an extension, then verify that it matches the exact installed
operator CRD. The `main` branch is mutable and discovery-only: resolve and
record its commit before using a selected definition in reproducible
validation. A miss does not prove that the CRD does not exist.[11]

Use the catalog's current `main` definition path. The resource kind is
lowercase in the catalog path:

```text
https://raw.githubusercontent.com/CustomResourceDefinition/catalog/main/definitions/{{group}}/{{resourcekind-lowercase}}.yaml
```

For example, an Argo CD Application definition is:

```text
https://raw.githubusercontent.com/CustomResourceDefinition/catalog/main/definitions/argoproj.io/application.yaml
```

Do not use this CRD-definition lookup for built-in Kubernetes resources such
as `v1/Secret`; they have no CRD in the catalog.[11]

Do not treat the catalog as a `resource validate` input integration: its
definition documents must be passed to the CLI as extensions. Keep built-in
Kubernetes resources in the render output, but validate them with
Kubernetes-aware tooling or cluster admission/dry-run separately. Use
`--error-on-missing-schemas` only when every rendered GVK is expected to have
an XRD/CRD definition, or expect it to fail for built-ins.[10]

Issue #195 is an open v2.4.0 report by human author `@jkroepke` of the
`v1/Secret` message; it does not establish a released fix or a supported
workaround.[12]

## Image-version boundary

In CLI v2.4.0, omitting `--crossplane-image` selects a Crossplane image whose
tag equals the CLI binary version. Supply the override when that matching Core
image is unavailable—for example, when the CLI release precedes the matching
Core release. The `:stable` value is useful for checking against the current
stable Core image, but it is mutable; pin a Core image tag or digest in CI for
reproducible validation.[8]

CLI PR #148 changes the default image to `:stable`, but it merged after v2.4.0
and was not contained in a stable release as of 2026-07-16. It therefore does
not change the documented v2.4.0 behavior.[9]

# Citations

[1] [CLI render behavior, output, and Docker guidance](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L1-L35)

[2] [Documented new-XR render invocation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L86-L99)

[3] [Pipeline-mode guard and XR GVK compatibility check](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L118-L158)

[4] [Functions-only loader validation](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/load.go#L89-L113)

[5] [Observed-resource input and status-mocking guidance](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L54-L74)

[6] [Full render-to-validation pipeline](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/validate/help/validate.md#L61-L71)

[7] [Full-XR output behavior](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L327-L375)

[8] [Validation inputs, missing-definition failure, and image selection](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/validate/cmd.go#L74-L156)

[9] [PR #148: change validation image default to `:stable`](https://github.com/crossplane/cli/pull/148), merged 2026-06-25; release containment checked 2026-07-16.

[10] [CLI extension-only definition inputs](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/validate/help/validate.md#L1-L27), [CRD validator construction](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/pkg/validate/validate.go#L48-L92), and [missing-definition exit behavior](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/pkg/validate/validate.go#L130-L140)

[11] [CRD Catalog definition files and definition examples](https://github.com/CustomResourceDefinition/catalog/blob/0584c9f7e6eaef8367cd65e59266d8ad49764f0c/README.md#L20-L38)

[12] [CLI issue #195: built-in Secret missing-definition report](https://github.com/crossplane/cli/issues/195), opened by human author `@jkroepke` on 2026-07-16; researched 2026-07-16.

[13] [Standalone file-based render requires the Functions argument](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/cmd.go#L396-L413)
