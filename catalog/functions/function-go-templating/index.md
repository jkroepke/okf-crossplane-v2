# function-go-templating v0.12.2

# Package and input

* [Package and installation](package.md) - Install and reference the selected stable function package.
* [GoTemplate input](input.md) - Author Inline, FileSystem, or Environment input using the generated schema.
* [Environment template source](environment-source.md) - Load template text from the reserved EnvironmentConfig pipeline-context map.

# Rendering and request data

* [Request data and context](request-data.md) - Read request state, extra resources, context, and credentials.
* [Context](context.md) - Read, create, and deeply update shared function-pipeline context.
* [ExtraResources](extra-resources.md) - Request cluster resources by name or labels and consume them directly or through pipeline context.
* [Connection details](connection-details.md) - Aggregate observed connection details into an explicitly composed Kubernetes Secret for v2 composite resources.
* [Rendered output](rendered-output.md) - Name resources, report readiness, update status, and handle v2 connection details.

# Patterns and examples

* [Pattern decision routes](patterns/index.md) - Choose among readiness evaluation, consumer publication, desired-resource introduction, and external-integration patterns by outcome.

# Reference and history

* [Template functions](template-functions.md) - Use project-specific helpers and understand the Sprig boundary.
* [Sprig v3.3.0](sprig.md) - Use the exact supporting function library exposed by this release.
* [Project history](project-history.md) - Distinguish included changes, reports, and post-release proposals.
