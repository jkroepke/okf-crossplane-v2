# function-go-templating Patterns

* [Manual readiness](manual-readiness.md) - Mark a composed resource ready from an observed condition or guarded field check.
* [Non-composed-resource readiness](non-composed-resource-readiness.md) - Fetch a controller-created status object and translate it into composed-resource readiness.
* [Sveltos ClusterSummary deployment status](external-resource-readiness.md) - Observe a Profile's deterministic summary and require every expected feature in its copied configuration to be provisioned.
* [Provider-backed external queries](provider-backed-external-query.md) - Query external APIs through a provider-opentofu Workspace and consume observed outputs safely.
