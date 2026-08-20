---
type: Crossplane Core Concept
title: Minimal managed-resource activation
description: A preventive platform policy for using Alpha MRAPs to activate only required modern namespaced managed-resource APIs.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resource-activation-policies/
tags: [crossplane, managed-resources, mrap, providers, security]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: helm-default-activation-and-disabling-it
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L166-L191'
    title: 'Helm default activation and disabling it'
  - id: exact-names-wildcard-syntax-and-wildcard-best-practices
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L72-L91'
    title: 'Exact names, wildcard syntax, and wildcard best practices'
  - id: best-practices
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L452-L466'
    title: 'best practices'
  - id: modern-and-legacy-managed-resource-styles
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L122-L151'
    title: 'Modern and legacy managed-resource styles'
  - id: configuration-package-mrap-dependency-guidance
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L276-L292'
    title: 'Configuration package MRAP dependency guidance'
  - id: dependency-recommendation
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L459-L463'
    title: 'dependency recommendation'
  - id: additive-overlap-and-non-deactivation-e2e-behavior
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_activation_policy_test.go#L191-L256'
    title: 'Additive overlap and non-deactivation E2E behavior'
  - id: activation-only-reconciliation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L106-L147'
    title: 'Activation-only reconciliation'
  - id: irreversible-mrd-state
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_types.go#L25-L54'
    title: 'irreversible MRD state'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths: [apis/apiextensions/v1alpha1/mrd_policy_types.go, internal/controller/apiextensions/activationpolicy/reconciler.go, test/e2e/apiextensions_activation_policy_test.go]
feature_state: Alpha
---

# Overview

`ManagedResourceActivationPolicy` (MRAP) lets a platform activate a subset of
provider ManagedResourceDefinitions (MRDs). The v2.3 Helm default instead
activates all MRDs via `activate: ["*"]`; setting
`provider.defaultActivations={}` omits that default.[^helm-default-activation-and-disabling-it]

This document proposes a stricter **platform policy**, not a Crossplane
requirement: disable the default wildcard before any MRDs are activated, then
declare only the exact plural MRD names required by a configuration or its
Compositions. This minimizes the API surface from the outset.

# Recommended policy boundary

1. Use exact plural MRD object names, such as
   `buckets.s3.aws.m.crossplane.io`, as the default. The docs recommend exact
   names first; wildcard entries are supported but should be used only when
   their maintenance benefit is worth the broader activation scope.[^exact-names-wildcard-syntax-and-wildcard-best-practices][^best-practices]
2. For new v2 namespaced designs, select `.m.` modern namespaced MRDs when
   provider compatibility and migration requirements permit. Legacy resources
   remain documented for backward compatibility, so this is not an unconditional
   migration rule.[^modern-and-legacy-managed-resource-styles]
3. Package the MRAP with the Crossplane Configuration that supplies the
   dependent Compositions. This creates a composition/configuration-specific
   dependency boundary without asserting that a Composition owns an MRAP.[^configuration-package-mrap-dependency-guidance][^dependency-recommendation]
4. Allow overlap when two configurations need the same MRD. Policies are
   additive, so either policy can activate it and both may report it.[^additive-overlap-and-non-deactivation-e2e-behavior]

# One-way planning constraint

MRAP is Alpha and activation is irreversible: matching sets an MRD Active, and
neither policy deletion nor later narrowing changes it back to Inactive.[^additive-overlap-and-non-deactivation-e2e-behavior][^activation-only-reconciliation][^irreversible-mrd-state]
Therefore minimal activation is preventive. Do not first deploy the default
wildcard and expect a later exact policy to remove unused APIs.

The user-facing ambiguity of an unqualified `kubectl get buckets` across
multiple API groups is not established by the selected Crossplane sources.
Use the fully qualified resource/group while checking the Kubernetes client
behavior in the target cluster; do not rely on short-name resolution during an
API migration.

# Relationships

See [ManagedResourceActivationPolicy](managed-resource-activation-policy.md)
for API matching and lifecycle behavior. [Provider families](/providers/provider-families.md)
can reduce a provider package's resource surface; MRAP then limits which
shipped MRDs become active.

[^helm-default-activation-and-disabling-it]: [Helm default activation and disabling it](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L166-L191)
[^exact-names-wildcard-syntax-and-wildcard-best-practices]: [Exact names, wildcard syntax, and wildcard best practices](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L72-L91) and [best practices](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L452-L466)
[^best-practices]: [best practices](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L452-L466)
[^modern-and-legacy-managed-resource-styles]: [Modern and legacy managed-resource styles](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L122-L151)
[^configuration-package-mrap-dependency-guidance]: [Configuration package MRAP dependency guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L276-L292) and [dependency recommendation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L459-L463)
[^dependency-recommendation]: [dependency recommendation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resource-activation-policies.md#L459-L463)
[^additive-overlap-and-non-deactivation-e2e-behavior]: [Additive overlap and non-deactivation E2E behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/test/e2e/apiextensions_activation_policy_test.go#L191-L256)
[^activation-only-reconciliation]: [Activation-only reconciliation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/activationpolicy/reconciler.go#L106-L147) and [irreversible MRD state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_types.go#L25-L54)
[^irreversible-mrd-state]: [irreversible MRD state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1alpha1/mrd_types.go#L25-L54)
