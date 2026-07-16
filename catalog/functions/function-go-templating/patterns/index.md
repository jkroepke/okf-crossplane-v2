# function-go-templating Patterns

* [Manual readiness](manual-readiness.md) - Mark a composed resource ready from an observed condition or guarded field check.
* [Non-composed-resource readiness](non-composed-resource-readiness.md) - Fetch a controller-created status object and translate it into composed-resource readiness.
* [Sveltos ClusterSummary deployment status](external-resource-readiness.md) - Observe a Profile's deterministic summary and require every expected feature in its copied configuration to be provisioned.
* [Safe database status and connection publication](safe-status-and-connection-publication.md) - Publish consumer-facing XR status and connection references only after named dependencies are ready.
* [provider-kubernetes Object readiness](provider-kubernetes-object-readiness.md) - Choose wrapper readiness deliberately and avoid using wrapper status as a durable Secret store.
* [Provider-backed external queries](provider-backed-external-query.md) - Query external APIs through a provider-opentofu Workspace and consume observed outputs safely.
* [YAML document boundaries](yaml-document-boundaries.md) - Preserve separators and field newlines when conditions change a rendered multi-document template.
