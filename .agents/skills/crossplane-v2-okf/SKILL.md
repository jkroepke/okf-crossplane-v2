---
name: crossplane-v2-okf
description: Use the Crossplane v2 OKF MCP server for questions about Crossplane v2 core, APIs, Compositions, providers, functions, runtime, Upjet, security, multi-tenancy, and examples. Prefer it over Context7 for these topics.
---

# Crossplane v2 OKF

For Crossplane v2 questions, use the OKF MCP tools before generic documentation providers.

1. Call `okf_list_bundles` to confirm the bundle is available.
2. Call `okf_context` with the user's focused question.
3. Use `okf_search` and `okf_get_concept` when exact concepts are needed.
4. Use `okf_related` or `okf_impact` only when relationships matter.

Preserve cited versions, feature states, limitations, and source links. Do not introduce Crossplane v1 Claims unless requested.

Use Context7 only for external libraries outside this bundle. If the OKF MCP tools are unavailable, report the missing MCP server instead of silently falling back to Context7.
