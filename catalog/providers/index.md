# Provider Model

* [Provider implementation families and selection](provider-landscape.md) - Distinguish Upjet-generated, AWS Go-codegen, and bespoke provider APIs without inferring support from a repository name.
* [Provider families and modern managed-resource groups](provider-families.md) - Identify AWS family packages from pinned metadata and distinguish modern namespaced `.m.` groups from legacy cluster-scoped APIs.
* [Upjet Terraform provenance](upjet-terraform-provenance.md) - Use a selected provider Makefile, resource configuration, and generated CRD before adapting version-matched Terraform documentation examples.
* [Provider connection-detail source retrieval](provider-connection-details-source-retrieval.md) - Read a selected-release provider's connection-detail implementation to determine Secret keys, conditionality, and dynamic-key boundaries.
* [Provider package revisions and activation scope](provider-package-revisions.md) - Plan upgrades with the parent-scoped active-revision boundary and cluster-wide API/controller effects in view.
* [Provider CRD schema discovery](crd-schema-discovery.md) - Find provider schemas through version-addressed registry routes or pinned package CRD directories.
