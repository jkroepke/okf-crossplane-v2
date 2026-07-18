---
type: Crossplane Provider
title: Retrieve Crossplane provider connection Secret keys from source
description: Determine a Crossplane managed resource's published Secret keys from its selected provider release rather than its destination-only CRD field.
tags: [crossplane, providers, upjet, provider-sql, connection-details, secrets]
timestamp: 2026-07-18T00:00:00Z
sources:
  - repository: crossplane-contrib/provider-upjet-azure
    commit: e0398bae1693e229c9060631e048b93177df6fa4
    paths: [config/cluster/sql/config.go, package/crds/sql.azure.upbound.io_mssqlservers.yaml]
  - repository: crossplane-contrib/provider-upjet-aws
    commit: 857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60
    paths: [config/cluster/efs/config.go, apis/cluster/efs/v1beta2/zz_filesystem_terraformed.go]
  - repository: crossplane-contrib/provider-sql
    commit: 0c8113bf3811a8b7d469d1dc88fed4f46ad5ec96
    paths: [pkg/clients/mssql/mssql.go, pkg/controller/cluster/mssql/user/reconciler.go]
  - repository: crossplane/crossplane-runtime
    commit: 9711defba79c6128064740b18b38a4991a0e9db2
    paths: [pkg/reconciler/managed/reconciler.go, apis/common/v1/resource.go]
  - repository: crossplane/crossplane-runtime
    commit: 504c43e478d7364d73a1834ba277e3a9f94b8e0a
    paths: [apis/common/v1/resource.go]
feature_state: Not stated by selected sources
feature_state_basis: This is unlabelled provider implementation behavior; individual managed-resource APIs retain the maturity of their own served versions.
---

# Overview

`spec.writeConnectionSecretToRef` selects where a Crossplane managed resource
writes provider connection details. It does not define the resource-specific
keys or guarantee that every possible key is present.[1][2] Retrieve the
selected Crossplane provider release's resource-specific implementation. Do not
infer keys from `status.atProvider`, Terraform attribute names, or a similarly
named managed resource.

# Retrieval procedure

1. Pin the installed provider package release to an immutable commit and select
   the exact managed-resource group, version, kind, and scope.
2. Identify the implementation path that creates or returns connection details
   for that exact resource; do not infer it from the kind name.
3. For an Upjet-based Crossplane provider, prove the Terraform resource mapping
   from generated resource metadata or the generated controller, then locate
   the service configuration, commonly
   `config/<scope>/<service>/config.go`, and find
   `AddResourceConfigurator("<terraform-resource>", ...)` for that proven
   mapping.
4. In that Upjet configuration, read the assigned
   `r.Sensitive.AdditionalConnectionDetailsFn`. In another Crossplane provider,
   trace the resource's `managed.ConnectionDetails` return value to the
   reconciler or connection publisher that receives it.
5. Record literal keys, conditional keys, dynamic key templates, source
   attributes, and errors separately. A dynamic `fmt.Sprintf` key is a runtime
   key family, not a finite static schema.

The Upjet config-file location is a convention, not a universal Crossplane
provider API. If the relevant implementation is absent, do not conclude that
the resource publishes no details: report the selected source location as
unresolved and inspect the provider's resource-specific code path.

# Selected-release examples

| Crossplane managed resource and mapping | Provider function result | Connection Secret consequence |
| --- | --- | --- |
| AWS cluster `efs.aws.upbound.io/v1beta2` `FileSystem` → `aws_efs_file_system` | The configurator assigns an inline `AdditionalConnectionDetailsFn`. When Terraform attribute `id` is a string, it adds the literal `id` key; otherwise it returns no such entry.[3][4] | The destination Secret can contain `data.id` with the EFS file-system ID. Do not assume other EFS resources use this key. |
| Azure cluster `sql.azure.upbound.io/v1beta2` `MSSQLServer` → `azurerm_mssql_server` | `msSQLConnectionDetails` requires `name`, `administrator_login`, and `fully_qualified_domain_name`; it returns `username` as `<administrator_login>@<name>` and `endpoint` as the FQDN. It adds `password` only when `administrator_login_password` is available.[5][6] | Treat `username` and `endpoint` as function-required output values; treat `password` as conditional rather than promising a fixed three-key Secret. |
| provider-sql cluster `mssql.sql.crossplane.io/v1alpha1` `User` | The MSSQL client returns `managed.ConnectionDetails` with `username`, `password`, `endpoint`, and `port`. The User reconciler passes that map as `ExternalCreation.ConnectionDetails` during creation and password update; the runtime publishes supplied connection details additively.[8][9] | The Secret data contract has those four keys for this code path. The `User` API is Alpha because the served API is `v1alpha1`; do not transfer that state to the provider implementation pattern.[10] |

The Azure example uses Crossplane runtime constants for the literal key names
`endpoint`, `username`, and `password`.[6] The EFS function uses its own
literal `id` key.[3] provider-sql uses the runtime constants for `username`,
`password`, `endpoint`, and `port` in its typed `managed.ConnectionDetails`
return value.[8]

# Limitations

This procedure establishes a provider-release implementation contract, not a
Crossplane-wide Secret schema. The resulting bytes can be conditional,
transformed, or absent because their source Terraform attributes are absent or
because the function returns an error. Examples that configure an input Secret
reference are not examples of `writeConnectionSecretToRef` output.[7] A typed
`managed.ConnectionDetails` return value is not itself proof of publication;
trace the selected resource's hand-off to its connection publisher.[9]

# Relationships

Use this procedure after [managed-resource references and ProviderConfig](../core/managed-resource-references-and-provider-config.md) establishes the generic destination boundary. Use [Upjet Terraform provenance](upjet-terraform-provenance.md) to prove a resource-to-Terraform mapping before interpreting provider configuration.

# Citations

[1] [Crossplane v2.3 connection Secret guidance](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/managed-resources/managed-resources.md#L453-L504)

[2] [Azure MSSQLServer CRD destination-reference schema](https://github.com/crossplane-contrib/provider-upjet-azure/blob/e0398bae1693e229c9060631e048b93177df6fa4/package/crds/sql.azure.upbound.io_mssqlservers.yaml#L2750-L2766)

[3] [AWS EFS FileSystem connection-details configurator](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/config/cluster/efs/config.go#L48-L63)

[4] [AWS EFS FileSystem Terraform-resource mapping](https://github.com/crossplane-contrib/provider-upjet-aws/blob/857b535dd0eb9b8242ad9d7c4e54aaa3e4616d60/apis/cluster/efs/v1beta2/zz_filesystem_terraformed.go#L17-L25)

[5] [Azure MSSQLServer Terraform mapping and connection-details assignment](https://github.com/crossplane-contrib/provider-upjet-azure/blob/e0398bae1693e229c9060631e048b93177df6fa4/apis/cluster/sql/v1beta2/zz_mssqlserver_terraformed.go#L17-L25) and [configurator](https://github.com/crossplane-contrib/provider-upjet-azure/blob/e0398bae1693e229c9060631e048b93177df6fa4/config/cluster/sql/config.go#L46-L50)

[6] [Azure MSSQLServer connection-detail function](https://github.com/crossplane-contrib/provider-upjet-azure/blob/e0398bae1693e229c9060631e048b93177df6fa4/config/cluster/sql/config.go#L18-L43) and [runtime key constants](https://github.com/crossplane/crossplane-runtime/blob/504c43e478d7364d73a1834ba277e3a9f94b8e0a/apis/common/v1/resource.go#L25-L43)

[7] [Generated Azure MSSQLServer input Secret-reference example](https://github.com/crossplane-contrib/provider-upjet-azure/blob/e0398bae1693e229c9060631e048b93177df6fa4/examples-generated/cluster/sql/v1beta2/mssqlserver.yaml#L5-L34)

[8] [provider-sql MSSQL typed connection details](https://github.com/crossplane-contrib/provider-sql/blob/0c8113bf3811a8b7d469d1dc88fed4f46ad5ec96/pkg/clients/mssql/mssql.go#L112-L120), [runtime map type](https://github.com/crossplane/crossplane-runtime/blob/9711defba79c6128064740b18b38a4991a0e9db2/pkg/reconciler/managed/reconciler.go#L142-L144), and [runtime key constants](https://github.com/crossplane/crossplane-runtime/blob/9711defba79c6128064740b18b38a4991a0e9db2/apis/common/v1/resource.go#L25-L33)

[9] [provider-sql MSSQL User creation hand-off](https://github.com/crossplane-contrib/provider-sql/blob/0c8113bf3811a8b7d469d1dc88fed4f46ad5ec96/pkg/controller/cluster/mssql/user/reconciler.go#L221-L223), [password-update hand-off](https://github.com/crossplane-contrib/provider-sql/blob/0c8113bf3811a8b7d469d1dc88fed4f46ad5ec96/pkg/controller/cluster/mssql/user/reconciler.go#L226-L253), [runtime publisher interface](https://github.com/crossplane/crossplane-runtime/blob/9711defba79c6128064740b18b38a4991a0e9db2/pkg/reconciler/managed/reconciler.go#L151-L161), [create publication](https://github.com/crossplane/crossplane-runtime/blob/9711defba79c6128064740b18b38a4991a0e9db2/pkg/reconciler/managed/reconciler.go#L1386), and [update publication](https://github.com/crossplane/crossplane-runtime/blob/9711defba79c6128064740b18b38a4991a0e9db2/pkg/reconciler/managed/reconciler.go#L1490)

[10] [provider-sql MSSQL User v1alpha1 API](https://github.com/crossplane-contrib/provider-sql/blob/0c8113bf3811a8b7d469d1dc88fed4f46ad5ec96/apis/cluster/mssql/v1alpha1/register.go#L26-L30) and [managed-resource markers](https://github.com/crossplane-contrib/provider-sql/blob/0c8113bf3811a8b7d469d1dc88fed4f46ad5ec96/apis/cluster/mssql/v1alpha1/user_types.go#L72-L85)
