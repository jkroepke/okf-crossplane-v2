---
type: Crossplane Composition Design Guide
title: Design the XR API and provider contracts
description: Define a versioned XRD contract and bind it to verified provider APIs before writing the pipeline.
tags: [crossplane, composition, xrd, providers, api-design]
timestamp: 2026-07-18T00:00:00Z
crossplane_release: v2.3.3
documentation_series: v2.3
feature_state: Not stated by selected sources
---

# Define the platform API

Start with the [composite resource model](core/composite-resource-model.md) and
define a current [CompositeResourceDefinition v2](core/composite-resource-definition.md).
Choose namespace scope deliberately, then apply [OpenAPI](core/xrd-openapi-schema.md),
[CEL validation](core/xrd-cel-validation.md), collection semantics, and
[tenant admission security](core/tenant-xr-api-security.md).

An XRD version needs `name`, `served`, and `referenceable`; exactly one served
version is referenceable. A Composition must target the generated XR GVK:

```yaml
spec:
  compositeTypeRef:
    apiVersion: <xrd.spec.group>/<referenceable-version.name>
    kind: <xrd.spec.names.kind>
```

Do not substitute an XRD or CRD name for these fields.

# Select concrete provider APIs

Use [provider implementation families and selection](providers/provider-landscape.md),
then inspect the exact installed [provider CRD schema](providers/crd-schema-discovery.md).
Record the Provider package, ProviderConfig, managed-resource GVKs, activation
requirements, credentials, connection-detail keys, and external-name behavior.
Never infer an Upjet mapping or compatibility from a similar resource name.

This concept deliberately stops before provider-specific manifests: those are
project inputs and must be tested against the selected provider release.

Continue with [pipeline and security design](composition-pipeline-and-security.md),
then complete the [testing and packaging gate](composition-testing-and-packaging.md).
