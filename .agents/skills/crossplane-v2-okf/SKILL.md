---
name: crossplane-v2-okf
description: Use the Crossplane v2 OKF MCP server as the exclusive external knowledge source for questions about Crossplane v2 core, APIs, Compositions, providers, functions, runtime, Upjet, security, multi-tenancy, and examples. Do not use generic documentation or library retrieval tools for content covered by this bundle.
---

# Crossplane v2 OKF

For every Crossplane v2 ecosystem question, use the OKF MCP tools before answering or creating artifacts.

## General workflow

1. Call `okf_list_bundles` and confirm that the Crossplane v2 bundle is available.
2. Call `okf_context` with the user's focused question.
3. When the task is to build, author, design, or substantially review a
   Crossplane v2 Composition, retrieve the **Develop a Crossplane v2
   Composition** concept with concept ID `composition-developer-starter` as
   the primary routing guide. Follow its links to the required API, provider,
   function, security, readiness, identity, testing, and packaging concepts.
4. Use `okf_search` and `okf_get_concept` when exact concepts or API details are needed.
5. Use `okf_related` or `okf_impact` only when relationships matter.

The Composition developer starter is a navigation route, not a substitute for
provider-specific evidence. Use the provider workflow below for concrete
managed-resource schemas, examples, and upstream Terraform documentation.

## Package versions

Use `get_versions(name)` before selecting a provider or function release when
an exact version was not supplied by the user or the local project.

- Pass a short package name, an `account/package` name, or a full
  `xpkg.upbound.io` package reference.
- Prefer `latest`, which is the highest stable semantic version returned by the
  tool. Do not replace it with the latest prerelease.
- Preserve the resolved package name and selected version in all later tool
  calls and in the answer.
- When the user or local project pins a version, use that exact version and do
  not silently upgrade it.

## Provider CRD workflow

For provider-specific resource questions, use the following sequence. All
provider CRD tools use the argument order shown here.

1. Discover candidates with
   `provider_crd_search(provider_name, provider_version, crd_search_term)`.
   Use a focused kind, API-group, or wildcard term. Do not assume a resource
   from name similarity.
2. Select an exact result and retrieve its schema with
   `provider_crd_get_definition(provider_name, provider_version, crd_name)`.
   Add the optional `path` selector such as `.spec` or `.spec.versions[0]`
   when only part of the CRD is needed; the tool returns that subtree as YAML.
3. When creating or reviewing manifests, retrieve example locations with
   `provider_crd_get_examples(provider_name, provider_version, crd_name)`.
4. For an Upjet-managed resource, retrieve the mapped Terraform documentation
   location with
   `provider_crd_get_terraform_docs(provider_name, provider_version, crd_name)`
   when field semantics, constraints, import behavior, or upstream examples are
   relevant.

`crd_name` may be a kind, `group/Kind`, `group/version/Kind`, or a YAML fragment
containing `apiVersion` and `kind`. Prefer `group/version/Kind` after discovery
because it keeps the API surface explicit and avoids ambiguous kinds.

Keep the same resolved provider name and provider version across search,
definition, examples, and Terraform documentation calls. Never combine a CRD
definition from one provider release with examples or Terraform documentation
resolved from another release.

## Fetching returned source locations

`provider_crd_get_examples` and `provider_crd_get_terraform_docs` may return
only a GitHub `repository`, immutable or versioned `ref`, and `path`. A connected
GitHub integration may fetch those exact returned locations.

This is a narrow source-following exception, not permission for independent
GitHub research:

- Fetch only the repository, ref, and path returned by the MCP tool.
- Do not broaden the search to adjacent files, branches, issues, pull requests,
  or repository-wide code search unless the user explicitly requests source
  investigation beyond the MCP result.
- Do not replace the returned ref with `main`, `master`, or another version.
- Treat a missing returned file as incomplete provider evidence and report it.
- Preserve the returned location in the final answer so the evidence remains
  traceable.

The Terraform documentation tool establishes the Crossplane-to-Terraform
resource mapping from provider source. Do not infer Terraform resource names by
converting the CRD kind or API group yourself.

## Evidence boundaries

Treat the OKF bundle and the provider tools exposed by the same MCP server as
the exclusive external retrieval sources for covered Crossplane ecosystem
content. Local project files and materials supplied by the user may still be
inspected.

Do not supplement, verify, or replace bundle results with generic documentation
or library retrieval tools. The only external source fetch allowed by this
skill is an exact GitHub location returned by
`provider_crd_get_examples` or `provider_crd_get_terraform_docs`.

Preserve cited versions, feature states, limitations, CRD API versions, and
original source locations. Do not introduce Crossplane v1 Claims unless
explicitly requested.

When the bundle or provider tools do not contain enough information, state that
the available OKF knowledge is incomplete and identify what is missing. Do not
silently switch to another retrieval source or guess a provider schema,
example path, or Terraform mapping.

When the OKF MCP server or required tools are unavailable, report that
dependency as unavailable and stop the Crossplane-specific retrieval workflow.
Do not fall back to web search, `curl`, arbitrary raw GitHub URLs, `gh`,
Context7, or another documentation source to retrieve Crossplane material.
Local project files and user-supplied material remain in scope.
