---
type: Crossplane Development Guide
title: Crossplane v2 Composition developer route
description: A routing guide for designing, implementing, testing, and packaging a Crossplane v2 Composition.
resource: https://docs.crossplane.io/v2.3/composition/compositions/
tags: [crossplane, composition, composition-authoring, development]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:35:21Z" }
crossplane_release: v2.3.3
documentation_series: v2.3
feature_state: Not stated by selected sources
---

# Ask about the project wrapper first

When a user requests a new Composition or a new Composition-backed API and has
not already chosen a repository structure, ask:

> Would you like this wrapped as a Crossplane control plane project (CLI Beta),
> or should I create standalone Composition manifests?

Treat the project wrapper as an explicit opt-in. Do not scaffold or migrate to
project mode unless the user chooses it. When the user opts in, follow the
[control plane project workflow](cli/control-plane-projects.md). When the user
chooses standalone manifests, use the
[standalone manifest layout](core/composition-project-layout.md).

This question is a catalog authoring policy, not a Crossplane requirement.

# Use this as a route, not a checklist to stop reading

Each stage is an independently consumable concept. An implementation is not
complete until the testing and live-verification stage is complete; do not
skip it because the API or pipeline documents are sufficient to render YAML.

1. [Design the XR API and select provider contracts](composition-api-and-provider-contracts.md)
2. [Design the function pipeline and security boundaries](composition-pipeline-and-security.md)
3. [Render, test, smoke-test, and package](composition-testing-and-packaging.md)

Provider-specific GVKs, fields, credentials, connection keys, and external
behavior must come from the provider release installed in the target
environment. This route supplies no universal runnable manifest.

## Default cloud-provider choice

For a new Composition that needs AWS, Azure, or GCP resources, prefer the
corresponding Upjet provider:

| Cloud | Prefer for new work | Avoid introducing for new work |
| --- | --- | --- |
| AWS | `crossplane-contrib/provider-upjet-aws` | `crossplane-contrib/provider-aws` |
| Azure | `crossplane-contrib/provider-upjet-azure` | `crossplane-contrib/provider-azure` |
| GCP | `crossplane-contrib/provider-upjet-gcp` | `crossplane-contrib/provider-gcp` |

This is an authoring default, not an in-place replacement rule. If a
Composition or its target cluster already uses one of the non-Upjet providers,
continue using that provider unless an explicit, resource-by-resource migration
has been planned and tested. Provider packages can expose different GVKs,
scopes, ProviderConfigs, external identities, and migration behavior. Consult
[provider implementation families and selection](providers/provider-landscape.md)
before selecting a package, then inspect the exact pinned provider CRD schema.

## Default function choice

If the project has no existing Compositions and the requester did not name a
function to implement the Composition, start with
[function-go-templating](functions/function-go-templating/index.md). Treat this
as a practical default for a new implementation, not a requirement: an
explicit function choice or an existing project pattern takes precedence.

## Completion gate

Before declaring the Composition implemented, record evidence for all of the
following in the project (fixtures, commands, or CI output):

- rendered initial and observed-resource stages;
- assertions for desired resources, references, status, and connection data;
- Kubernetes admission and provider-backed reconciliation smoke tests; and
- package build and installation/revision activation validation.

The [testing and packaging concept](composition-testing-and-packaging.md) is
the authoritative gate and should be linked from implementation tasks.
