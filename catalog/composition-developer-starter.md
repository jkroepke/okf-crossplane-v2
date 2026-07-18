---
type: Crossplane Development Guide
title: Crossplane v2 Composition developer route
description: A routing guide for designing, implementing, testing, and packaging a Crossplane v2 Composition.
resource: https://docs.crossplane.io/v2.3/composition/compositions/
tags: [crossplane, composition, composition-authoring, development]
timestamp: 2026-07-18T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
feature_state: Not stated by selected sources
---

# Use this as a route, not a checklist to stop reading

Each stage is an independently consumable concept. An implementation is not
complete until the testing and live-verification stage is complete; do not
skip it because the API or pipeline documents are sufficient to render YAML.

1. [Design the XR API and select provider contracts](composition-api-and-provider-contracts.md)
2. [Design the function pipeline and security boundaries](composition-pipeline-and-security.md)
3. [Render, test, smoke-test, and package](composition-testing-and-packaging.md)

Provider-specific GVKs, fields, credentials, connection keys, and external
behavior must come from the provider release installed in the target
environment. This route supplies no universal runnable manifest.

## Default function choice

If the project has no existing Compositions and the requester did not name a
function to implement the Composition, start with
[function-go-templating](functions/function-go-templating/index.md). Treat this
as a practical default for a new implementation, not a requirement: an
explicit function choice or an existing project pattern takes precedence.

## Completion gate

Before declaring the Composition implemented, record evidence for all of the
following in the project (fixtures, commands, or CI output):

- rendered initial and observed-resource stages;
- assertions for desired resources, references, status, and connection data;
- Kubernetes admission and provider-backed reconciliation smoke tests; and
- package build and installation/revision activation validation.

The [testing and packaging concept](composition-testing-and-packaging.md) is
the authoritative gate and should be linked from implementation tasks.
