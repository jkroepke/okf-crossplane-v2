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
  - example/extra-resources/composition.yaml
  - example/functions/getExtraResources/composition.yaml
  - example/functions/getExtraResourcesFromContext/composition.yaml
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
| `namespace` | No | Namespace for a namespaced resource. In v0.12.2 the implementation copies it only when `matchName` is non-empty. Omit it for a cluster-scoped resource. |

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

# Limitations

- The special `ExtraResources` object is a function rendering directive, not a Kubernetes object that is added to desired composed resources.[3]
- Label selectors are equality maps only; this schema does not expose set-based selector expressions.[2]
- Although the schema accepts `namespace` beside either match field, v0.12.2
  copies it to the protocol selector only on the `matchName` path. Namespaced
  label matching is therefore not supported by this implementation.[2]
- The README's response illustration shows arrays directly beneath requirement
  keys, but its access syntax and released helpers read an `items` envelope.
  Follow the implementation-backed `requiredResources[key].items` shape.[1][4]
- Retrieval timing and any result-count limit are controlled by Crossplane's composition-function protocol, not by the template helper. The selected function source does not define its own count limit.
- This function forwards empty `apiVersion` or `kind` strings and does not
  validate that exactly one match field is set. Any protocol-side rejection is
  outside the selected function source.[2]
- Because result lookup returns `nil` for absent paths, use `default (list)` before ranging when a request may have no result.[4][6]

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
