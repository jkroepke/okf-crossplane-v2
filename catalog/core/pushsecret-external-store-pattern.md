---
type: pattern
title: Push platform-team Secrets to external stores
description: An Alpha External Secrets Operator pattern for pushing selected Kubernetes Secret data to configured external secret stores.
resource: https://external-secrets.io/latest/api/pushsecret/
tags: [crossplane, platform, secrets, external-secrets-operator, pushsecret]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: pushsecret-crd-scope-served-api-version-and-purpose
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/config/crds/bases/external-secrets.io_pushsecrets.yaml#L8-L36'
    title: 'PushSecret CRD scope, served API version, and purpose'
  - id: pushsecret-documented-selection-per-key-bulk-and-templating-capabilities
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/api/pushsecret.md#L3-L8'
    title: 'PushSecret documented selection, per-key, bulk, and templating capabilities'
  - id: same-namespace-source-secret-and-selector-types
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/apis/externalsecrets/v1alpha1/pushsecret_types.go#L124-L149'
    title: 'Same-namespace source Secret and selector types'
  - id: explicit-mappings-bulk-store-validation-and-key-conversion
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/apis/externalsecrets/v1alpha1/pushsecret_types.go#L172-L256'
    title: 'Explicit mappings, bulk-store validation, and key conversion'
  - id: update-and-deletion-policy-guidance
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/guides/pushsecrets.md#L2-L6'
    title: 'Update and deletion policy guidance'
  - id: vault-pushsecret-example
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/snippets/vault-pushsecret.yaml#L10-L32'
    title: 'Vault PushSecret example'
  - id: aws-secrets-manager-oriented-metadata-example
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/snippets/aws-sm-push-secret-with-metadata.yaml#L1-L29'
    title: 'AWS Secrets Manager-oriented metadata example'
  - id: bulk-pushsecret-datato-documentation
    resource: 'https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/api/pushsecret.md#L30-L84'
    title: 'Bulk PushSecret dataTo documentation'
  - id: crossplane-v2-3-aggregate-secret-starts-with-empty-data
    resource: 'https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/manifests/guides/connection-details-composition/composition-go-templating.yaml#L53-L67'
    title: 'Crossplane v2.3 aggregate Secret starts with empty data'
source_repository: external-secrets/external-secrets
source_tag: v2.7.0
source_commit: e215053f3e68504de7483f9542b49f19f98293a1
source_paths:
  - config/crds/bases/external-secrets.io_pushsecrets.yaml
  - apis/externalsecrets/v1alpha1/pushsecret_types.go
  - docs/api/pushsecret.md
  - docs/guides/pushsecrets.md
  - docs/snippets/vault-pushsecret.yaml
  - docs/snippets/aws-sm-push-secret-with-metadata.yaml
source_role: supporting
documentation_repository: crossplane/docs
documentation_series: v2.3
documentation_commit: f1315464e35d40d25a28e4c15b6725b0e21adf91
documentation_paths:
  - content/v2.3/manifests/guides/connection-details-composition/composition-go-templating.yaml
feature_state: Alpha
---

# Overview

Platform teams can use External Secrets Operator (ESO) `PushSecret` to publish
selected data from a Kubernetes `Secret` to an external secret provider through
a configured `SecretStore` or `ClusterSecretStore`. This is an ESO pattern, not
a Crossplane feature or recommendation.[^pushsecret-crd-scope-served-api-version-and-purpose][^pushsecret-documented-selection-per-key-bulk-and-templating-capabilities]

`PushSecret` is namespaced and served as `external-secrets.io/v1alpha1`, so this
pattern is Alpha. A source `Secret` selected by name must be in the same
namespace as the `PushSecret`.[^pushsecret-crd-scope-served-api-version-and-purpose][^same-namespace-source-secret-and-selector-types]

# Pattern

1. Configure the target provider and authentication as an ESO `SecretStore` or
   `ClusterSecretStore`. Its provider-specific authentication, authorization,
   and metadata are outside this pattern.
2. Let the team own the source Kubernetes `Secret` and a same-namespace
   `PushSecret`.
3. Use `data` for explicit source-key to remote-key mappings. Use `dataTo` only
   when bulk selection and key rewriting are needed; every `dataTo` entry must
   identify a target store by name or label selector.[^pushsecret-documented-selection-per-key-bulk-and-templating-capabilities][^explicit-mappings-bulk-store-validation-and-key-conversion]
4. Choose lifecycle behavior deliberately. `Replace` is the default and
   overwrites an existing provider value. `IfNotExists` avoids overwrite, but
   can leave the cluster and provider values different. Provider data remains
   after deleting `PushSecret` unless `deletionPolicy: Delete` is set.[^update-and-deletion-policy-guidance]

Before publishing a Crossplane-produced aggregate Secret, establish that its
required keys are present. The aggregate pattern deliberately permits an empty
Secret during initial reconciliation; `PushSecret` selection does not prove
that every mapped key is available.[^crossplane-v2-3-aggregate-secret-starts-with-empty-data] The selected ESO sources do not establish
the exact reconciliation result for an absent source key, so this catalog does
not guess it. Gate publication or application readiness using the Crossplane
connection-data contract first.

This authored starter manifest maps two keys to a Vault-configured
`SecretStore`; it is not copied from the ESO source.

```yaml
apiVersion: external-secrets.io/v1alpha1
kind: PushSecret
metadata:
  name: team-service-credentials
  namespace: team-a
spec:
  secretStoreRefs:
    - name: team-a-vault
      kind: SecretStore
  selector:
    secret:
      name: service-credentials
  data:
    - match:
        secretKey: username
        remoteRef:
          remoteKey: teams/team-a/service
          property: username
    - match:
        secretKey: password
        remoteRef:
          remoteKey: teams/team-a/service
          property: password
```

# Provider examples

ESO's v2.7.0 documentation includes a Vault `SecretStore` example with
per-key remote mappings. Its AWS Secrets Manager-oriented example shows that
`data` entries can carry provider-specific metadata such as a KMS key,
format, description, and tags.[^vault-pushsecret-example][^aws-secrets-manager-oriented-metadata-example] Those fields must be evaluated against
the selected provider's ESO documentation and access policy.

# Limitations

- Use ESO's exact names: `SecretStore` and `ClusterSecretStore`, rather than
  the imprecise phrase “Cloud Provider SecretsStore”.
- This pattern makes the selected Kubernetes Secret data available to the
  chosen external provider. Scope ESO and provider credentials, store access,
  and team RBAC accordingly.
- `dataTo` applies conversion before matching and rewriting, defaults to
  `None`, and its metadata is provider-specific.[^explicit-mappings-bulk-store-validation-and-key-conversion][^bulk-pushsecret-datato-documentation]
- ESO is a supporting source here. It does not establish Crossplane API
  behavior, compatibility, or security guarantees.

# Relationships

The source Secret can be a normal composed Kubernetes Secret, such as the
connection-details aggregate described in
[Compose connection details with function-go-templating](../functions/function-go-templating/connection-details.md).
That Crossplane pattern determines how the Secret is composed; ESO determines
whether and how selected data is later published to an external store.
Use [safe status and connection publication](../functions/function-go-templating/patterns/safe-status-and-connection-publication.md)
when key completeness gates the consumer contract.

[^pushsecret-crd-scope-served-api-version-and-purpose]: [PushSecret CRD scope, served API version, and purpose](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/config/crds/bases/external-secrets.io_pushsecrets.yaml#L8-L36)
[^pushsecret-documented-selection-per-key-bulk-and-templating-capabilities]: [PushSecret documented selection, per-key, bulk, and templating capabilities](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/api/pushsecret.md#L3-L8)
[^same-namespace-source-secret-and-selector-types]: [Same-namespace source Secret and selector types](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/apis/externalsecrets/v1alpha1/pushsecret_types.go#L124-L149)
[^explicit-mappings-bulk-store-validation-and-key-conversion]: [Explicit mappings, bulk-store validation, and key conversion](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/apis/externalsecrets/v1alpha1/pushsecret_types.go#L172-L256)
[^update-and-deletion-policy-guidance]: [Update and deletion policy guidance](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/guides/pushsecrets.md#L2-L6)
[^vault-pushsecret-example]: [Vault PushSecret example](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/snippets/vault-pushsecret.yaml#L10-L32)
[^aws-secrets-manager-oriented-metadata-example]: [AWS Secrets Manager-oriented metadata example](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/snippets/aws-sm-push-secret-with-metadata.yaml#L1-L29)
[^bulk-pushsecret-datato-documentation]: [Bulk PushSecret `dataTo` documentation](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/api/pushsecret.md#L30-L84)
[^crossplane-v2-3-aggregate-secret-starts-with-empty-data]: [Crossplane v2.3 aggregate Secret starts with empty data](https://github.com/crossplane/docs/blob/f1315464e35d40d25a28e4c15b6725b0e21adf91/content/v2.3/manifests/guides/connection-details-composition/composition-go-templating.yaml#L53-L67)
