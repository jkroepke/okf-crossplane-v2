---
type: function
title: Context in function-go-templating
description: Read, create, and deeply update composition-function pipeline context from Go templates.
resource: https://github.com/crossplane-contrib/function-go-templating/tree/0a1e6d386f4363fae257ddbfb5b497416370e830/example/context
tags: [crossplane, composition-function, context, pipeline]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: readme-request-data-and-subsequent-step-context-visibility
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73'
    title: 'README request data and subsequent-step context visibility'
  - id: meta-kind-processing-and-context-response-writes
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L270-L334'
    title: 'Meta-kind processing and Context response writes'
  - id: bundled-context-pipeline-example
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/context/composition.yaml#L22-L58'
    title: 'Bundled Context pipeline example'
  - id: invalid-scalar-context-data-test
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1005-L1043'
    title: 'Invalid scalar Context data test'
  - id: deep-merge-implementation-and-tests
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/context.go#L10-L20'
    title: 'Deep merge implementation and tests'
  - id: repository-apache-2-0-license
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/LICENSE'
    title: 'Repository Apache-2.0 license'
  - id: extraresources-v2-and-compatibility-requirement-fields
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L311-L327'
    title: 'ExtraResources v2 and compatibility requirement fields'
  - id: claimconditions-composite-and-claim-targets
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/claimconditions.go#L12-L77'
    title: 'ClaimConditions composite and claim targets'
  - id: readme-context-guidance-and-later-step-visibility
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277'
    title: 'README Context guidance and later-step visibility'
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

Templates receive the incoming composition-function context as `.context`.[^readme-request-data-and-subsequent-step-context-visibility]
They can render a special `meta.gotemplating.fn.crossplane.io/v1alpha1`
`Context` document to create or update context returned to Crossplane. The
function consumes this document as an instruction; it does not add it to the
desired composed resources.[^meta-kind-processing-and-context-response-writes]

Context returned by a pipeline step is available to subsequent steps.[^readme-context-guidance-and-later-step-visibility] A
template can therefore read data written by an earlier function, transform it,
and publish new or updated keys.[^bundled-context-pipeline-example]

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
a scalar `data` value produces a fatal function result.[^meta-kind-processing-and-context-response-writes][^invalid-scalar-context-data-test]

# Behavior

- An empty `data: {}` map leaves the incoming context unchanged.[^deep-merge-implementation-and-tests]
- New top-level keys are added. Existing maps are merged recursively, and
  values from the rendered `Context` override existing values at the same
  nested path.[^deep-merge-implementation-and-tests]
- Every merged top-level value is converted to a protobuf value and written to
  the response context. A value that cannot be converted produces a fatal
  result.[^meta-kind-processing-and-context-response-writes]
- Templates read incoming context, not context produced earlier in the same
  rendering pass. A single template can still copy an incoming value to a new
  key, as the bundled example demonstrates.[^bundled-context-pipeline-example]

## Multiple Context documents

Each rendered `Context` document is merged independently against the original
request context. Response writes from earlier documents are not used as the
merge base for later documents.[^meta-kind-processing-and-context-response-writes][^deep-merge-implementation-and-tests]

- New, distinct top-level keys from multiple documents remain in the response.
- If documents update the same top-level key, the later document writes the
  complete value obtained from original context plus its own update. Earlier
  same-invocation additions beneath that key can therefore be lost.

Prefer one `Context` document per function invocation when several updates
touch the same top-level key.

# Example

This summarized v2-safe pattern updates a nested environment value, copies an
incoming value to another key, and adds a new key:[^bundled-context-pipeline-example]

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
than copied as a complete Composition.[^bundled-context-pipeline-example][^repository-apache-2-0-license]

# Special meta kinds and Crossplane v2

The selected runtime switch accepts Context, ExtraResources, and ClaimConditions
at the meta API version.[^meta-kind-processing-and-context-response-writes]

| Kind | Crossplane v2 status |
|---|---|
| `Context` | V2-safe. Updates pipeline context as documented above. |
| `ExtraResources` | V2-safe capability. Emits current `requirements.resources`; the release also retains a deprecated v1 compatibility path for cluster-scoped selectors.[^extraresources-v2-and-compatibility-requirement-fields] |
| `ClaimConditions` | Partially v2-safe. The default or `Composite` target emits a condition for the XR. `CompositeAndClaim` targets a Claim and is excluded from claim-free v2 usage.[^claimconditions-composite-and-claim-targets] |

An unknown kind under this API version produces a fatal result. The error text
does not include every accepted kind; the runtime switch is authoritative for
released behavior.[^meta-kind-processing-and-context-response-writes]

# Limitations

- `Context` is an Alpha instruction because its API version is `v1alpha1`.
- Context keys are shared pipeline state. Use qualified keys when ownership
  could collide with another function.
- Multiple documents that update the same top-level key have the overwrite
  behavior described above; they are not accumulated sequentially.
- The selected release does not test collisions involving arrays, nulls, or
  unlike value types. Avoid relying on undocumented collision semantics for
  those cases.
- The Claim target of `ClaimConditions` is excluded from legacy-free v2 usage.

# Relationships

See [request data and pipeline context](request-data.md) for the other request
fields exposed to templates. `ExtraResources` also stores fetched resource
groups beneath the reserved context key
`apiextensions.crossplane.io/extra-resources`.[^extraresources-v2-and-compatibility-requirement-fields]

[^readme-request-data-and-subsequent-step-context-visibility]: [README request data and subsequent-step context visibility](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73)
[^meta-kind-processing-and-context-response-writes]: [Meta-kind processing and Context response writes](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L270-L334)
[^bundled-context-pipeline-example]: [Bundled Context pipeline example](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/context/composition.yaml#L22-L58)
[^invalid-scalar-context-data-test]: [Invalid scalar Context data test](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1005-L1043)
[^deep-merge-implementation-and-tests]: [Deep merge implementation and tests](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/context.go#L10-L20)
[^repository-apache-2-0-license]: [Repository Apache-2.0 license](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/LICENSE)
[^extraresources-v2-and-compatibility-requirement-fields]: [ExtraResources v2 and compatibility requirement fields](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L311-L327)
[^claimconditions-composite-and-claim-targets]: [ClaimConditions composite and claim targets](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/claimconditions.go#L12-L77)
[^readme-context-guidance-and-later-step-visibility]: [README Context guidance and later-step visibility](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L241-L277)
