---
type: function
title: Function package
description: The shared cluster-scoped package API used to install composition-capable and operation-capable functions.
resource: https://docs.crossplane.io/v2.3/packages/functions/
tags: [crossplane, function-package, beta]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: function-identity-and-served-versions
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L7-L41'
    title: 'Function identity and served versions'
  - id: served-storage-flags
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L264-L289'
    title: 'served/storage flags'
  - id: package-field-and-validation
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L86-L96'
    title: 'Package field and validation'
  - id: documented-installation
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/functions.md#L25-L45'
    title: 'Documented installation'
  - id: lifecycle-fields-and-defaults
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L79-L167'
    title: 'Lifecycle fields and defaults'
  - id: printer-columns
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L20-L32'
    title: 'Printer columns'
  - id: status
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L171-L180'
    title: 'status'
  - id: operation-steps-reference-function-objects
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L68-L233'
    title: 'Operation steps reference Function objects'
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - cluster/crds/pkg.crossplane.io_functions.yaml
---

# Overview

`Function` is a cluster-scoped `pkg.crossplane.io` package API. Crossplane v2.3.3 serves `v1` as storage and also serves `v1beta1`; under this catalog's served-version ceiling, the API is **Beta**.[^function-identity-and-served-versions][^served-storage-flags]

Create a `Function` whose required `spec.package` is a fully qualified OCI image with a tag or digest. Composition and Operation pipeline steps then reference the installed object's name.[^package-field-and-validation][^documented-installation]

# Schema

Package lifecycle controls include pull secrets and policy, automatic or manual revision activation, revision history, Crossplane constraint and dependency controls, and runtime configuration. Defaults include 
`IfNotPresent`, automatic activation, one retained revision, constraint and dependency checks enabled, and runtime configuration named `default`.[^lifecycle-fields-and-defaults]

Status exposes conditions, the current revision, resolved package, and applied image configuration references. Printer columns surface Installed, Healthy, Package, and Age.[^printer-columns][^status]

# Limitations

The released CRD description calls this a package for “a new kind of composition function,” while released Operation APIs reference the same kind. This catalog preserves the broader capability model established by 
package metadata and the Operations documentation instead of treating that description as an API restriction.[^operation-steps-reference-function-objects]

[^function-identity-and-served-versions]: [Function identity and served versions](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L7-L41) and [served/storage flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L264-L289)
[^served-storage-flags]: [served/storage flags](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L264-L289)
[^package-field-and-validation]: [Package field and validation](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L86-L96)
[^documented-installation]: [Documented installation](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/packages/functions.md#L25-L45)
[^lifecycle-fields-and-defaults]: [Lifecycle fields and defaults](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L79-L167)
[^printer-columns]: [Printer columns](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L20-L32) and [status](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L171-L180)
[^status]: [status](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/pkg.crossplane.io_functions.yaml#L171-L180)
[^operation-steps-reference-function-objects]: [Operation steps reference Function objects](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/cluster/crds/ops.crossplane.io_operations.yaml#L68-L233)
