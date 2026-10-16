---
type: Crossplane Development Guide
title: Generate runtime.Object methods on Go models
description: Opt in with the CLI v2.5.0 features.generateGoRuntimeObjects setting so control plane project Go models implement runtime.Object and register with a runtime.Scheme through AddToScheme.
resource: https://github.com/crossplane/cli
tags: [crossplane, cli, project, go, schemas, code-generation]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T21:45:00Z" }
sources:
  - id: config-features
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/config/config.go#L31-L82'
    title: 'CLI config file version and feature fields'
  - id: config-path
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/config/config.go#L84-L113'
    title: 'CLI config file path resolution'
  - id: config-set-keys
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/config/set.go#L44-L80'
    title: 'crossplane config set keys and validation'
  - id: config-docs
    resource: 'https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L537-L578'
    title: 'CLI v2.5 crossplane config reference'
  - id: command-maturity
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/main.go#L77-L88'
    title: 'CLI command group maturity labels'
  - id: generator-options
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/interface.go#L37-L75'
    title: 'Generator options reach only the Go generator'
  - id: project-schema-languages
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/apis/dev/v1alpha1/project_types.go#L132-L139'
    title: 'Project spec.schemas.languages'
  - id: runtime-objects-gate
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L40-L59'
    title: 'runtime.Object generation gate and by-value types'
  - id: root-struct-rule
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L174-L193'
    title: 'Root struct rule'
  - id: deepcopy-generation
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L231-L332'
    title: 'DeepCopy generation'
  - id: runtime-object-methods
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L334-L371'
    title: 'runtime.Object methods and scheme registration'
  - id: groupversion-info
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L670-L727'
    title: 'groupversion_info.go with AddToScheme'
  - id: generation-order
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L306-L317'
    title: 'runtime.Object before accessors'
  - id: models-go-mod
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L68-L105'
    title: 'Generated models go.mod'
  - id: v2-4-models-go-mod
    resource: 'https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/internal/schemas/generator/go.go#L67-L76'
    title: 'CLI v2.4.0 generated models go.mod'
  - id: runtime-objects-tests
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject_integration_test.go#L26-L153'
    title: 'runtime.Object generation integration tests'
  - id: runtime-objects-compilegate
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject_compilegate_test.go#L19-L230'
    title: 'compilegate behaviour tests'
  - id: v2-4-config-features
    resource: 'https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/internal/config/config.go#L41-L45'
    title: 'CLI v2.4.0 config features'
  - id: composition-generate-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/generate.go#L110-L111'
    title: 'composition generate passes the Go options'
  - id: project-build-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/project/build.go#L103-L104'
    title: 'project build passes the Go options'
  - id: runtime-objects-default-off-test
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject_integration_test.go#L71-L87'
    title: 'No runtime.Object methods by default test'
  - id: runtime-objects-loop
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L61-L101'
    title: 'DeepCopy for every struct, runtime.Object for root structs'
  - id: dependency-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/dependency/add.go#L93-L98'
    title: 'dependency add filters generators by project languages'
  - id: composition-render-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/xr/cmd.go#L401-L443'
    title: 'composition render parses the project file and passes unfiltered generators'
  - id: operation-render-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/op/cmd.go#L360-L367'
    title: 'operation render passes unfiltered generators'
  - id: composition-render-mount
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/composition.go#L27-L29'
    title: 'composition subcommands and maturity'
documentation_series: cli-v2.5
documentation_repository: crossplane/docs
documentation_commit: d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d
documentation_paths: [content/cli/v2.5/command-reference.md]
source_repository: crossplane/cli
source_tag: v2.5.0
source_commit: 1acb525095a4e43c9a765954efa66a47667a432b
source_paths: [internal/config/config.go, cmd/crossplane/config/set.go, cmd/crossplane/main.go, internal/schemas/generator/interface.go, internal/schemas/generator/runtimeobject.go, internal/schemas/generator/go.go, internal/schemas/generator/runtimeobject_integration_test.go, internal/schemas/generator/runtimeobject_compilegate_test.go, apis/dev/v1alpha1/project_types.go]
feature_state: Not stated by selected sources
feature_state_basis: Neither the config command, the config struct, nor the CLI v2.5 config reference carries a maturity label for this setting. Every consuming command generates models from a project file that uses the Alpha dev.crossplane.io/v1alpha1 Project metadata API, so an end-to-end workflow is at most Alpha; the consuming commands themselves are Beta, Alpha (operation render), or unlabelled (composition render).
---

# Overview

From CLI v2.5.0, the `features.generateGoRuntimeObjects` setting makes the Go
models that the CLI generates for a control plane project implement
`runtime.Object`, and adds a per-package `AddToScheme` helper so the types can
be registered with a `runtime.Scheme`.[^config-features][^config-docs] The
setting is off by default.[^config-features][^runtime-objects-default-off-test] CLI v2.4.0 had only the
`enableAlpha` and `disableBeta` features.[^v2-4-config-features]

# Enable it

```shell
crossplane config set features.generateGoRuntimeObjects true
```

`crossplane config set` accepts only known keys and parses the value as a
boolean.[^config-set-keys] The setting lives in the CLI config file,
`config.yaml`, found through `--config`, then `CROSSPLANE_CONFIG`, then
`$XDG_CONFIG_HOME/crossplane/config.yaml` or
`~/.config/crossplane/config.yaml`; the file must declare `version: 1`.[^config-path][^config-features][^config-docs]

```yaml
version: 1
features:
  generateGoRuntimeObjects: true
```

# Behavior

- Only the Go generator receives the option.[^generator-options]
  Schema-generating commands pass it, including `composition generate`,
  `project build`, `dependency add`, and, in project mode, `composition render`
  and `operation render`.[^composition-generate-wiring][^project-build-wiring][^dependency-wiring][^composition-render-wiring][^operation-render-wiring]
- Most of these commands filter generators by the project's
  `spec.schemas.languages`, so a non-empty `languages` list without `go` means
  they generate no Go models.[^dependency-wiring][^project-schema-languages] `composition render`
  and `operation render` pass all generators unfiltered, so they generate Go
  models even when `languages` omits `go`.[^composition-render-wiring][^operation-render-wiring]
- Every generated non-alias struct gets `DeepCopyInto` and `DeepCopy`.
  `Time`, `MicroTime`, `FieldsV1`, and `RawExtension` values are copied by
  value.[^runtime-objects-loop][^runtime-objects-gate][^deepcopy-generation]
- A root struct is one with `APIVersion`, `Kind`, and `Metadata` fields, which
  excludes object references.[^root-struct-rule][^runtime-objects-loop] Root structs also get
  `DeepCopyObject`, `GetObjectKind`, `GroupVersionKind`, and
  `SetGroupVersionKind`, plus an `init()` that registers the type with the
  package `SchemeBuilder`.[^runtime-object-methods]
- Each package that registers types gets a `groupversion_info.go` defining
  `GroupVersion`, `SchemeBuilder`, and `AddToScheme`.[^groupversion-info]
  Built-in Kubernetes packages use their real API group.[^runtime-objects-tests]
- runtime.Object methods are generated before any
  GetX and SetX accessors from `features.generateGoModelAccessors`, so an accessor
  whose name would duplicate one of these methods is not
  emitted.[^generation-order]
- With the setting off, no runtime.Object methods or `groupversion_info.go` are
  generated.[^runtime-objects-tests]

# Generated module

Independently of the setting, the generated models `go.mod` in CLI v2.5.0
declares `go 1.24.0` and requires `k8s.io/apimachinery v0.33.0`, pinned to the
Go function template.[^models-go-mod] In CLI v2.4.0 it declared `go 1.23` and
directly required only `github.com/oapi-codegen/runtime`.[^v2-4-models-go-mod]

# Limitations

- The setting itself has no maturity label. The consuming commands are Beta,
  Alpha (`operation render`), or unlabelled (`composition render`), and all of
  them read a project file that uses the Alpha `dev.crossplane.io/v1alpha1`
  Project metadata API.[^command-maturity][^composition-render-mount][^composition-render-wiring][^project-schema-languages][^config-docs]
- The behaviour tests that compile generated code and round-trip it through a
  scheme run only with the `compilegate` build tag.[^runtime-objects-compilegate]

# Relationships

- [Opt in to a control plane project](control-plane-projects.md) describes the
  project workflow that generates these models.

[^config-features]: [CLI config file version and feature fields](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/config/config.go#L31-L82)
[^config-path]: [CLI config file path resolution](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/config/config.go#L84-L113)
[^config-set-keys]: [crossplane config set keys and validation](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/config/set.go#L44-L80)
[^config-docs]: [CLI v2.5 crossplane config reference](https://github.com/crossplane/docs/blob/d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d/content/cli/v2.5/command-reference.md#L537-L578)
[^command-maturity]: [CLI command group maturity labels](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/main.go#L77-L88)
[^generator-options]: [Generator options reach only the Go generator](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/interface.go#L37-L75)
[^project-schema-languages]: [Project spec.schemas.languages](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/apis/dev/v1alpha1/project_types.go#L132-L139)
[^runtime-objects-gate]: [runtime.Object generation gate and by-value types](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L40-L59)
[^root-struct-rule]: [Root struct rule](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L174-L193)
[^deepcopy-generation]: [DeepCopy generation](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L231-L332)
[^runtime-object-methods]: [runtime.Object methods and scheme registration](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L334-L371)
[^groupversion-info]: [groupversion_info.go with AddToScheme](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L670-L727)
[^generation-order]: [runtime.Object before accessors](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L306-L317)
[^models-go-mod]: [Generated models go.mod](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L68-L105)
[^v2-4-models-go-mod]: [CLI v2.4.0 generated models go.mod](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/internal/schemas/generator/go.go#L67-L76)
[^runtime-objects-tests]: [runtime.Object generation integration tests](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject_integration_test.go#L26-L153)
[^runtime-objects-compilegate]: [compilegate behaviour tests](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject_compilegate_test.go#L19-L230)
[^v2-4-config-features]: [CLI v2.4.0 config features](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/internal/config/config.go#L41-L45)
[^composition-generate-wiring]: [composition generate passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/generate.go#L110-L111)
[^project-build-wiring]: [project build passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/project/build.go#L103-L104)
[^runtime-objects-default-off-test]: [No runtime.Object methods by default test](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject_integration_test.go#L71-L87)
[^runtime-objects-loop]: [DeepCopy for every struct, runtime.Object for root structs](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/runtimeobject.go#L61-L101)
[^dependency-wiring]: [dependency add filters generators by project languages](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/dependency/add.go#L93-L98)
[^composition-render-wiring]: [composition render parses the project file and passes unfiltered generators](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/xr/cmd.go#L401-L443)
[^operation-render-wiring]: [operation render passes unfiltered generators](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/op/cmd.go#L360-L367)
[^composition-render-mount]: [composition subcommands and maturity](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/composition.go#L27-L29)
