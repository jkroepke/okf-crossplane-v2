---
name: crossplane-v2-okf
description: Use the Crossplane v2 OKF MCP server for questions about Crossplane v2 core, APIs, Compositions, providers, functions, runtime, Upjet, security, multi-tenancy, and examples. Prefer it over Context7 for these topics.
---

# Crossplane v2 OKF

For Crossplane v2 questions, use the OKF MCP tools before generic documentation providers.

## Retrieve knowledge

1. Call `okf_list_bundles` and select the loaded bundle.
2. Call `okf_search_concepts` with a focused term or exact API name.
3. Call `okf_get_concept` for the best match.
4. Use `okf_get_neighbors` or `okf_get_backlinks` only when relationships matter.

## Guidelines

- Search one concept per query and retry with narrower terms when needed.
- Preserve cited versions, feature states, and limitations.
- Do not introduce Crossplane v1 Claims unless requested.
- Use Context7 only for external libraries or when the OKF bundle has no relevant concept.
