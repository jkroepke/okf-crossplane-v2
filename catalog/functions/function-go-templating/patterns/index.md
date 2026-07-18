# function-go-templating Patterns

When a Composition task spans multiple patterns, start with the
[pipeline and security design route](../../../composition-pipeline-and-security.md).
The leaf concepts remain separate because readiness evaluation, consumer
publication, and desired-resource introduction change different state.

# Readiness evaluation

* [Manual readiness](manual-readiness.md) - Mark a composed resource ready from an observed condition or guarded field check.
* [function-auto-ready](../../function-auto-ready/readiness.md) - Derive readiness from the matched observed composed resource with optional Alpha CEL, built-in, and generic condition checks.
* [Non-composed-resource readiness](non-composed-resource-readiness.md) - Fetch a controller-created status object and translate it into composed-resource readiness.
* [provider-kubernetes Object readiness](provider-kubernetes-object-readiness.md) - Choose wrapper readiness deliberately and avoid using wrapper status as a durable Secret store.

# Product-specific readiness examples

* [Sveltos ClusterSummary deployment status](sveltos-clustersummary-readiness.md) - Specialize non-composed-resource readiness for a Profile's deterministic summary and require every expected feature in its copied configuration to be provisioned.

# Consumer publication

* [Safe database status and connection publication](safe-status-and-connection-publication.md) - Publish consumer-facing XR status and connection references only after named dependencies are ready and required data is complete.

# Desired-resource introduction

* [Readiness-gated staging](readiness-gated-staging.md) - Introduce one exceptional dependent stage after observed readiness, then retain it across later reconciliations.
* [function-sequencer](../../function-sequencer/sequencing.md) - Move a declared or branching introduction graph out of the template while retaining observed successors.

# External integration

* [Provider-backed external queries](provider-backed-external-query.md) - Query external APIs through a provider-opentofu Workspace and consume observed outputs safely.

# Template robustness

* [YAML document boundaries](yaml-document-boundaries.md) - Preserve separators and field newlines when conditions change a rendered multi-document template.
