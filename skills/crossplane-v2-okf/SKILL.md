---
name: crossplane-v2-okf
description: Use the Crossplane v2 OKF MCP server as the exclusive external knowledge source for Crossplane v2 core, API, Composition, provider, function, runtime, Upjet, security, multi-tenancy, and example facts. For an external service's behavior or security guidance, use its primary vendor documentation as defined by the evidence boundary.
---

# Crossplane v2 OKF

For every Crossplane v2 ecosystem question, use the OKF MCP tools before answering or creating artifacts.

## Workflow

1. Call `okf_list_bundles` and confirm the Crossplane v2 bundle is available.
2. Call `okf_context` with the user's focused question.
3. For building, authoring, designing, or substantially reviewing a Crossplane v2 Composition, retrieve **Develop a Crossplane v2 Composition** (`composition-developer-starter`) as the primary routing guide. Follow its links to required API, provider, function, security, readiness, identity, testing, and packaging concepts.
4. Use `okf_search` and `okf_get_concept` for exact concepts or API details; use `okf_related` or `okf_impact` only when relationships matter.

The Composition developer starter is a navigation route, not provider-specific evidence. Use the provider workflow below for concrete managed-resource schemas, examples, and upstream Terraform documentation.

## Provider-family packages

Before emitting a `pkg.crossplane.io/v1` `Provider`, retrieve provider-family guidance and determine whether the selected release is monolithic or split into family and service packages.

- A source repository is not necessarily an installable package: do not turn `crossplane-contrib/provider-upjet-aws` into `xpkg.upbound.io/crossplane-contrib/provider-upjet-aws` without selected-release package evidence.
- For a new AWS, Azure, or GCP Upjet composition that needs one service, select its service package. For example, an S3-only AWS composition uses `xpkg.upbound.io/upbound/provider-aws-s3:<version>`, not the deprecated AWS monolithic package. Resolve Azure and GCP identities from selected-release family evidence, never from an API group or service name. Each selected service package installs its shared family/config package through its declared dependency.
- Do not install a family/configuration package directly unless selected package documentation requires it. Do not install an unrelated family service merely to obtain a `ProviderConfig`.
- Check for an existing monolithic provider: family packages do not take over its resource endpoints. Require an explicit, resource-by-resource migration plan before changing that topology.
- If selected-release evidence does not identify the installable service package, stop and report the gap. Never infer it from a CRD group, Terraform resource, or source repository name.

## Versions

Use `get_versions(name)` before choosing a provider or function release unless the user or local project supplied an exact version. Pass a short name, `account/package`, or full `xpkg.upbound.io` reference. Prefer `latest` (the tool's highest stable semantic version), never the latest prerelease. Preserve the resolved name and version in later calls and the answer; honor supplied pins without silently upgrading.

## Provider CRDs

For provider-specific resource questions, use this sequence and argument order. Preserve the resolved provider name and version throughout; never mix a CRD definition from one release with examples or Terraform documentation from another.

1. Discover candidates: `provider_crd_search(provider_name, provider_version, crd_search_term)`. Use a focused kind, API group, or wildcard; do not infer a resource from name similarity.
2. Select one and retrieve its schema: `provider_crd_get_definition(provider_name, provider_version, crd_name)`. Optionally use `path` (for example, `.spec` or `.spec.versions[0]`) when only a YAML subtree is needed; the tool returns that subtree.
3. For manifest creation or review, retrieve example locations: `provider_crd_get_examples(provider_name, provider_version, crd_name)`.
4. For an Upjet-managed resource, retrieve the mapped Terraform documentation with `provider_crd_get_terraform_docs(provider_name, provider_version, crd_name)` when field semantics, constraints, import behavior, or upstream examples matter.

`crd_name` may be a kind, `group/Kind`, `group/version/Kind`, or a YAML fragment containing `apiVersion` and `kind`. After discovery, prefer `group/version/Kind` to make the API explicit and avoid ambiguous kinds.

## Returned source locations

`provider_crd_get_examples` and `provider_crd_get_terraform_docs` may return only a GitHub `repository`, immutable or versioned `ref`, and `path`; a connected GitHub integration may fetch that exact location. This narrow exception does not allow independent GitHub research:

- Fetch only the returned repository, ref, and path; do not expand to adjacent files, branches, issues, pull requests, or repository-wide search unless the user explicitly requests source investigation beyond the MCP result.
- Do not substitute `main`, `master`, or another version for the returned ref. Treat a missing returned file as incomplete provider evidence and report it.
- Preserve the returned location in the final answer for traceability.

The Terraform documentation tool establishes the Crossplane-to-Terraform resource mapping from provider source. Never infer a Terraform resource name by converting a CRD kind or API group.

## Evidence boundaries

Treat the OKF bundle and its provider tools as the exclusive external retrieval sources for Crossplane-specific facts. Local project files and user-supplied material remain in scope. Do not supplement, verify, or replace a Crossplane API, Composition, provider-package, function, runtime, or CRD result with general documentation. The sole external fetch for a returned provider example or Terraform document is its exact GitHub location.

An external service configured by a Composition is a separate evidence domain. When its behavior materially affects the requested result—such as access controls, data retention, encryption, networking, billing, or service limits—use the service vendor's official documentation. Prefer the mapped Terraform documentation first when it answers the field-level question. Use vendor documentation to establish service behavior and recommended safeguards; never use it to infer Crossplane API shape, provider package identity, or a Terraform mapping. Cite service evidence separately and describe it as service guidance.

Preserve cited versions, feature states, limitations, CRD API versions, and original source locations. Do not introduce Crossplane v1 Claims unless explicitly requested. If the bundle or provider tools lack Crossplane information, say the available OKF knowledge is incomplete and identify the gap; do not guess a provider schema, example path, or Terraform mapping.

If the OKF MCP server or required tools are unavailable, report that dependency as unavailable and stop Crossplane-specific retrieval. This does not prevent use of primary vendor documentation for the independent external-service question, but do not use it as a substitute for missing Crossplane evidence.
