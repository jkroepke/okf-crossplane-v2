---
type: Crossplane Composition Verification Guide
title: Test, smoke-test, and package a Composition
description: A mandatory verification gate covering rendering, assertions, admission, live reconciliation, and package activation.
tags: [crossplane, composition, testing, validation, packaging]
timestamp: 2026-07-18T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
feature_state: Not stated by selected sources
---

# Verification is part of implementation

Use the [reference project layout](core/composition-project-layout.md) to keep
XRD, Composition, example XR, Functions, provider setup, and fixtures distinct.
Render with the [Crossplane CLI](cli/local-composition-rendering.md) for both
the initial and observed-resource stages. Add [xprin assertion suites](tools/xprin-test-suites.md)
for repeatable checks of desired objects, logical keys, references, readiness,
status, and connection data.

Rendering is necessary but insufficient. It does not prove Kubernetes
admission, provider schemas, credentials, RBAC, external behavior, or live
reconciliation. Run a cluster-backed smoke test that applies the XRD,
Composition, Functions, and example XR, then observe provider and XR
conditions. Test failure and deletion paths where the pipeline does not run.

# Package only after tests pass

Use a [Configuration package](core/configurations/index.md) to distribute the
XRD, Composition, and dependencies only after API, provider, pipeline, and
fixtures agree. Validate package build, registry publication (if applicable),
revision activation, installation, and rollback/promotion procedure. Package
revision activation does not validate provider semantics.

## Evidence record

Attach commands or CI artifacts for rendering, assertions, admission, live
smoke testing, package build, and activation. If any item is unavailable, mark
the implementation incomplete and state the project-specific gap.
