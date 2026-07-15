---
type: pattern
title: Push platform-team Secrets to external stores
description: An Alpha External Secrets Operator pattern for pushing selected Kubernetes Secret data to configured external secret stores.
resource: https://external-secrets.io/latest/api/pushsecret/
tags: [crossplane, platform, secrets, external-secrets-operator, pushsecret]
timestamp: 2026-07-16T00:00:00Z
source_repository: external-secrets/external-secrets
source_tag: v2.7.0
source_commit: e215053f3e68504de7483f9542b49f19f98293a1
source_role: supporting
feature_state: Alpha
---

# Overview

Platform teams can use External Secrets Operator (ESO) `PushSecret` to publish
selected data from a Kubernetes `Secret` to an external secret provider through
a configured `SecretStore` or `ClusterSecretStore`. This is an ESO pattern, not
a Crossplane feature or recommendation.[1][2]

`PushSecret` is namespaced and served as `external-secrets.io/v1alpha1`, so this
pattern is Alpha. A source `Secret` selected by name must be in the same
namespace as the `PushSecret`.[1][3]

# Pattern

1. Configure the target provider and authentication as an ESO `SecretStore` or
   `ClusterSecretStore`. Its provider-specific authentication, authorization,
   and metadata are outside this pattern.
2. Let the team own the source Kubernetes `Secret` and a same-namespace
   `PushSecret`.
3. Use `data` for explicit source-key to remote-key mappings. Use `dataTo` only
   when bulk selection and key rewriting are needed; every `dataTo` entry must
   identify a target store by name or label selector.[2][4]
4. Choose lifecycle behavior deliberately. `Replace` is the default and
   overwrites an existing provider value. `IfNotExists` avoids overwrite, but
   can leave the cluster and provider values different. Provider data remains
   after deleting `PushSecret` unless `deletionPolicy: Delete` is set.[5]

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
format, description, and tags.[6][7] Those fields must be evaluated against
the selected provider's ESO documentation and access policy.

# Limitations

- Use ESO's exact names: `SecretStore` and `ClusterSecretStore`, rather than
  the imprecise phrase “Cloud Provider SecretsStore”.
- This pattern makes the selected Kubernetes Secret data available to the
  chosen external provider. Scope ESO and provider credentials, store access,
  and team RBAC accordingly.
- `dataTo` applies conversion before matching and rewriting, defaults to
  `None`, and its metadata is provider-specific.[4][8]
- ESO is a supporting source here. It does not establish Crossplane API
  behavior, compatibility, or security guarantees.

# Relationships

The source Secret can be a normal composed Kubernetes Secret, such as the
connection-details aggregate described in
[Compose connection details with function-go-templating](../functions/function-go-templating/connection-details.md).
That Crossplane pattern determines how the Secret is composed; ESO determines
whether and how selected data is later published to an external store.

# Citations

[1] [PushSecret CRD scope, served API version, and purpose](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/config/crds/bases/external-secrets.io_pushsecrets.yaml#L8-L36)

[2] [PushSecret documented selection, per-key, bulk, and templating capabilities](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/api/pushsecret.md#L3-L8)

[3] [Same-namespace source Secret and selector types](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/apis/externalsecrets/v1alpha1/pushsecret_types.go#L124-L149)

[4] [Explicit mappings, bulk-store validation, and key conversion](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/apis/externalsecrets/v1alpha1/pushsecret_types.go#L172-L256)

[5] [Update and deletion policy guidance](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/guides/pushsecrets.md#L2-L6)

[6] [Vault PushSecret example](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/snippets/vault-pushsecret.yaml#L10-L32)

[7] [AWS Secrets Manager-oriented metadata example](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/snippets/aws-sm-push-secret-with-metadata.yaml#L1-L29)

[8] [Bulk PushSecret `dataTo` documentation](https://github.com/external-secrets/external-secrets/blob/e215053f3e68504de7483f9542b49f19f98293a1/docs/api/pushsecret.md#L30-L84)
