---
type: function
title: ExtraResources in function-go-templating
description: Request cluster resources by name or labels and consume them directly or through pipeline context.
resource: https://github.com/crossplane-contrib/function-go-templating/tree/0a1e6d386f4363fae257ddbfb5b497416370e830/example/extra-resources
tags: [crossplane, composition-function, extra-resources, context]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: readme-extraresources-declaration-dynamic-selectors-and-access
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L216'
    title: 'README ExtraResources declaration, dynamic selectors, and access'
  - id: requirement-fields-and-selector-conversion
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62'
    title: 'Requirement fields and selector conversion'
  - id: rendered-requirement-processing-and-response-requirements
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L311-L330'
    title: 'Rendered requirement processing and response requirements'
  - id: direct-and-context-lookup-helpers
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L164'
    title: 'Direct and context lookup helpers'
  - id: context-merge-behavior
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L64-L117'
    title: 'Context merge behavior'
  - id: bundled-direct-access-helper-example
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/functions/getExtraResources/composition.yaml#L18-L34'
    title: 'Bundled direct-access helper example'
  - id: repository-apache-2-0-license
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/LICENSE'
    title: 'Repository Apache-2.0 license'
  - id: legacy-then-current-context-merge-call-order
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L370-L384'
    title: 'Legacy-then-current context merge call order'
  - id: crossplane-protocol-contract-for-missing-required-resources
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L70-L92'
    title: 'Crossplane protocol contract for missing required resources'
  - id: crossplane-required-resource-fetch-repeat-and-stabilization-loop
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L149'
    title: 'Crossplane required-resource fetch, repeat, and stabilization loop'
  - id: exact-name-notfound-and-label-list-fetch-behavior
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L171-L227'
    title: 'Exact-name NotFound and label-list fetch behavior'
  - id: helper-tests-for-empty-items-and-absent-paths
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps_test.go#L572-L593'
    title: 'Helper tests for empty items and absent paths'
  - id: template-execution-fatal-result-path
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L90-L118'
    title: 'Template execution fatal-result path'
  - id: crossplane-fetch-error-propagation-into-the-composition-pipeline
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L378-L409'
    title: 'Crossplane fetch-error propagation into the Composition pipeline'
  - id: released-cluster-scoped-label-tests
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1083-L1147'
    title: 'Released cluster-scoped label tests'
  - id: namespaced-exact-name-test
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1762-L1822'
    title: 'namespaced exact-name test'
  - id: go-template-variable-assignment-scope-and-break
    resource: 'https://github.com/golang/go/blob/d563bc4ba3301156c1e6b115a89c659b00d71fe7/src/text/template/doc.go#L121-L127'
    title: 'Go-template variable assignment, scope, and break'
  - id: variable-declaration-and-reassignment
    resource: 'https://github.com/golang/go/blob/d563bc4ba3301156c1e6b115a89c659b00d71fe7/src/text/template/doc.go#L283-L310'
    title: 'variable declaration and reassignment'
  - id: sprig-list-helpers
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/lists.md#L1-L125'
    title: 'Sprig list helpers'
  - id: dictionary-helpers
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L38-L106'
    title: 'dictionary helpers'
  - id: function-go-templating-s-sprig-function-map
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L62'
    title: 'function-go-templating''s Sprig function map'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
source_paths:
  - README.md
  - extraresources.go
  - fn.go
  - fn_test.go
  - function_maps.go
  - function_maps_test.go
  - example/extra-resources/composition.yaml
  - example/functions/getExtraResources/composition.yaml
  - example/functions/getExtraResourcesFromContext/composition.yaml
supporting_source_repository: crossplane/crossplane
supporting_source_tag: v2.3.3
supporting_source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
supporting_source_paths:
  - proto/fn/v1/run_function.proto
  - internal/xfn/required_resources.go
  - internal/xfn/required_resources_test.go
  - internal/controller/apiextensions/composite/composition_functions.go
feature_state: Alpha
feature_state_basis: >-
  The rendered special resource uses
  meta.gotemplating.fn.crossplane.io/v1alpha1.
---

# Overview

A template can render the special
`meta.gotemplating.fn.crossplane.io/v1alpha1` `ExtraResources` object to ask
Crossplane to fetch Kubernetes resources from the local cluster. Each entry
under `requirements` has an arbitrary key that later identifies the returned
group.[^readme-extraresources-declaration-dynamic-selectors-and-access][^requirement-fields-and-selector-conversion]

The implementation can return rendered selectors as response requirements and
can consume matching resources when they are present in a function request.
The bundled example emits a requirement and reads returned items in the same
template.[^readme-extraresources-declaration-dynamic-selectors-and-access][^rendered-requirement-processing-and-response-requirements]

# Schema

Each requirement supports:[^requirement-fields-and-selector-conversion]

| Field | Use | Meaning |
|---|---|---|
| `apiVersion` | Semantically necessary | API version passed to the protocol selector. This function does not validate that it is non-empty. |
| `kind` | Semantically necessary | Kind passed to the protocol selector. This function does not validate that it is non-empty. |
| `matchName` | Conditional | Exact resource name. Used when it is non-empty. |
| `matchLabels` | Conditional | Label map. Used when `matchName` is empty; an empty map therefore selects by an empty label set. |
| `namespace` | No | Namespace for a namespaced resource. In v0.12.2 the implementation copies it only when `matchName` is non-empty; it is ignored on the `matchLabels` path. Omit it for a cluster-scoped resource. |

The template itself may compute selector values from request data, including labels derived from the observed composite resource.[^readme-extraresources-declaration-dynamic-selectors-and-access]

# Behavior

- Multiple `ExtraResources` documents may contribute requirements, but requirement keys must be unique across the rendered output. A duplicate key produces a fatal function result.[^rendered-requirement-processing-and-response-requirements]
- A non-empty `matchName` takes precedence over `matchLabels`. When `matchName`
  is empty, the function constructs a label selector from `matchLabels`.[^requirement-fields-and-selector-conversion]
  This conflicts with the field comment, which says defined labels cause the
  name to be ignored; the catalog follows runtime behavior.
- The current `required_resources` protocol field receives every selector. For compatibility with the older interface, the deprecated `extra_resources` field also receives cluster-scoped selectors.[^rendered-requirement-processing-and-response-requirements]
- Fetched results are exposed in template data by requirement key. `getExtraResources . "key"` reads the current request's `requiredResources[key].items`, falling back to `extraResources[key].items`; a missing key returns `nil`.[^direct-and-context-lookup-helpers]
- The function copies fetched results into response context at
  `apiextensions.crossplane.io/extra-resources`. Within either the legacy
  `extra_resources` map or current `required_resources` map, request groups
  replace same-key groups from incoming context and unrelated context groups
  are retained.[^context-merge-behavior]
- When both protocol maps are non-empty, the function processes legacy results
  first and current results second. Each merge starts from the incoming request
  context, so the second response-context write supersedes the first. Current
  `required_resources` groups therefore win; legacy-only groups from that same
  invocation are not guaranteed to survive.[^context-merge-behavior][^legacy-then-current-context-merge-call-order]
- `getExtraResourcesFromContext . "key"` reads
  `context[apiextensions.crossplane.io/extra-resources][key].items`; a missing
  entry returns `nil`. This is useful in a later pipeline step or when reading
  resources accumulated by an earlier invocation.[^direct-and-context-lookup-helpers][^context-merge-behavior]

## No-match execution

`requiredResources` is protocol terminology for resources Crossplane must try
to fetch. It does **not** require at least one matching object. Crossplane
v2.3.3 and function-go-templating v0.12.2 handle a successful zero-match lookup
as follows:[^crossplane-protocol-contract-for-missing-required-resources][^crossplane-required-resource-fetch-repeat-and-stabilization-loop]

1. The function returns the selector in its response requirements.
2. Crossplane attempts the lookup and records the requirement key even when no
   object matched.
3. Crossplane calls the function again with the empty result.
4. The function renders normally. Once it returns the same requirements,
   Crossplane considers them stable and continues the Composition pipeline.

The released code preserves a low-level distinction between selector types:

| Selector | Zero-match representation | Outcome |
|---|---|---|
| Exact `matchName` | Kubernetes `NotFound` becomes a nil resource group without an error. | The requirement key is recorded and the function is called again. |
| `matchLabels` | A successful empty `List` becomes a resource group with zero items. | The requirement key is recorded and the function is called again. |

The function helpers may expose a present zero-item path as an empty slice and
an absent path as `nil`; protobuf-to-map conversion can also omit an empty
repeated `items` field. Ordinary `range` treats both as zero elements, and the
bundled examples normalize them with `default (list)`.[^exact-name-notfound-and-label-list-fetch-behavior][^helper-tests-for-empty-items-and-absent-paths]

No-match behavior is therefore permissive by default: the composition
continues and a range over the result emits nothing. A template that needs at
least one object must enforce that condition itself. Template evaluation errors
still produce a fatal function result, actual Kubernetes fetch errors other
than `NotFound` abort the pipeline step, and requirements that keep changing
eventually fail the bounded stabilization loop.[^crossplane-required-resource-fetch-repeat-and-stabilization-loop][^template-execution-fatal-result-path][^crossplane-fetch-error-propagation-into-the-composition-pipeline]

# Example

This summarized pattern requests resources by label, then safely iterates over the returned list:[^readme-extraresources-declaration-dynamic-selectors-and-access][^bundled-direct-access-helper-example]

```yaml
apiVersion: meta.gotemplating.fn.crossplane.io/v1alpha1
kind: ExtraResources
requirements:
  buckets:
    apiVersion: s3.aws.upbound.io/v1beta1
    kind: Bucket
    matchLabels:
      example: "true"
---
{{- range $resource := (getExtraResources . "buckets" | default (list)) }}
# Use $resource here.
{{- end }}
```

The example is summarized from the Apache-2.0-licensed project source; it is not a verbatim runnable Composition and the selected API version and kind must exist in the cluster.[^bundled-direct-access-helper-example][^repository-apache-2-0-license]

## Template-side namespace filter

This illustrative template-side pattern retains the first returned item from
the composite's namespace, then uses it outside the loop. `break` stops the
template scan after that match:[^go-template-variable-assignment-scope-and-break][^variable-declaration-and-reassignment]

```gotemplate
{{- $selected := dict }}
{{- $namespace := $.observed.composite.resource.metadata.namespace }}
{{- range $extraResource := (getExtraResources . "bucket" | default (list)) }}
  {{- if eq $extraResource.resource.metadata.namespace $namespace }}
    {{- $selected = $extraResource }}
    {{- break }}
  {{- end }}
{{- end }}

{{- if $selected }}
# Render a desired resource using $selected.resource here.
{{- end }}
```

`getExtraResources` reads the items already included in the function request;
it does not construct or alter an `ExtraResources` selector.[^direct-and-context-lookup-helpers] This is
therefore a template-side **consumption** filter: it can prevent
cross-namespace items from influencing rendered desired resources, but cannot
narrow the earlier all-namespace `List`, reduce its RBAC requirement, or avoid
the associated lookup cost.[^requirement-fields-and-selector-conversion][^exact-name-notfound-and-label-list-fetch-behavior]

Sprig v3.3.0 has no predicate-based list filter or nested-field finder for this
unstructured result shape. Its list helpers operate on whole list items, while
`pluck` selects a top-level key from explicitly supplied dictionaries and `dig`
traverses one dictionary. The `range` is therefore still needed to find a
matching item; the variable assignment and `break` are Go-template syntax, not
Sprig functions.[^go-template-variable-assignment-scope-and-break][^variable-declaration-and-reassignment][^sprig-list-helpers][^dictionary-helpers][^function-go-templating-s-sprig-function-map]

# Limitations

- The special `ExtraResources` object is a function rendering directive, not a Kubernetes object that is added to desired composed resources.[^rendered-requirement-processing-and-response-requirements]
- Label selectors are equality maps only; this schema does not expose set-based selector expressions.[^requirement-fields-and-selector-conversion]
- `matchLabels` works for cluster-scoped resources; the released tests cover
  both a non-empty label map and an empty label map.[^released-cluster-scoped-label-tests][^namespaced-exact-name-test] The limitation is
  namespace scoping: although the schema accepts `namespace` beside
  `matchLabels`, v0.12.2 returns the label selector before copying the
  namespace. Crossplane consequently receives an empty namespace and performs
  an all-namespace label list, subject to RBAC, rather than limiting the list
  to the supplied namespace. The only released namespaced test uses
  `matchName`.[^requirement-fields-and-selector-conversion][^exact-name-notfound-and-label-list-fetch-behavior][^released-cluster-scoped-label-tests][^namespaced-exact-name-test]
- The README's response illustration shows arrays directly beneath requirement
  keys, but its access syntax and released helpers read an `items` envelope.
  Follow the implementation-backed `requiredResources[key].items` shape.[^readme-extraresources-declaration-dynamic-selectors-and-access][^direct-and-context-lookup-helpers]
- Retrieval timing and any result-count limit are controlled by Crossplane's composition-function protocol, not by the template helper. The selected function source does not define its own count limit.
- This function forwards empty `apiVersion` or `kind` strings and does not
  validate that exactly one match field is set. Any protocol-side rejection is
  outside the selected function source.[^requirement-fields-and-selector-conversion]
- Because result lookup returns `nil` for absent paths, use `default (list)` before ranging when a request may have no result.[^direct-and-context-lookup-helpers][^bundled-direct-access-helper-example]
- For a namespaced `matchLabels` requirement, a template-side namespace test
  filters only the returned results. It is not a retrieval-scope or
  least-privilege mitigation; use `matchName` when an exact name is available.
- The early-stop pattern is first-match-wins. If multiple resources in the
  composite's namespace match, define a stronger selector or an explicit
  selection policy before using the retained item.
- Do not use the word `required` as a cardinality guarantee. The selected
  protocol and implementations impose no minimum match count.[^crossplane-protocol-contract-for-missing-required-resources][^crossplane-required-resource-fetch-repeat-and-stabilization-loop]

# Relationships

See [template functions](template-functions.md) for all helper signatures and [request data and context](request-data.md) for the rest of the request available to templates. [Composed-resource RBAC](../../core/composed-resource-rbac.md) identifies the Crossplane Core service account as the required-resource read principal; do not grant these reads to the Function pod merely because the Function declared the selector.

[^readme-extraresources-declaration-dynamic-selectors-and-access]: [README ExtraResources declaration, dynamic selectors, and access](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L216)
[^requirement-fields-and-selector-conversion]: [Requirement fields and selector conversion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62)
[^rendered-requirement-processing-and-response-requirements]: [Rendered requirement processing and response requirements](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L311-L330)
[^direct-and-context-lookup-helpers]: [Direct and context lookup helpers](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L164)
[^context-merge-behavior]: [Context merge behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L64-L117)
[^bundled-direct-access-helper-example]: [Bundled direct-access helper example](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/functions/getExtraResources/composition.yaml#L18-L34)
[^repository-apache-2-0-license]: [Repository Apache-2.0 license](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/LICENSE)
[^legacy-then-current-context-merge-call-order]: [Legacy-then-current context merge call order](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L370-L384)
[^crossplane-protocol-contract-for-missing-required-resources]: [Crossplane protocol contract for missing required resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L70-L92)
[^crossplane-required-resource-fetch-repeat-and-stabilization-loop]: [Crossplane required-resource fetch, repeat, and stabilization loop](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L149)
[^exact-name-notfound-and-label-list-fetch-behavior]: [Exact-name NotFound and label-list fetch behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L171-L227)
[^helper-tests-for-empty-items-and-absent-paths]: [Helper tests for empty items and absent paths](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps_test.go#L572-L593)
[^template-execution-fatal-result-path]: [Template execution fatal-result path](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L90-L118)
[^crossplane-fetch-error-propagation-into-the-composition-pipeline]: [Crossplane fetch-error propagation into the Composition pipeline](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L378-L409)
[^released-cluster-scoped-label-tests]: [Released cluster-scoped label tests](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1083-L1147) and [namespaced exact-name test](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1762-L1822)
[^namespaced-exact-name-test]: [namespaced exact-name test](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1762-L1822)
[^go-template-variable-assignment-scope-and-break]: [Go-template variable assignment, scope, and `break`](https://github.com/golang/go/blob/d563bc4ba3301156c1e6b115a89c659b00d71fe7/src/text/template/doc.go#L121-L127) and [variable declaration and reassignment](https://github.com/golang/go/blob/d563bc4ba3301156c1e6b115a89c659b00d71fe7/src/text/template/doc.go#L283-L310)
[^variable-declaration-and-reassignment]: [variable declaration and reassignment](https://github.com/golang/go/blob/d563bc4ba3301156c1e6b115a89c659b00d71fe7/src/text/template/doc.go#L283-L310)
[^sprig-list-helpers]: [Sprig list helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/lists.md#L1-L125) and [dictionary helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L38-L106)
[^dictionary-helpers]: [dictionary helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L38-L106)
[^function-go-templating-s-sprig-function-map]: [function-go-templating's Sprig function map](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L62)
