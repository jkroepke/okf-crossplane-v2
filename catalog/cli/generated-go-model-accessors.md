---
type: Crossplane Development Guide
title: Generate GetX and SetX accessors on Go models
description: Opt in with the CLI v2.5.0 features.generateGoModelAccessors setting so control plane project Go models gain GetX and SetX methods for interfaces and generics.
resource: https://github.com/crossplane/cli
tags: [crossplane, cli, project, go, schemas, code-generation]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T21:30:00Z" }
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
  - id: accessors-generation
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors.go#L37-L201'
    title: 'Accessor generation rules'
  - id: accessors-default-off-test
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L101-L117'
    title: 'No accessors by default test'
  - id: accessors-method-set-test
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L314-L357'
    title: 'Accessor method set test'
  - id: accessors-nil-guard-test
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L395-L426'
    title: 'Accessor nil-receiver guard test'
  - id: accessors-chained-getter-test
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L220-L295'
    title: 'Generated models compile and chain getters'
  - id: accessors-after-runtime-objects
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L306-L317'
    title: 'Accessor generation order'
  - id: composition-generate-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/generate.go#L110-L111'
    title: 'composition generate passes the Go options'
  - id: project-build-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/project/build.go#L103-L104'
    title: 'project build passes the Go options'
  - id: project-run-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/project/run.go#L156-L157'
    title: 'project run passes the Go options'
  - id: function-generate-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/function/generate.go#L162-L163'
    title: 'function generate passes the Go options'
  - id: dependency-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/dependency/add.go#L93-L98'
    title: 'dependency add filters generators by project languages'
  - id: dependency-cache-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/dependency/cache.go#L88-L91'
    title: 'dependency update-cache passes the Go options'
  - id: composition-render-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/xr/cmd.go#L401-L443'
    title: 'composition render parses the project file and passes unfiltered generators'
  - id: operation-render-wiring
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/op/cmd.go#L360-L367'
    title: 'operation render passes unfiltered generators'
  - id: composition-render-mount
    resource: 'https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/composition.go#L27-L29'
    title: 'composition subcommands and maturity'
  - id: v2-4-config-features
    resource: 'https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/internal/config/config.go#L41-L45'
    title: 'CLI v2.4.0 config features'
documentation_series: cli-v2.5
documentation_repository: crossplane/docs
documentation_commit: d1c9eb7fd1548d0d61ab3901781919a5b4aaf69d
documentation_paths: [content/cli/v2.5/command-reference.md]
source_repository: crossplane/cli
source_tag: v2.5.0
source_commit: 1acb525095a4e43c9a765954efa66a47667a432b
source_paths: [internal/config/config.go, cmd/crossplane/config/set.go, cmd/crossplane/main.go, internal/schemas/generator/interface.go, internal/schemas/generator/accessors.go, internal/schemas/generator/accessors_test.go, internal/schemas/generator/go.go, apis/dev/v1alpha1/project_types.go]
feature_state: Not stated by selected sources
feature_state_basis: Neither the config command, the config struct, nor the CLI v2.5 config reference carries a maturity label for this setting. Every consuming command generates models from a project file that uses the Alpha dev.crossplane.io/v1alpha1 Project metadata API, so an end-to-end workflow is at most Alpha; the consuming commands themselves are Beta, Alpha (operation render), or unlabelled (composition render).
---

# Overview

From CLI v2.5.0, the `features.generateGoModelAccessors` setting adds `GetX`
and `SetX` methods to the Go models that the CLI generates for a control plane
project, so code can reach generated resources through interfaces and
generics.[^config-features][^config-docs] The setting is off by default.
CLI v2.4.0 had only the `enableAlpha` and `disableBeta`
features.[^v2-4-config-features]

# Enable it

```shell
crossplane config set features.generateGoModelAccessors true
```

`crossplane config set` accepts only known keys and parses the value as a
boolean.[^config-set-keys] The setting lives in the CLI config
file, `config.yaml`, which the CLI finds through the `--config` flag, then
`CROSSPLANE_CONFIG`, then `$XDG_CONFIG_HOME/crossplane/config.yaml` or
`~/.config/crossplane/config.yaml`.[^config-path][^config-docs] The file must
declare `version: 1`; a missing file means every feature is off.[^config-features]

```yaml
version: 1
features:
  generateGoModelAccessors: true
```

# Behavior

- Only the Go generator receives the option. JSON, KCL, and Python schemas are
  unchanged.[^generator-options]
- Commands that generate project schemas pass the option: `composition
  generate`, `project build`, `project run`, `function generate`, `dependency
  add`, `dependency update-cache`, and, in project mode, `composition render`
  and `operation render`.[^composition-generate-wiring][^project-build-wiring][^project-run-wiring][^function-generate-wiring][^dependency-wiring][^dependency-cache-wiring][^composition-render-wiring][^operation-render-wiring]
- Most of these commands filter generators by the project's
  `spec.schemas.languages`, so a non-empty `languages` list without `go` means
  they generate no Go models.[^dependency-wiring][^project-schema-languages] `composition render`
  and `operation render` pass all generators unfiltered, so they generate Go
  models, with accessors when the setting is on, even when `languages` omits
  `go`.[^composition-render-wiring][^operation-render-wiring]
- Each exported, named field of each generated struct gets a pointer-receiver
  `GetX()` that returns the field's own type and a `SetX(v)` that takes
  it.[^accessors-generation][^accessors-method-set-test]
- Getters return the zero value on a nil receiver, so chained getters are safe
  on partly filled objects; setters have no nil
  guard.[^accessors-nil-guard-test][^accessors-chained-getter-test]
- Type aliases, embedded fields, unexported fields, and names that already exist
  as methods are skipped.[^accessors-generation]
- Accessors are added last, after any `runtime.Object` methods, so an accessor
  whose name would duplicate such a method is not emitted. The cited site is
  one of several generation paths that use the same
  order.[^accessors-after-runtime-objects]
- With the setting off, no accessors are generated.[^accessors-default-off-test]

# Limitations

- The setting itself has no maturity label. The consuming commands are Beta,
  Alpha (`operation render`), or unlabelled (`composition render`), and all of
  them read a project file that uses the Alpha `dev.crossplane.io/v1alpha1`
  Project metadata API.[^command-maturity][^composition-render-mount][^composition-render-wiring][^config-docs]
- Only `crossplane config set` is shown rejecting unknown keys. The selected
  sources do not establish that a misspelled key in `config.yaml` is
  rejected.[^config-set-keys][^config-features]

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
[^accessors-generation]: [Accessor generation rules](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors.go#L37-L201)
[^accessors-default-off-test]: [No accessors by default test](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L101-L117)
[^accessors-method-set-test]: [Accessor method set test](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L314-L357)
[^accessors-nil-guard-test]: [Accessor nil-receiver guard test](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L395-L426)
[^accessors-chained-getter-test]: [Generated models compile and chain getters](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/accessors_test.go#L220-L295)
[^accessors-after-runtime-objects]: [Accessor generation order](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/internal/schemas/generator/go.go#L306-L317)
[^composition-generate-wiring]: [composition generate passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/generate.go#L110-L111)
[^project-build-wiring]: [project build passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/project/build.go#L103-L104)
[^project-run-wiring]: [project run passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/project/run.go#L156-L157)
[^function-generate-wiring]: [function generate passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/function/generate.go#L162-L163)
[^dependency-wiring]: [dependency add filters generators by project languages](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/dependency/add.go#L93-L98)
[^dependency-cache-wiring]: [dependency update-cache passes the Go options](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/dependency/cache.go#L88-L91)
[^composition-render-wiring]: [composition render parses the project file and passes unfiltered generators](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/xr/cmd.go#L401-L443)
[^operation-render-wiring]: [operation render passes unfiltered generators](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/render/op/cmd.go#L360-L367)
[^composition-render-mount]: [composition subcommands and maturity](https://github.com/crossplane/cli/blob/1acb525095a4e43c9a765954efa66a47667a432b/cmd/crossplane/composition/composition.go#L27-L29)
[^v2-4-config-features]: [CLI v2.4.0 config features](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/internal/config/config.go#L41-L45)
