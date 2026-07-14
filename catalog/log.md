---
type: log
title: crossplane-catalog-update-log
description: Chronological record of high-level Crossplane catalog updates.
timestamp: 2026-07-12T00:00:00Z
---

# Catalog Update Log

## 2026-07-14
* **Creation**: Added Crossplane Core Usage and ClusterUsage deletion protection, scope semantics, and current mixed namespace/cluster limitations.
* **Creation**: Added a release-pinned function-auto-ready v0.7.0 knowledge set covering package use, readiness ordering, Kubernetes health checks, Beta input, and Alpha CEL customizations.
* **Creation**: Added the Crossplane v2 function-go-templating pattern for aggregating observed connection details into an explicitly composed Kubernetes Secret.
* **Update**: Documented function-go-templating Context semantics and the Crossplane v2 compatibility boundary of all special meta kinds.
* **Update**: Documented exact function-go-templating helper semantics and added a dedicated ExtraResources capability reference.

## 2026-07-12
* **Update**: Expanded provider-agnostic Managed Resource knowledge with anatomy, reconciliation lifecycle, policies, identity safety, references, ProviderConfig, controls, conditions, and MR activation APIs.
* **Creation**: Added the two-role Crossplane Functions model, distinguishing composition functions from Alpha operation functions and documenting direct, scheduled, and watched invocation.
* **Creation**: Added a v2.3.3-pinned summary of the Composition Functions specification, explicitly separated from operation functions.
* **Creation**: Added Crossplane Configuration package concepts covering package contents, installation, revisions, dependencies, and authoring metadata.
* **Creation**: Established a Crossplane Core v2.3.3 foundation covering composite resources, XRDs, Composition pipelines, managed resources, and MRDs.
* **Creation**: Added a legacy-free, release-pinned function-go-templating v0.12.2 knowledge set with schema, behavior, helper, Sprig, and project-history concepts.
