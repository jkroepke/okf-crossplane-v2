---
type: function
title: ExtraResources in function-go-templating
description: Request cluster resources by name or labels and consume them directly or through pipeline context.
resource: https://github.com/crossplane-contrib/function-go-templating/tree/0a1e6d386f4363fae257ddbfb5b497416370e830/example/extra-resources
tags: [crossplane, composition-function, extra-resources, context]
timestamp: 2026-07-14T00:00:00Z
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
group.[1][2]

The implementation can return rendered selectors as response requirements and
can consume matching resources when they are present in a function request.
The bundled example emits a requirement and reads returned items in the same
template.[1][3]

# Schema

Each requirement supports:[2]

| Field | Use | Meaning |
|---|---|---|
| `apiVersion` | Semantically necessary | API version passed to the protocol selector. This function does not validate that it is non-empty. |
| `kind` | Semantically necessary | Kind passed to the protocol selector. This function does not validate that it is non-empty. |
| `matchName` | Conditional | Exact resource name. Used when it is non-empty. |
| `matchLabels` | Conditional | Label map. Used when `matchName` is empty; an empty map therefore selects by an empty label set. |
| `namespace` | No | Namespace for a namespaced resource. In v0.12.2 the implementation copies it only when `matchName` is non-empty; it is ignored on the `matchLabels` path. Omit it for a cluster-scoped resource. |

The template itself may compute selector values from request data, including labels derived from the observed composite resource.[1]

# Behavior

- Multiple `ExtraResources` documents may contribute requirements, but requirement keys must be unique across the rendered output. A duplicate key produces a fatal function result.[3]
- A non-empty `matchName` takes precedence over `matchLabels`. When `matchName`
  is empty, the function constructs a label selector from `matchLabels`.[2]
  This conflicts with the field comment, which says defined labels cause the
  name to be ignored; the catalog follows runtime behavior.
- The current `required_resources` protocol field receives every selector. For compatibility with the older interface, the deprecated `extra_resources` field also receives cluster-scoped selectors.[3]
- Fetched results are exposed in template data by requirement key. `getExtraResources . "key"` reads the current request's `requiredResources[key].items`, falling back to `extraResources[key].items`; a missing key returns `nil`.[4]
- The function copies fetched results into response context at
  `apiextensions.crossplane.io/extra-resources`. Within either the legacy
  `extra_resources` map or current `required_resources` map, request groups
  replace same-key groups from incoming context and unrelated context groups
  are retained.[5]
- When both protocol maps are non-empty, the function processes legacy results
  first and current results second. Each merge starts from the incoming request
  context, so the second response-context write supersedes the first. Current
  `required_resources` groups therefore win; legacy-only groups from that same
  invocation are not guaranteed to survive.[5][8]
- `getExtraResourcesFromContext . "key"` reads
  `context[apiextensions.crossplane.io/extra-resources][key].items`; a missing
  entry returns `nil`. This is useful in a later pipeline step or when reading
  resources accumulated by an earlier invocation.[4][5]

## No-match execution

`requiredResources` is protocol terminology for resources Crossplane must try
to fetch. It does **not** require at least one matching object. Crossplane
v2.3.3 and function-go-templating v0.12.2 handle a successful zero-match lookup
as follows:[9][10]

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
bundled examples normalize them with `default (list)`.[11][12]

No-match behavior is therefore permissive by default: the composition
continues and a range over the result emits nothing. A template that needs at
least one object must enforce that condition itself. Template evaluation errors
still produce a fatal function result, actual Kubernetes fetch errors other
than `NotFound` abort the pipeline step, and requirements that keep changing
eventually fail the bounded stabilization loop.[10][13][14]

# Example

This summarized pattern requests resources by label, then safely iterates over the returned list:[1][6]

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

The example is summarized from the Apache-2.0-licensed project source; it is not a verbatim runnable Composition and the selected API version and kind must exist in the cluster.[6][7]

## Template-side namespace filter

This illustrative template-side pattern filters returned items before emitting
any desired resource when a namespaced resource must be selected with
`matchLabels`. It keeps a resource returned from another namespace out of the
rendered output:

```gotemplate
{{- $someExtraResources := getExtraResources . "bucket" }}
{{- range $i, $extraResource := default (list) $someExtraResources }}
{{- if eq $extraResource.resource.metadata.namespace $.observed.composite.resource.metadata.namespace }}
# Render a desired resource that uses $extraResource.
{{- end }}
{{- end }}
```

`getExtraResources` reads the items already included in the function request;
it does not construct or alter an `ExtraResources` selector.[4] This is
therefore a template-side **consumption** filter: it can prevent
cross-namespace items from influencing rendered desired resources, but cannot
narrow the earlier all-namespace `List`, reduce its RBAC requirement, or avoid
the associated lookup cost.[2][11]

# Limitations

- The special `ExtraResources` object is a function rendering directive, not a Kubernetes object that is added to desired composed resources.[3]
- Label selectors are equality maps only; this schema does not expose set-based selector expressions.[2]
- `matchLabels` works for cluster-scoped resources; the released tests cover
  both a non-empty label map and an empty label map.[15] The limitation is
  namespace scoping: although the schema accepts `namespace` beside
  `matchLabels`, v0.12.2 returns the label selector before copying the
  namespace. Crossplane consequently receives an empty namespace and performs
  an all-namespace label list, subject to RBAC, rather than limiting the list
  to the supplied namespace. The only released namespaced test uses
  `matchName`.[2][11][15]
- The README's response illustration shows arrays directly beneath requirement
  keys, but its access syntax and released helpers read an `items` envelope.
  Follow the implementation-backed `requiredResources[key].items` shape.[1][4]
- Retrieval timing and any result-count limit are controlled by Crossplane's composition-function protocol, not by the template helper. The selected function source does not define its own count limit.
- This function forwards empty `apiVersion` or `kind` strings and does not
  validate that exactly one match field is set. Any protocol-side rejection is
  outside the selected function source.[2]
- Because result lookup returns `nil` for absent paths, use `default (list)` before ranging when a request may have no result.[4][6]
- For a namespaced `matchLabels` requirement, a template-side namespace test
  filters only the returned results. It is not a retrieval-scope or
  least-privilege mitigation; use `matchName` when an exact name is available.
- Do not use the word `required` as a cardinality guarantee. The selected
  protocol and implementations impose no minimum match count.[9][10]

# Relationships

See [template functions](template-functions.md) for all helper signatures and [request data and context](request-data.md) for the rest of the request available to templates.

# Citations

[1] [README ExtraResources declaration, dynamic selectors, and access](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L216)
[2] [Requirement fields and selector conversion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L16-L62)
[3] [Rendered requirement processing and response requirements](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L311-L330)
[4] [Direct and context lookup helpers](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L143-L164)
[5] [Context merge behavior](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L64-L117)
[6] [Bundled direct-access helper example](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/example/functions/getExtraResources/composition.yaml#L18-L34)
[7] [Repository Apache-2.0 license](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/LICENSE)
[8] [Legacy-then-current context merge call order](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L370-L384)
[9] [Crossplane protocol contract for missing required resources](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L70-L92)
[10] [Crossplane required-resource fetch, repeat, and stabilization loop](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L67-L149)
[11] [Exact-name NotFound and label-list fetch behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/xfn/required_resources.go#L171-L227)
[12] [Helper tests for empty items and absent paths](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps_test.go#L572-L593)
[13] [Template execution fatal-result path](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn.go#L90-L118)
[14] [Crossplane fetch-error propagation into the Composition pipeline](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L378-L409)
[15] [Released cluster-scoped label tests](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1083-L1147)
and [namespaced exact-name test](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/fn_test.go#L1762-L1822)
