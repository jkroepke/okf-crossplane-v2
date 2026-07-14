---
type: function
title: Context in function-go-templating
description: Read, create, and deeply update composition-function pipeline context from Go templates.
resource: https://github.com/crossplane-contrib/function-go-templating/tree/0a1e6d386f4363fae257ddbfb5b497416370e830/example/context
tags: [crossplane, composition-function, context, pipeline]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths:
  - README.md
  - context.go
  - context_test.go
  - fn.go
  - fn_test.go
  - claimconditions.go
  - example/context/composition.yaml
feature_state: Alpha
feature_state_basis: >-
  The rendered special resource uses
  meta.gotemplating.fn.crossplane.io/v1alpha1.
---

# Overview

Templates receive the incoming composition-function context as `.context`.[1]
They can render a special `meta.gotemplating.fn.crossplane.io/v1alpha1`
`Context` document to create or update context returned to Crossplane. The
function consumes this document as an instruction; it does not add it to the
desired composed resources.[2]

Context returned by a pipeline step is available to subsequent steps.[10] A
template can therefore read data written by an earlier function, transform it,
and publish new or updated keys.[3]

# Schema

```yaml
apiVersion: meta.gotemplating.fn.crossplane.io/v1alpha1
kind: Context
data:
  region: eu-central-1
  settings:
    enabled: true
  zones:
    - a
    - b
```

`data` must be present and decode to a map from string keys to JSON-compatible
values. Values may be scalars, arrays, maps, or null. An omitted `data` field or
a scalar `data` value produces a fatal function result.[2][4]

# Behavior

- An empty `data: {}` map leaves the incoming context unchanged.[5]
- New top-level keys are added. Existing maps are merged recursively, and
  values from the rendered `Context` override existing values at the same
  nested path.[5]
- Every merged top-level value is converted to a protobuf value and written to
  the response context. A value that cannot be converted produces a fatal
  result.[2]
- Templates read incoming context, not context produced earlier in the same
  rendering pass. A single template can still copy an incoming value to a new
  key, as the bundled example demonstrates.[3]

## Multiple Context documents

Each rendered `Context` document is merged independently against the original
request context. Response writes from earlier documents are not used as the
merge base for later documents.[2][5]

- New, distinct top-level keys from multiple documents remain in the response.
- If documents update the same top-level key, the later document writes the
  complete value obtained from original context plus its own update. Earlier
  same-invocation additions beneath that key can therefore be lost.

Prefer one `Context` document per function invocation when several updates
touch the same top-level key.

# Example

This summarized v2-safe pattern updates a nested environment value, copies an
incoming value to another key, and adds a new key:[3]

```yaml
apiVersion: meta.gotemplating.fn.crossplane.io/v1alpha1
kind: Context
data:
  "apiextensions.crossplane.io/environment":
    nested:
      enabled: true
  copied:
    value: {{ index .context "source" "value" }}
  new-key:
    hello: world
```

The example is summarized from the Apache-2.0-licensed project source rather
than copied as a complete Composition.[3][6]

# Special meta kinds and Crossplane v2

The selected runtime switch accepts four kinds at the meta API version.[2]

| Kind | Crossplane v2 status |
|---|---|
| `Context` | V2-safe. Updates pipeline context as documented above. |
| `ExtraResources` | V2-safe capability. Emits current `requirements.resources`; the release also retains a deprecated v1 compatibility path for cluster-scoped selectors.[7] |
| `CompositeConnectionDetails` | Legacy v1 XR only. The selected README explicitly says it is unsupported for v2 XRs; compose a Kubernetes `Secret` instead.[8] |
| `ClaimConditions` | Partially v2-safe. The default or `Composite` target emits a condition for the XR. `CompositeAndClaim` targets a Claim and is excluded from claim-free v2 usage.[9] |

An unknown kind under this API version produces a fatal result. The error text
lists only `CompositeConnectionDetails`, `Context`, and `ExtraResources`, even
though the adjacent runtime case also accepts `ClaimConditions`; the switch is
authoritative for released behavior.[2]

# Limitations

- `Context` is an Alpha instruction because its API version is `v1alpha1`.
- Context keys are shared pipeline state. Use qualified keys when ownership
  could collide with another function.
- Multiple documents that update the same top-level key have the overwrite
  behavior described above; they are not accumulated sequentially.
- The selected release does not test collisions involving arrays, nulls, or
  unlike value types. Avoid relying on undocumented collision semantics for
  those cases.
- `CompositeConnectionDetails` and the Claim target of `ClaimConditions` are
  excluded from legacy-free v2 examples.

# Relationships

See [request data and pipeline context](request-data.md) for the other request
fields exposed to templates. `ExtraResources` also stores fetched resource
groups beneath the reserved context key
`apiextensions.crossplane.io/extra-resources`.[7]

# Citations

[1] [README request data and subsequent-step context visibility](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73)
[2] [Meta-kind processing and Context response writes](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L270-L334)
[3] [Bundled Context pipeline example](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/context/composition.yaml#L22-L58)
[4] [Invalid scalar Context data test](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1005-L1043)
[5] [Deep merge implementation and tests](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/context.go#L10-L20)
[6] [Repository Apache-2.0 license](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/LICENSE)
[7] [ExtraResources v2 and compatibility requirement fields](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L311-L327)
[8] [Legacy-v1 and v2 connection-details guidance](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L78-L122)
[9] [ClaimConditions composite and claim targets](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/claimconditions.go#L12-L77)
[10] [README Context guidance and later-step visibility](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277)
