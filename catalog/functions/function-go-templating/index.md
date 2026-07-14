---
type: index
title: function-go-templating-index
description: Progressive index for function-go-templating release knowledge.
timestamp: 2026-07-14T00:00:00Z
---

# function-go-templating v0.12.2

* [Package and installation](package.md) - Install and reference the selected stable function package.
* [GoTemplate input](input.md) - Author Inline, FileSystem, or Environment input using the generated schema.
* [Environment template source](environment-source.md) - Load template text from the reserved EnvironmentConfig pipeline-context map.
* [Request data and context](request-data.md) - Read request state, extra resources, context, and credentials.
* [Context](context.md) - Read, create, and deeply update shared function-pipeline context.
* [ExtraResources](extra-resources.md) - Request cluster resources by name or labels and consume them directly or through pipeline context.
* [Manual readiness](manual-readiness.md) - Mark a composed resource ready from an observed condition or guarded field check.
* [Non-composed-resource readiness](non-composed-resource-readiness.md) - Fetch a controller-created status object and translate it into composed-resource readiness.
* [Sveltos ClusterSummary deployment status](external-resource-readiness.md) - Observe a Profile's deterministic summary and require every expected feature in its copied configuration to be provisioned.
* [Provider-backed external queries](provider-backed-external-query.md) - Query external APIs through a provider-opentofu Workspace and consume observed outputs safely.
* [Connection details](connection-details.md) - Aggregate observed connection details into an explicitly composed Kubernetes Secret for v2 composite resources.
* [Rendered output](rendered-output.md) - Name resources, report readiness, update status, and handle v2 connection details.
* [Template functions](template-functions.md) - Use project-specific helpers and understand the Sprig boundary.
* [Sprig v3.3.0](sprig.md) - Use the exact supporting function library exposed by this release.
* [Project history](project-history.md) - Distinguish included changes, reports, and post-release proposals.
