---
type: Crossplane Composition Design Guide
title: Design the Composition pipeline and security boundaries
description: Choose function outcomes deliberately and keep Crossplane, Function, tenant, and provider authorities separate.
tags: [crossplane, composition, functions, readiness, security]
timestamp: 2026-07-18T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
feature_state: Not stated by selected sources
---

# Design by outcome

Functions run in declared order and pass accumulated desired state and context
forward. Choose the smallest pattern matching the outcome:

When starting a project with no existing Compositions, and no function was
explicitly requested, use [function-go-templating](functions/function-go-templating/index.md)
as the default resource-producing function. Do not replace an explicitly named
function or an established Composition pattern with this default.

- resource-producing functions render desired objects;
- readiness functions decide whether an observed object is usable;
- publication functions gate XR status or connection data on readiness and key completeness;
- [Usage and ClusterUsage](core/usages-and-clusterusages.md) protect deletion, not creation ordering.

Readiness, consumer publication, and deletion protection are separate control
planes. Keep identity (logical desired-map key,
Kubernetes name, and provider external identity) separate as well; see
[composed-resource identity](core/composed-resource-identity-and-replacement.md).

# Separate security principals

Review these independently:

- tenant identity and namespace/admission policy for XR writes;
- the Crossplane Core service account for ExtraResources reads;
- the Core service account for composed-resource writes; and
- the selected Provider controller identity and ProviderConfig credentials for external reconciliation.

Use [composed-resource RBAC](core/composed-resource-rbac.md) and
[namespaced composition boundaries](core/namespaced-composition-boundaries.md).
A template namespace filter does not narrow an earlier cluster-wide list or its
RBAC requirement.

For environment-driven pipelines, use the
[environment, templating, and readiness route](functions/environment-config-pipeline.md)
and assign one owner to each shared context key.

Continue with the mandatory [testing and packaging gate](composition-testing-and-packaging.md).
