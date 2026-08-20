---
type: concept
title: Managed resource external identity and creation safety
description: External-name identity, provider-specific adoption, and timestamp guards against duplicate resources after uncertain creates.
resource: https://docs.crossplane.io/v2.3/managed-resources/managed-resources/
tags: [crossplane, core, managed-resources, external-name, creation-safety]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: external-name-annotation-and-initializer
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/meta/meta.go#L35-L39'
    title: 'External-name annotation and initializer'
  - id: initializer-behavior
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/api.go#L58-L76'
    title: 'initializer behavior'
  - id: documented-external-lookup-behavior
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L607-L621'
    title: 'Documented external lookup behavior'
  - id: creation-timestamp-persistence
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1349-L1445'
    title: 'Creation timestamp persistence'
  - id: incomplete-creation-detection-and-deterministic-name-exception
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1100-L1116'
    title: 'Incomplete creation detection and deterministic-name exception'
  - id: recent-create-guard
    resource: 'https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1210-L1225'
    title: 'Recent-create guard'
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane-runtime
source_commit: fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827
source_paths: [pkg/meta/meta.go, pkg/reconciler/managed/reconciler.go]
feature_state: Not stated by selected sources
---

# External identity

`crossplane.io/external-name` stores the provider-facing identifier. A Provider may initialize it from the Kubernetes name only when it is empty; its exact format and lookup semantics are
provider-specific.[^external-name-annotation-and-initializer][^initializer-behavior]

Pre-setting external name can support observing an existing resource only when that Provider's `Observe` implementation understands the identifier. The runtime defines no universal import
or adoption guarantee.[^documented-external-lookup-behavior]

# Creation leak protection

Before calling `Create`, the reconciler persists `crossplane.io/external-create-pending`. It then records either `external-create-succeeded` or `external-create-failed` after the call.[^creation-timestamp-persistence]

When the newest pending timestamp is later than both success and failure, creation may have succeeded without Crossplane learning the result. Controllers without deterministic external names
stop rather than risk a duplicate. Controllers configured with deterministic external names continue because another create resolves to the same identity.[^incomplete-creation-detection-and-deterministic-name-exception] Removing the pending annotation
from a stopped resource is an operator safety decision, not proof that creation failed.

After a recently successful create, a temporarily absent observation is treated as likely eventual consistency and is requeued rather than recreated immediately.[^recent-create-guard]

[^external-name-annotation-and-initializer]: [External-name annotation and initializer](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/meta/meta.go#L35-L39) and [initializer behavior](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/api.go#L58-L76)
[^initializer-behavior]: [initializer behavior](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/api.go#L58-L76)
[^documented-external-lookup-behavior]: [Documented external lookup behavior](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L607-L621)
[^creation-timestamp-persistence]: [Creation timestamp persistence](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1349-L1445)
[^incomplete-creation-detection-and-deterministic-name-exception]: [Incomplete creation detection and deterministic-name exception](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1100-L1116)
[^recent-create-guard]: [Recent-create guard](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1210-L1225)
