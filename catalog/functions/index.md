# Function Model

* [Crossplane Functions](overview.md) - Understand the two function roles and their shared package and protocol.
* [Function package](package.md) - Install a composition-capable or operation-capable function package.

# Composition Functions

* [Composition functions](composition-functions.md) - Continuously reconcile XRs through ordered Composition pipelines.
* [Composition Functions specification](composition-function-specification.md) - Normative contract for serving, desired state, packaging, and runtime assumptions.

* [function-environment-configs](function-environment-configs/) - Select and merge EnvironmentConfigs into pipeline context.
* [function-go-templating](function-go-templating/) - Render desired resources from Go templates in a composition pipeline.
* [function-auto-ready](function-auto-ready/) - Determine desired composed-resource readiness from observed resources.
* [EnvironmentConfig, Go templating, and readiness pipeline](environment-config-pipeline.md) - Order the three functions by their context and desired-resource dependencies.

# Operation Functions

* [Operation functions](operation-functions.md) - Run Alpha once-to-completion operational pipelines.
* [Scheduled and watched Operations](scheduled-and-watched-operations.md) - Trigger operation pipelines on schedules or resource changes.
