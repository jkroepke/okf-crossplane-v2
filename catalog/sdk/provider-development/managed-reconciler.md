---
type: Crossplane Development Guide
title: Managed reconciler and typed external-client lifecycle
description: Implement a hand-written provider controller with crossplane-runtime's managed reconciler and typed external connector contract.
resource: https://github.com/crossplane/crossplane-runtime/tree/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed
tags: [crossplane, provider-development, sdk, reconciler, controller]
generated: { by: "process:crossplane-okf-generation", at: "2026-08-20T23:09:30Z" }
sources:
  - id: connector-contract
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L274-L371'
    title: Typed connector and function adapter contracts
  - id: external-client-contract
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L374-L539'
    title: External-client lifecycle and result contracts
  - id: reconciler-options
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L663-L915'
    title: Managed reconciler options and construction
  - id: reconciliation-order
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1083-L1196'
    title: Initialization, reference, connection, observation, event, and condition order
  - id: connection-publication-routing
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L620-L650'
    title: Modern and legacy connection-detail routing
  - id: template-controller-setup
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype.go#L51-L109'
    title: Template managed controller setup
  - id: template-simulated-client
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype.go#L172-L254'
    title: Simulated external-client implementation
  - id: runtime-resource-fakes
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/fake/mocks.go#L343-L425'
    title: Runtime managed-resource test fakes
  - id: runtime-mock-client
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/test/fake.go#L270-L318'
    title: Configurable controller-runtime mock client
  - id: template-empty-observe-tests
    resource: 'https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype_test.go#L39-L75'
    title: Template Observe test scaffold
source_repository: crossplane/crossplane-runtime
source_tag: v2.3.3
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
supporting_source_repository: crossplane/provider-template
supporting_source_commit: a74b386da0ec848036e16ff0a207c5a16bc9827f
source_paths: [pkg/reconciler/managed/reconciler.go, pkg/resource/fake/mocks.go, pkg/test/fake.go]
feature_state: Not stated by selected sources
feature_state_basis: Unlabelled exported Go SDK contracts and implementation behavior; the stable source tag establishes availability, not maturity.
---

# Controller construction

`managed.NewReconciler` requires a scheme-registered managed kind. Its defaults
do not connect to a real external system, so a Provider must install an
external connector.[^reconciler-options] Prefer the typed connector option for
the Provider's concrete managed-resource type; the runtime adapts it to the
managed reconciler.[^connector-contract]

The template composes this with a typed connector, ProviderConfig usage
tracker, poll interval, safe-start gate, desired-state filtering, rate
limiting, optional management-policy and change-log features, and optional
metrics.[^template-controller-setup] Keep only the options the finished
Provider actually supports and tests.

# Reconciliation sequence

For a non-deleting resource, the selected runtime follows this high-level
order:[^reconciliation-order]

```text
Initialize -> Resolve references -> Connect -> Observe
                                      |
                                      +-> Create, late-initialize, update, or poll
                                      +-> Publish connection details and status
```

Reference resolution is skipped during deletion. After connection, the
reconciler defers disconnect and uses the observation result to choose the
next lifecycle action. Connection and observation failures produce warning
events, mark reconcile-error conditions, and trigger a status-update attempt.[^reconciliation-order]

# External-client contract

The typed client methods are designed to be non-blocking and idempotent:[^external-client-contract]

| Method | Contract boundary |
|---|---|
| `Observe` | Read the external resource; do not modify it. Report existence, up-to-date state, and late initialization, and update the managed resource with observed state. |
| `Create` | Create after observation reports absence; return creation details and any connection details. |
| `Update` | Reconcile an existing, outdated external resource and return update connection details when applicable. |
| `Delete` | Request deletion while the Kubernetes managed resource is deleting; repeated calls must be safe. |
| `Disconnect` | Release per-reconcile external client resources when the loop ends. |

Observation, create, and update results can return connection details. For a
modern managed resource, the default reconciler routes them through the local
connection-secret owner contract; the arbitrary-namespace path belongs to the
deprecated legacy resource shape.[^external-client-contract][^connection-publication-routing]

# Replace the simulated service

The template's client deliberately prints configuration, uses a no-op service,
assigns a fixed external name, and copies one sample field between desired and
observed state.[^template-simulated-client] Replace all of that behavior with:

- a provider-specific API client and authentication path;
- deterministic observation and comparison logic;
- create/update/delete calls that satisfy the idempotency contract;
- external-name handling appropriate to the external API; and
- explicit connection details and error handling where the Provider supports them.

Do not generalize the `MyType` simulation into a Provider behavior claim. Its
own Alpha API is only a runnable skeleton.

# Tests

crossplane-runtime supplies fake modern and legacy managed resources,
ProviderConfig-related fakes, and a configurable mock of controller-runtime's
client.[^runtime-resource-fakes][^runtime-mock-client] The template's
table-driven `TestObserve` structure contains no test cases in the selected
snapshot.[^template-empty-observe-tests]

Add cases for at least absence, up-to-date observation, drift, late
initialization, each external error, and every credential/configuration path
the Provider exposes. Test repeated lifecycle calls because the SDK contract
requires idempotency.

# Relationships

The connector obtains its client through
[ProviderConfig and credential wiring](provider-configuration.md). The managed
type that enters this reconciler must satisfy the
[modern managed-resource API contract](managed-resource-apis.md).

[^connector-contract]: [Typed connector and function adapter contracts](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L274-L371)
[^external-client-contract]: [External-client lifecycle and result contracts](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L374-L539)
[^reconciler-options]: [Managed reconciler options and construction](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L663-L915)
[^reconciliation-order]: [Initialization, reference, connection, observation, event, and condition order](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1083-L1196)
[^connection-publication-routing]: [Modern and legacy connection-detail routing](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L620-L650)
[^template-controller-setup]: [Template managed controller setup](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype.go#L51-L109)
[^template-simulated-client]: [Simulated external-client implementation](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype.go#L172-L254)
[^runtime-resource-fakes]: [Runtime managed-resource test fakes](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/resource/fake/mocks.go#L343-L425)
[^runtime-mock-client]: [Configurable controller-runtime mock client](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/test/fake.go#L270-L318)
[^template-empty-observe-tests]: [Template Observe test scaffold](https://github.com/crossplane/provider-template/blob/a74b386da0ec848036e16ff0a207c5a16bc9827f/internal/controller/mytype/mytype_test.go#L39-L75)
