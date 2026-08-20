---
type: Crossplane Development Guide
title: Generate, test, build, and package a provider
description: Use provider-template's pinned build and generation toolchain to review API output, test controllers, build the runtime image, and produce an xpkg.
resource: https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/Makefile
tags: [crossplane, provider-development, sdk, testing, build, xpkg]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:09:30Z" }
sources:
  - id: build-submodule-gitlink
    resource: 'https://api.github.com/repos/crossplane/provider-template/git/trees/a74b386da0ec848036e16ff0a207c5a16bc9827f?recursive=1'
    title: Immutable provider-template tree containing the build gitlink
  - id: template-makefile
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/Makefile#L1-L67'
    title: Template Go, image, xpkg, and integration targets
  - id: generation-directives
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/generate.go#L20-L27'
    title: Provider API generation directives
  - id: reviewable-target
    resource: 'https://github.com/crossplane/build/blob/b964dbe0ff0856a762f1a06fe554c647d22af7f0/makelib/common.mk#L427-L446'
    title: Pinned build reviewable target
  - id: go-targets
    resource: 'https://github.com/crossplane/build/blob/b964dbe0ff0856a762f1a06fe554c647d22af7f0/makelib/golang.mk#L101-L169'
    title: Pinned Go generation, test, and build targets
  - id: xpkg-build
    resource: 'https://github.com/crossplane/build/blob/b964dbe0ff0856a762f1a06fe554c647d22af7f0/makelib/xpkg.mk#L67-L89'
    title: Pinned xpkg output and runtime image embedding
  - id: provider-package-metadata
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/package/crossplane.yaml#L1-L13'
    title: Template Provider package metadata
  - id: integration-install
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/cluster/local/integration_tests.sh#L139-L174'
    title: Template integration package installation and health wait
  - id: provider-package-installation
    resource: 'https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/v2.4/packages/providers.md#L33-L75'
    title: Crossplane v2.4 Provider package installation
  - id: digest-installation
    resource: 'https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/v2.4/packages/providers.md#L110-L136'
    title: Crossplane v2.4 registry and digest guidance
source_repository: crossplane/provider-template
source_commit: a74b386da0ec848036e16ff0a207c5a16bc9827f
supporting_source_repositories:
  - repository: crossplane/build
    commit: b964dbe0ff0856a762f1a06fe554c647d22af7f0
  - repository: crossplane/docs
    series: v2.4
    commit: f51137d2f8e92a167bb580be528c78b879ed406d
source_paths: [Makefile, apis/generate.go, package/crossplane.yaml, cluster/local/integration_tests.sh]
feature_state: Not stated by selected sources
feature_state_basis: Unlabelled build, test, generation, and packaging workflow; individual manifest API versions do not transfer maturity to the workflow.
---

# Pinned toolchain

The selected template commit pins its shared `crossplane/build` submodule at
`b964dbe0ff0856a762f1a06fe554c647d22af7f0`. The template Makefile delegates
normal Go, image, Kubernetes-tool, and xpkg behavior to that submodule.[^build-submodule-gitlink][^template-makefile]
Keep the submodule initialized and evaluate build behavior against that exact
revision rather than a moving build branch.

# Generation and review gate

Run:

```shell
make reviewable
```

At the selected build revision, `reviewable` is the aggregate generation,
lint, and test gate.[^reviewable-target] Its Go generation path runs
`go generate` and `go mod tidy`; the template's API directive regenerates
deepcopy methods, CRDs, and Crossplane method sets.[^go-targets][^generation-directives]
The unit-test target runs Go tests with coverage, and the build target compiles
the configured static package (`cmd/provider` in this template).[^go-targets][^template-makefile]

Review generated changes to `zz_generated*.go` and `package/crds/**` before
committing. An unexpected generated diff is evidence that an authored API or
tool version changed; do not hand-edit it away.

# Build outputs

The template configures one Provider runtime image and one xpkg. The selected
xpkg machinery produces `<name>-<version>.xpkg` and embeds the Provider runtime
image when the package metadata is a `Provider`.[^template-makefile][^xpkg-build]

The checked-in metadata declares:

- `kind: Provider` in `meta.pkg.crossplane.io/v1alpha1`;
- the source repository and Apache-2.0 license; and
- the `safe-start` package capability.[^provider-package-metadata]

That metadata API version does not label the entire Provider implementation or
build workflow Alpha. Their maturity is **Not stated by selected sources**.

# Local and integration checks

The Makefile offers `run`, `dev`, `dev-clean`, and an integration target.[^template-makefile]
The selected integration script installs the built xpkg as a Provider and
waits for a Healthy condition.[^integration-install] It discovers a Crossplane
chart version dynamically, so the script is not evidence of testing against a
single immutable Crossplane release. Pin the test environment separately when
release reproducibility matters.

The template's checked-in managed-resource unit test has no cases; complete
the controller test matrix described in the
[managed reconciler guide](managed-reconciler.md) before treating
`make reviewable` as meaningful behavior coverage.

# Installation boundary

Official v2.4 documentation installs the resulting package through a
`pkg.crossplane.io/v1` `Provider` object whose `spec.package` points to a
registry location.[^provider-package-installation] It also documents digest
references for deterministic and repeatable installation.[^digest-installation]

The same page explicitly places Provider build instructions outside its scope.
Use the pinned template and build sources for authoring behavior, and use the
v2.4 page for the operator-side package installation contract.

[^build-submodule-gitlink]: [Immutable provider-template tree containing the build gitlink](https://api.github.com/repos/crossplane/provider-template/git/trees/a74b386da0ec848036e16ff0a207c5a16bc9827f?recursive=1)
[^template-makefile]: [Template Go, image, xpkg, and integration targets](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/Makefile#L1-L67)
[^generation-directives]: [Provider API generation directives](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/apis/generate.go#L20-L27)
[^reviewable-target]: [Pinned build reviewable target](https://github.com/crossplane/build/blob/b964dbe0ff0856a762f1a06fe554c647d22af7f0/makelib/common.mk#L427-L446)
[^go-targets]: [Pinned Go generation, test, and build targets](https://github.com/crossplane/build/blob/b964dbe0ff0856a762f1a06fe554c647d22af7f0/makelib/golang.mk#L101-L169)
[^xpkg-build]: [Pinned xpkg output and runtime image embedding](https://github.com/crossplane/build/blob/b964dbe0ff0856a762f1a06fe554c647d22af7f0/makelib/xpkg.mk#L67-L89)
[^provider-package-metadata]: [Template Provider package metadata](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/package/crossplane.yaml#L1-L13)
[^integration-install]: [Template integration package installation and health wait](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/cluster/local/integration_tests.sh#L139-L174)
[^provider-package-installation]: [Crossplane v2.4 Provider package installation](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/v2.4/packages/providers.md#L33-L75)
[^digest-installation]: [Crossplane v2.4 registry and digest guidance](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/v2.4/packages/providers.md#L110-L136)
