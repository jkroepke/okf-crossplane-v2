---
type: example
title: Provider-backed external queries in function-go-templating
description: Query external APIs through a provider-opentofu Workspace and consume its observed outputs in a later Go-template reconciliation.
resource: https://github.com/crossplane/crossplane/issues/4141
tags: [crossplane, composition-function, function-go-templating, provider-opentofu, multitenancy]
timestamp: 2026-07-14T00:00:00Z
source_repository: upbound/provider-opentofu
source_tag: v1.1.4
source_commit: 6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609
research_timestamp: 2026-07-14
feature_state: Beta
feature_state_basis: The namespaced provider-opentofu Workspace and function-go-templating input APIs used by the pattern are served as v1beta1.
---

# Problem

Crossplane issue #4141 reports that an observe-only managed resource still
models one external object identified by a unique external identifier; it does
not provide a general query by tags or properties. Zero, multiple, or changing
matches do not naturally fit that one-to-one relationship. The open issue
discusses query functions, provider data sources, required resources, and a
provider-integrated query API as alternatives, but does not establish that a
general query facility shipped in Crossplane v2.3.3.[1]

# Multi-tenant credential boundary

Crossplane v2.3.3 supports credentials on a Composition pipeline step, but each
Secret name and namespace is a literal value in the Composition. The controller
reads that exact Secret and passes its data to the function. It does not resolve
the reference from XR fields or pipeline context.[2][3]

Issue #7343 therefore reports a narrower gap than “Functions have no
credentials”: a function using one statically referenced Secret or one pod
identity cannot by that mechanism select different credentials for each XR or
tenant. The open issue proposes dynamic credential references and describes a
two-pass required-resource workaround. It does not prove that every custom
query function—or `upbound/function-azresourcegraph` in every configuration—
fails in a multi-tenant deployment.[4]

A provider-backed query can be useful when tenant credential selection already
uses ProviderConfig. Unlike the static Function credential reference described
above, each Workspace selects a ProviderConfig. In the user-reported design,
each tenant has its own namespace, the Workspace references a namespaced
ProviderConfig in that namespace, and only tenant-level credentials are exposed
through that configuration. This keeps cloud authentication and external
querying in a managed resource while function-go-templating only renders and
observes the Kubernetes object. The selected provider implementation resolves
a namespaced ProviderConfig in the Workspace namespace and forces that
configuration's credential Secret references into the same namespace.[5][12][13]
With the namespace and RBAC assumptions below, this avoids the static
per-Composition Function Secret reference for this query path.

# Pattern

provider-opentofu v1.1.4 serves the namespaced
`opentofu.m.upbound.io/v1beta1` `Workspace`. An inline Workspace accepts OpenTofu
module text and a typed `providerConfigRef`. Non-sensitive outputs are published
in the arbitrary JSON map `status.atProvider.outputs`; sensitive outputs belong
in the connection Secret instead. The Go-template pipeline input used here is
also served as `gotemplating.fn.crossplane.io/v1beta1`.[5][6][14]

The provider's upstream observe-only example uses an AWS data source, patches a
Workspace output to XR status, then patches that status into another managed
resource. The following is an adapted, user-reported variant that keeps the
rendering in function-go-templating and queries an AWS IAM Identity Center
administrator role. It has not been independently executed against the pinned
releases. The snippet was supplied by the user and is not copied from the
upstream example.[7]

```gotemplate
{{- $name := .observed.composite.resource.metadata.name }}
{{- $iamAdminRole := printf "role-iam-administrator-%s" $name }}
---
apiVersion: opentofu.m.upbound.io/v1beta1
kind: Workspace
metadata:
  annotations:
    {{ setResourceNameAnnotation $iamAdminRole }}
  name: {{ $iamAdminRole }}
spec:
  forProvider:
    source: Inline
    module: |-
      output "principal_arn" {
        value = one(data.aws_iam_roles.account_administrator_role.arns)
      }

      data "aws_iam_roles" "account_administrator_role" {
        name_regex  = "AWSReservedSSO_AccountAdministratorAccess_.*"
        path_prefix = "/aws-reserved/sso.amazonaws.com/"

        lifecycle {
          postcondition {
            condition = length(self.arns) == 1
            error_message = length(self.arns) == 0 ? "Could not find the AWS SSO administrator role ARN" : (
              "Found more than one AWS SSO administrator role ARN"
            )
          }
        }
      }
  providerConfigRef:
    kind: ProviderConfig
    name: opentofu
```

`setResourceNameAnnotation` makes the Workspace a named desired composed
resource. On a later reconciliation, retrieve the observed Workspace by the
same composition resource name and guard the normally absent first-observation
path before rendering a dependent field:[8][9]

```gotemplate
{{- $dataIAMAdminRole := getComposedResource . $iamAdminRole }}
{{- $principalArn := dig "status" "atProvider" "outputs" "principal_arn" "" ($dataIAMAdminRole | default (dict)) }}
{{- if $principalArn }}
principalArn: {{ $principalArn | quote }}
{{- end }}
```

Whether `principalArn` may be omitted until the output exists depends on the
downstream resource schema. The unguarded expression
`get $dataIAMAdminRole.status.atProvider.outputs "principal_arn"` can fail
before `get` runs when the Workspace or an intermediate status map is absent.

# Limitations

- The repeated `ProviderConfig` name `opentofu` refers to a distinct namespaced
  object in each tenant namespace. The isolation conclusion assumes that the
  Workspace is also created in that namespace and that Kubernetes RBAC and
  Secret access prevent cross-tenant configuration or credential use.
- The provider performs namespace-based lookup; it does not independently
  establish tenant authorization. Prevent unintended `ClusterProviderConfig`
  use and restrict who may create or change Workspaces, ProviderConfigs, and
  credential Secrets.
- ProviderConfig determines how the Workspace authenticates; this example does
  not prescribe a Secret layout or cloud authentication backend.
- Only non-sensitive outputs should be consumed from
  `status.atProvider.outputs`.[6]
- provider-opentofu warns that local state is not persisted, long-running
  modules can exceed the default timeout, and Workspace reconciliation can be
  CPU-intensive.[10]

# Licensing and attribution

provider-opentofu is Apache-2.0 licensed.[11] The upstream observe-only example
is summarized and cited rather than copied. The Go-template and OpenTofu module
above adapt material supplied directly by the user for this catalog change; no
external provenance for that material was identified.

# Project-history boundaries

Issues #4141 and #7343 were open and human-authored at the 2026-07-14 research
timestamp. No linked released change was found that resolves either report in
Crossplane v2.3.3. Bot and app activity was excluded; one GitHub Actions stale
comment on #4141 was omitted.

# Relationships

See [request data and context](../request-data.md) for observed resources and
credentials, and [rendered output](../rendered-output.md) for composition resource
names and readiness.

# Citations

[1] [Crossplane issue #4141](https://github.com/crossplane/crossplane/issues/4141)
[2] [Composition credential API](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/apiextensions/v1/composition_common.go#L75-L125)
[3] [Released Secret loading behavior](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/internal/controller/apiextensions/composite/composition_functions.go#L357-L375)
[4] [Crossplane issue #7343](https://github.com/crossplane/crossplane/issues/7343)
[5] [Workspace input and output types](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/apis/namespaced/v1beta1/workspace_types.go#L84-L187)
[6] [Workspace output publication](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/README.md#L22-L45)
[7] [Upstream observe-only data-source pattern](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/examples/cluster/observe-only-composition/composition.yaml#L12-L57)
[8] [Resource-name annotation helper](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103)
[9] [Observed composed-resource helper](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L124-L132)
[10] [provider-opentofu limitations](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/README.md#L120-L133)
[11] [provider-opentofu Apache-2.0 license](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/LICENSE)
[12] [Namespaced ProviderConfig resolution](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/internal/clients/client.go#L67-L107)
[13] [Credential Secret namespace enforcement](https://github.com/upbound/provider-opentofu/blob/6a1a4f3a3c174b4f6d91c84e74c4a5b6781b0609/internal/clients/client.go#L138-L147)
[14] [GoTemplate v1beta1 generated CRD](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L22)
