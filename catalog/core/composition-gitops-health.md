---
type: concept
title: Composition health assessment in GitOps tools
description: Crossplane Compositions expose no native health status, requiring careful GitOps health-assessment policy.
resource: https://github.com/crossplane/crossplane/issues/2672
tags: [crossplane, composition, gitops, kstatus, argocd, flux]
timestamp: 2026-07-14T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - apis/apiextensions/v1/composition_types.go
  - cluster/crds/apiextensions.crossplane.io_compositions.yaml
feature_state: Stable by repository default
project_history_researched_at: 2026-07-14
---

# Overview

Crossplane v2.3.3 `Composition` objects have `metadata` and `spec`, but no
`status`, status subresource, or conditions.[1][2] A GitOps health assessor
therefore cannot derive whether a Composition is ready, reconciling, or failed
from controller-reported Composition status.

This limitation is more precise than saying Compositions are categorically “not
kstatus compatible.” The kstatus implementation referenced in Crossplane issue
#2672 classifies an otherwise unknown resource with no recognized conditions as
`Current`.[3] It can therefore classify a Composition, but that result carries no
meaningful controller-derived health signal.

# Reported limitation

Open Crossplane issue #2672 reports Flux health-assessment problems for
Crossplane resources and proposes broader kstatus compatibility.[4] Its concrete
initial example is a `Provider`, not a `Composition`. A maintainer later noted
that Composition has no readiness concept or status conditions.[5]

The issue remained open on 2026-07-14. It is evidence of a reported integration
limitation, not proof that every Crossplane resource is incompatible with every
kstatus version. The selected v2.3.3 API independently corroborates only the
narrower Composition limitation: there is no native health status.

# Argo CD guidance

Crossplane's versioned v2.3 guide recommends instance-level Lua health
customizations for Crossplane and Upbound API groups.[6] The Crossplane-group
rule gives `Composition` special no-status treatment and reports it healthy
rather than waiting for conditions that do not exist.[7]

Argo CD 3.1 incorporates a bundled wildcard Lua health check for every kind whose
API group matches `*.crossplane.io`; PR #22919's merge commit is contained in
both v3.1.0 and the selected v3.1.16 release.[8] The released check includes a
healthy fixture for a status-less Composition.[9] It remains a Lua customization
embedded in Argo CD, rather than native Composition status or a kstatus
implementation.

The wildcard makes the check eligible for a broad API-group pattern, but its
logic recognizes a bounded set of conditions and special-case kinds. User-defined
Argo CD resource overrides take precedence over bundled scripts.[10] For
installations older than 3.1, the Crossplane guide's instance-level configuration
remains the documented approach; it also requires annotation-based resource
tracking and recommends Argo CD 2.4.8 or later.[11]

# Flux guidance

Flux's v2.9 documentation describes CEL expressions in
`.spec.healthCheckExprs` for custom-resource health assessment by a
`Kustomization` or `HelmRelease`.[12] Its Crossplane examples cover only:

- `pkg.crossplane.io/v1` `Provider`, using the `Healthy` condition.
- `iam.aws.crossplane.io/v1beta1` `Role`, using `Synced` and `Ready` conditions.[13]

The page provides no `Composition` or composite-resource example, no generic
Crossplane expression, and no minimum controller version. Because Composition
has no status or conditions, the published condition-based examples cannot be
transferred to it unchanged. A Flux policy for Composition would need to define
the desired no-status semantics and be validated against the deployed Flux
controller version.

# Limitations

- A Composition health result cannot represent the health of XRs or the resources they compose; those are separate objects with their own signals.
- Argo CD's Lua policy intentionally treats Composition's missing status as healthy. Bundling that policy in 3.1 does not add native readiness to the Crossplane API.
- Flux v2.9 CEL examples demonstrate customization for selected Crossplane resource kinds only. They do not establish a Composition workaround.
- No selected-release test directly runs kstatus against a v2.3.3 Composition.
- Claims, deprecated XRD v1, and legacy v1 XR semantics were excluded. No source code or configuration was copied or adapted.

# Citations

[1] [Crossplane v2.3.3 Composition Go type](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_types.go#L63-L82)
[2] [Released Composition schema termination and subresources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/apiextensions.crossplane.io_compositions.yaml#L259-L274)
[3] [Pinned kstatus fallback for unknown resources](https://github.com/kubernetes-sigs/cli-utils/blob/45a0b5b7e6b292c0a59c899aa50a3662a0c1cf7d/pkg/kstatus/status/status.go#L120-L137)
[4] [Open Crossplane issue #2672](https://github.com/crossplane/crossplane/issues/2672)
[5] [Maintainer comment on Composition readiness](https://github.com/crossplane/crossplane/issues/2672#issuecomment-988398492)
[6] [Crossplane v2.3 Argo CD wildcard health guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/crossplane-with-argo-cd.md#L38-L58)
[7] [Composition no-status handling in the documented Lua rule](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/crossplane-with-argo-cd.md#L121-L157)
[8] [Argo CD v3.1.16 bundled Crossplane health check](https://github.com/argoproj/argo-cd/blob/5d001b80990d14c0fc9b2cbee1eac25fc288da15/resource_customizations/_.crossplane.io/_/health.lua#L1-L67)
and [PR #22919 release containment](https://github.com/argoproj/argo-cd/compare/9149021b2cd1f7ed7d2ba711643b560127f81ad0...5d001b80990d14c0fc9b2cbee1eac25fc288da15)
[9] [Released Composition healthy fixture](https://github.com/argoproj/argo-cd/blob/5d001b80990d14c0fc9b2cbee1eac25fc288da15/resource_customizations/_.crossplane.io/_/health_test.yaml#L1-L9)
[10] [Argo CD wildcard and override selection behavior](https://github.com/argoproj/argo-cd/blob/5d001b80990d14c0fc9b2cbee1eac25fc288da15/util/lua/lua.go#L167-L205)
[11] [Argo CD version and annotation-based tracking guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/guides/crossplane-with-argo-cd.md#L7-L36)
[12] [Flux v2.9 CEL health-check mechanism](https://github.com/fluxcd/website/blob/32b8fe6417a23265c1d8eb2851ce8f0f7ef85317/content/en/flux/cheatsheets/cel-healthchecks.md#L8-L17)
[13] [Flux v2.9 Crossplane Provider and Role examples](https://github.com/fluxcd/website/blob/32b8fe6417a23265c1d8eb2851ce8f0f7ef85317/content/en/flux/cheatsheets/cel-healthchecks.md#L128-L140)
