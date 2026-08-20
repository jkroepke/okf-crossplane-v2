---
type: Crossplane Development Guide
title: Opt in to a Crossplane control plane project
description: Choose the Beta CLI project wrapper explicitly before scaffolding, locally running, and packaging a new Composition-backed API.
resource: https://docs.crossplane.io/cli/latest/get-started/get-started-with-control-plane-projects/
tags: [crossplane, cli, composition, project, authoring, packaging]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:35:21Z" }
sources:
  - id: project-command-beta-state
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/command-reference.md#L1095-L1103
    title: Crossplane project command Beta state
  - id: project-definition-and-layout
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L91-L145
    title: Control plane project definition and layout
  - id: project-init-contract
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/command-reference.md#L1184-L1238
    title: Project initialization contract
  - id: project-generation-workflow
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L162-L424
    title: API, Composition, dependency, and Function generation workflow
  - id: project-render-workflow
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L925-L1032
    title: Project-mode Composition rendering
  - id: project-run-workflow
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L1034-L1058
    title: Local project development control plane
  - id: project-runtime-prerequisites
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L80-L89
    title: Local project runtime prerequisites
  - id: project-build-and-push-workflow
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L1105-L1128
    title: Project build and push workflow
  - id: xrd-generation-boundary
    resource: https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L235-L238
    title: Example-XR XRD generation boundary
  - id: project-api-boundary
    resource: https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/apis/dev/v1alpha1/project_types.go#L69-L120
    title: Project metadata API boundary
documentation_series: cli-v2.4
source_repository: crossplane/docs
source_commit: f51137d2f8e92a167bb580be528c78b879ed406d
source_paths:
  - content/cli/v2.4/get-started/get-started-with-control-plane-projects.md
  - content/cli/v2.4/command-reference.md
supporting_sources:
  - repository: crossplane/cli
    commit: ef9b974770a45e085aacee3b2cdda6284ab6cf51
    paths:
      - apis/dev/v1alpha1/project_types.go
feature_state: Beta
feature_state_basis: The locked CLI v2.4 command reference explicitly labels the crossplane project command group Beta and warns that Beta features may change.
---

# Agent opt-in gate

Before creating files for a new Composition or Composition-backed API, ask the
requester one question unless they already selected a structure:

> Would you like this wrapped as a Crossplane control plane project (CLI Beta),
> or should I create standalone Composition manifests?

Project mode is opt-in. Do not initialize a project, add
`crossplane-project.yaml`, or reorganize existing manifests unless the
requester chooses the project route. This decision rule is a catalog authoring
policy, not a Crossplane requirement.

When the requester chooses standalone authoring, follow the
[standalone Composition manifest layout](/core/composition-project-layout.md)
and [standalone local rendering](/cli/local-composition-rendering.md).

# What the wrapper provides

The Crossplane CLI defines a project as a directory containing API definitions,
Compositions, embedded Functions, examples, tests, operations, and a
`crossplane-project.yaml` metadata file.[^project-definition-and-layout] The
`crossplane project` command group is explicitly **Beta**; the locked v2.4
documentation warns that Beta features may change.[^project-command-beta-state]

Choose this route when the requester wants the CLI to manage an end-to-end
authoring lifecycle:

- scaffold the standard project directories and metadata;
- generate an XRD and Composition;
- record dependencies and generate an embedded Function;
- discover and build embedded Functions during local rendering;
- run the packages on a local KIND development control plane; and
- build and push the resulting Configuration and embedded Function packages.

# Documented route

1. Initialize the selected directory with `crossplane project init <name>`.
   The name must be a DNS-1035 label; the command creates the project metadata
   and standard directories.[^project-init-contract]
2. Define the XR API, then use the CLI generation commands where they fit the
   requested authoring approach. The guide covers XRD generation from an
   example XR or SimpleSchema, Composition generation, dependency addition,
   and embedded Function generation.[^project-generation-workflow]
3. From the project directory, render the example XR and Composition. Project
   mode discovers and builds the embedded Functions, so this invocation does
   not take the standalone Functions manifest argument.[^project-render-workflow]
4. With a Docker-compatible runtime available, use `crossplane project run`
   for the local KIND control plane and registry. The command builds and pushes
   the embedded Function and Configuration packages, installs the
   Configuration, and selects the development cluster in the current kubectl
   context.[^project-run-workflow]
5. Use `crossplane project build` and `crossplane project push` when the
   requester wants to publish the packages for installation on an existing
   Crossplane cluster.[^project-build-and-push-workflow]

# Boundaries

- Project commands are Beta; do not hide that lifecycle state when offering
  the option.[^project-command-beta-state]
- `crossplane-project.yaml` uses the CLI's Project metadata type. It describes
  a buildable Configuration and its dependencies, Functions, paths,
  architectures, and schema generation; it is not a Kubernetes resource and
  has no status.[^project-api-boundary]
- Local project execution requires a Docker-compatible runtime because the
  guide builds Functions and creates a KIND cluster.[^project-runtime-prerequisites]
- Generating an XRD from an example XR cannot express field types, defaults,
  validation rules, or descriptions. Use the guide's SimpleSchema route or
  author the XRD schema directly when those controls are required.[^xrd-generation-boundary]
- Project wrapping does not replace the Composition design and verification
  gates. Continue through the
  [Composition developer route](/composition-developer-starter.md), including
  provider schema selection, security review, render assertions, live smoke
  tests, and package validation.

[^project-command-beta-state]: [Crossplane project command Beta state](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/command-reference.md#L1095-L1103)
[^project-definition-and-layout]: [Control plane project definition and layout](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L91-L145)
[^project-init-contract]: [Project initialization contract](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/command-reference.md#L1184-L1238)
[^project-generation-workflow]: [API, Composition, dependency, and Function generation workflow](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L162-L424)
[^project-render-workflow]: [Project-mode Composition rendering](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L925-L1032)
[^project-run-workflow]: [Local project development control plane](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L1034-L1058)
[^project-runtime-prerequisites]: [Local project runtime prerequisites](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L80-L89)
[^project-build-and-push-workflow]: [Project build and push workflow](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L1105-L1128)
[^xrd-generation-boundary]: [Example-XR XRD generation boundary](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/cli/v2.4/get-started/get-started-with-control-plane-projects.md#L235-L238)
[^project-api-boundary]: [Project metadata API boundary](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/apis/dev/v1alpha1/project_types.go#L69-L120)
