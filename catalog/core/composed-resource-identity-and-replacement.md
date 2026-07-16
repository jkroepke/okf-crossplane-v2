---
type: concept
title: Composed-resource identity and replacement
description: Why changing metadata.name under an unchanged logical resource key does not rename or replace an existing composed object, and how to stage a replacement.
resource: https://docs.crossplane.io/v2.3/composition/compositions/
tags: [crossplane, core, composition, composed-resources, identity, replacement]
timestamp: 2026-07-16T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - internal/controller/apiextensions/composite/composed.go
  - internal/controller/apiextensions/composite/composition_functions.go
  - internal/controller/apiextensions/composite/composition_render.go
feature_state: Stable by repository default; managementPolicies discussed separately are Beta
---

# Identity

A composed resource has distinct Composition, Kubernetes, and provider-side
identities. Treating them as interchangeable causes unsafe rename and
replacement plans.

| Identity | Scope | Replacement significance |
|---|---|---|
| Logical composition-resource key | An entry in Function desired and observed resource maps, persisted on the object as `crossplane.io/composition-resource-name` | The same key means the same composed resource. A new key declares a different desired resource.[1][2][16] |
| `metadata.name` | Kubernetes object identity | Kubernetes names cannot be updated. After Crossplane associates a key with an observed object, it preserves that object's name.[3][4] |
| `crossplane.io/external-name` | Provider-facing external identity for a managed resource | It is separate from the Kubernetes name. When supplied, its value is used as the external resource name.[5] |

# Behavior when `metadata.name` changes

Assume a Function keeps the logical key `database`, an existing object under
that key is successfully observed as `database-v1`, and a revised Composition
returns `database-v2`:

```text
observed["database"].metadata.name = "database-v1"
desired["database"].metadata.name  = "database-v2"
applied["database"].metadata.name  = "database-v1"
```

This is the released v2.3.3 behavior:

1. Crossplane loads objects referenced by the XR and indexes them by their
   logical composition-resource key.[2]
2. When a desired key matches an observed key, Crossplane unconditionally
   replaces the desired name, namespace, and `generateName` with the observed
   values.[4]
3. Crossplane server-side applies the resulting object at the preserved name.[6]

Therefore changing only `metadata.name` under an unchanged logical key does
**not** rename the old object and does **not** create a replacement object. The
new name is discarded before the API request, so this path does not produce a
Kubernetes immutable-name error or a name-change-specific warning. Other valid
desired fields may still be applied to the existing object.[4][6]

This conclusion is conditional on the existing object being found and
associated with the same logical key. The selected release has no dedicated
unit test that supplies an explicit different desired name under an existing
key, but the identity overwrite is unconditional in the released code.

# Deletion and immutable-field boundaries

If the referenced Kubernetes object is fully deleted, the observer confirms
`NotFound` with an uncached read and omits it from observed state. On the next
reconciliation there is no observed identity to restore, so an explicit desired
name survives, or Crossplane generates a name when none is supplied. Crossplane
persists the new reference before server-side apply creates the absent
object.[7][8]

Manual deletion can therefore make a changed name take effect, but only after
the old object is gone. For a managed resource, finalizers can delay that point
while the Provider handles the external resource. This is a destructive
recreation-after-absence path, not an in-place rename.[9]

Two related behaviors must remain separate:

- The Composition controller deletes an observed Kubernetes object when its
  logical key is omitted from final desired state.[10][11]
- For a Provider-defined immutable `forProvider` field, Crossplane does not use
  the field change itself as a force-replacement signal. The managed reconciler
  creates when the external resource is absent, but calls `Update` when it
  exists and differs; an update failure has no Core delete-and-create fallback.[12][13]

The narrow defensible rule is: **Crossplane Core does not automatically delete
and recreate an existing resource solely to apply an immutable-field change.**
The broader statement that recreation happens only after explicit Kubernetes
deletion is inaccurate. For example, with `Create` permitted, a Provider may
recreate an external resource that was deleted outside Crossplane while its
Kubernetes managed resource still exists.[14]

# Composition guidance

## Keep identity stable for normal updates

- Keep both the logical composition-resource key and `metadata.name` stable
  after creation.
- Prefer letting Crossplane generate the Kubernetes name unless a stable
  explicit name is required.[15]
- If a name change was accidental, restore the Composition's desired name to
  the observed name. Do not edit XR resource references or identity annotations
  to force reassociation.

## Stage an intentional replacement

For a rename or any other immutable change that requires replacement:

1. Add the replacement under a **new logical key** and a distinct Kubernetes
   name, while continuing to render the old key.
2. Wait for the replacement to become ready, migrate data when required, and
   move references, consumers, and published connection details.
3. In a later Composition revision, omit the old key. Crossplane then garbage
   collects the old composed Kubernetes object.[10][11]

This two-stage pattern is inferred guidance from the documented desired-state
contract and the released controller ordering. It provides an explicit
create-before-delete transition at the Composition level. A one-step change
that removes the old key and adds the new key does not: v2.3.3 garbage collects
the old object before it records and applies the new desired object.[10]

Before removing an old managed resource, verify its Provider behavior,
finalizers, `managementPolicies`, external deletion consequences, dependency
ordering, and data-retention requirements. Management Policies are Beta and
Provider support varies.[9][14]

Manual deletion of the old composed object is a last-resort replacement method.
It can cause downtime or external-resource deletion and should be used only
after those effects are explicitly accepted.

# Relationships

This identity behavior applies to objects produced by a
[Composition](composition.md). Provider-side immutable fields are introduced in
[managed resource anatomy](managed-resource-anatomy.md), while adoption and
provider-facing names are covered by
[external identity and creation safety](managed-resource-external-identity.md).

# Limitations

- The exact name-preservation proof is scoped to the Crossplane v2.3.3 Function
  composer and assumes the composed resource kind is unchanged.
- Official v2.3 documentation provides the desired-state and immutable-field
  mechanisms but no end-to-end composed-resource rename procedure. The staged
  replacement procedure is an implementation-backed authoring inference.
- Crossplane Core cannot establish whether every Provider or external service
  avoids an internal replacement during its own `Update` implementation.

# Citations

[1] [Logical `ResourceName` is not Kubernetes `metadata.name`](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composed.go#L23-L28)
[2] [Resource-reference lookup and logical-key association](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L778-L868)
[3] [Kubernetes `ObjectMeta.name` cannot be updated](https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types.go#L109-L134)
[4] [Observed name, namespace, and generated-name preservation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L482-L498)
[5] [Managed-resource external names](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L506-L568)
[6] [Server-side apply and invalid-object handling](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L611-L658)
[7] [Missing referenced objects are omitted from observed state](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L808-L817)
[8] [Name generation and references-before-apply ordering](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L528-L595)
[9] [Managed-resource deletion and finalizers](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L826-L840)
[10] [Garbage collection precedes references and apply](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L566-L628)
[11] [Desired-resource omission deletes the composed resource](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/composition/compositions.md#L698-L729)
[12] [Immutable managed-resource fields do not force replacement](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L185-L203)
[13] [Managed reconciler create-versus-update paths](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1349-L1373)
and [existing-resource update behavior](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/reconciler/managed/reconciler.go#L1490-L1541)
[14] [Management policies and recreation after external deletion](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L286-L355)
[15] [Generated composed-resource names are recommended](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_render.go#L74-L100)
[16] [Composition-resource annotation key and accessors](https://github.com/crossplane/crossplane-runtime/blob/fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827/pkg/xcrd/composite.go#L25-L40)
