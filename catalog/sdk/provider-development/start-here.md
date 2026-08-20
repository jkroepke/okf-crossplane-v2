---
type: Crossplane Development Guide
title: Start a provider project with provider-template
description: Use the pinned provider-template snapshot as the entry point for a hand-written Crossplane provider while preserving its version and example boundaries.
resource: https://github.com/crossplane/provider-template
tags: [crossplane, provider-development, sdk, go, provider-template]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:09:30Z" }
sources:
  - id: provider-responsibilities
    resource: 'https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/v2.4/packages/providers.md#L7-L29'
    title: Crossplane v2.4 provider responsibilities
  - id: template-purpose
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/README.md#L1-L10'
    title: provider-template purpose and included sample surfaces
  - id: template-workflow
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/README.md#L12-L32'
    title: provider-template development workflow
  - id: selected-dependencies
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/go.mod#L1-L19'
    title: provider-template Go and Crossplane dependencies
  - id: older-provider-guide-version-boundary
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/guide-provider-development.md#L60-L74'
    title: Older provider guide runtime target and provider-template recommendation
source_repository: crossplane/provider-template
source_commit: a74b386da0ec848036e16ff0a207c5a16bc9827f
source_revision: immutable main snapshot
source_paths: [README.md, go.mod]
crossplane_documentation_series: v2.4
feature_state: Not stated by selected sources
feature_state_basis: Unlabelled provider-development workflow and template snapshot; source stability does not establish product maturity.
---

# Overview

A Provider defines Kubernetes managed-resource APIs and implements the
authentication, external API calls, and controller logic that reconcile those
resources.[^provider-responsibilities] For a hand-written Go Provider,
`crossplane/provider-template` supplies a minimal project containing provider
configuration APIs, a sample managed resource, and a controller skeleton.[^template-purpose]

First decide whether a hand-written Provider is the right implementation
family. If a suitable Terraform provider exists, compare this route with the
[Upjet-generated and other provider families](/providers/provider-landscape.md)
before committing to custom controllers.

# Selected source boundary

This guide uses provider-template commit
`a74b386da0ec848036e16ff0a207c5a16bc9827f`. This workflow pins that exact
`main` snapshot instead of assigning it a semantic-version release identity.

The snapshot declares Go 1.25.11 and selects Crossplane APIs and
`crossplane-runtime/v2` v2.3.3.[^selected-dependencies] Current provider
orientation is taken from the Crossplane v2.4 documentation, but SDK behavior
in this section stays version-matched to the template's v2.3.3 dependency.

# Bootstrap sequence

After creating a repository from the template, its documented sequence is:

```shell
make submodules
make provider.prepare provider=<CamelCaseName>
make provider.addtype provider=<CamelCaseName> group=<lowercase-group> kind=<Kind>
```

Then replace the sample API group, managed-resource controller, and
ProviderConfig implementation; register the new API and controller; run
`make reviewable`; and run `make build`.[^template-workflow]

Treat every generated sample as a replacement checklist, not production
behavior. Continue with the [managed-resource API contract](managed-resource-apis.md),
[provider configuration](provider-configuration.md), and
[managed reconciler](managed-reconciler.md) before relying on the build and
package outputs.

# Documentation boundary

The older contributing provider-development guide still recommends
provider-template, but the same section says it targets crossplane-runtime
v0.9.0.[^older-provider-guide-version-boundary] It also contains older
cluster-scoped assumptions. This knowledge therefore uses the current pinned
template and its exact runtime dependency for API and behavior claims; the
older guide is not treated as the current SDK specification.

Neither the template snapshot nor the selected documentation assigns a
lifecycle state to the provider-development workflow. Its feature state is
**Not stated by selected sources**.

[^provider-responsibilities]: [Crossplane v2.4 provider responsibilities](https://github.com/crossplane/docs/blob/f51137d2f8e92a167bb580be528c78b879ed406d/content/v2.4/packages/providers.md#L7-L29)
[^template-purpose]: [provider-template purpose and included sample surfaces](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/README.md#L1-L10)
[^template-workflow]: [provider-template development workflow](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/README.md#L12-L32)
[^selected-dependencies]: [provider-template Go and Crossplane dependencies](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/go.mod#L1-L19)
[^older-provider-guide-version-boundary]: [Older provider guide runtime target and provider-template recommendation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/guide-provider-development.md#L60-L74)
