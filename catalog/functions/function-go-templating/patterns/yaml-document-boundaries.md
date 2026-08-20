---
type: Crossplane Example
title: Preserve YAML document boundaries in templates
description: Keep Go-template trim markers away from YAML document and field boundaries, then parse rendered output as YAML.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, go-template, yaml, rendering]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: inline-multi-manifest-template-guidance
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L52'
    title: 'Inline multi-manifest template guidance'
  - id: go-text-template-whitespace-trimming
    resource: 'https://github.com/golang/go/blob/28622c19591d95c9a83f706f2ed1b303d58da85f/src/text/template/doc.go#L39-L53'
    title: 'Go text/template whitespace trimming'
  - id: kubernetes-dns-label-length
    resource: 'https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/apimachinery/pkg/util/validation/validation.go#L158-L170'
    title: 'Kubernetes DNS label length'
  - id: sprig-dictionary-lookup
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L11-L48'
    title: 'Sprig dictionary lookup'
  - id: empty-value-defaults
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L5-L25'
    title: 'empty-value defaults'
  - id: go-template-comparison-rules
    resource: 'https://github.com/golang/go/blob/28622c19591d95c9a83f706f2ed1b303d58da85f/src/text/template/doc.go#L411-L441'
    title: 'Go-template comparison rules'
  - id: sprig-get-implementation
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/dict.go#L8-L27'
    title: 'Sprig get implementation'
  - id: reflection-helpers
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L12-L27'
    title: 'reflection helpers'
  - id: sprig-issue-53-nil-workaround-comment
    resource: 'https://github.com/Masterminds/sprig/issues/53#issuecomment-483414063'
    title: 'Sprig issue #53 nil-workaround comment'
  - id: yq-multi-document-eval-and-pretty-print-support
    resource: 'https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L350-L353'
    title: 'yq multi-document, eval, and pretty-print support'
  - id: cli-flags
    resource: 'https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L399-L402'
    title: 'CLI flags'
  - id: crossplane-cli-render-to-resource-validation-pipeline
    resource: 'https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/validate/help/validate.md#L61-L71'
    title: 'Crossplane CLI render-to-resource-validation pipeline'
  - id: current-cli-composition-render-command
    resource: 'https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L86-L99'
    title: 'Current CLI Composition render command'
  - id: historical-function-readme-render-example
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L149-L157'
    title: 'Historical function README render example'
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Beta
feature_state_basis: The generated GoTemplate input CRD serves and stores gotemplating.fn.crossplane.io/v1beta1.
project_history_researched_at: 2026-07-16T00:00:00Z
---

# Overview

An Inline `template` may contain one or more YAML documents.[^inline-multi-manifest-template-guidance] Go template
actions copy surrounding text verbatim by default, but `{{-` removes trailing
whitespace before an action and `-}}` removes leading whitespace after one.[^go-text-template-whitespace-trimming]
Consequently, trimming at a structural YAML boundary can join a `---` document
separator to adjacent YAML text. Treat this as an output-formatting hazard, not
a provider-reference problem.

# Safe field boundaries

When a conditional field follows a required field, preserve its
indentation and newline rather than using trim markers:

```gotemplate
spec:
  bucketName: {{ $spec.bucketName | quote }}
  {{ if $bucketArn }}
  bucketArn: {{ $bucketArn | quote }}
  {{ end }}
```

The examples are an inferred authoring pattern from the Go-template whitespace
rules; they are not a special `function-go-templating` syntax. Trim markers
remain useful on directive-only lines when removing whitespace cannot join YAML
syntax or values.

# Identifier and optional-input safety

When constructing an identifier for a DNS-label-limited field, reserve space
for the literal suffix before truncating the variable prefix. The length budget
is `63 - len(suffix)`: for example, `-bucket` leaves 56 characters and
`-public-access` leaves 49. Trim a trailing hyphen from the truncated prefix
before appending the suffix.[^kubernetes-dns-label-length]

```gotemplate
{{- $bucketResourceName := printf "%s-bucket" ($xr.metadata.name | trunc 56 | trimSuffix "-") -}}
{{- $publicAccessResourceName := printf "%s-public-access" ($xr.metadata.name | trunc 49 | trimSuffix "-") -}}
```

This is a size-safety pattern, not a uniqueness guarantee: two long composite
names sharing the retained prefix can still collide. Do not assume a
composition-resource-name annotation itself has a DNS-label limit unless the
particular consumer requires one.

Do not use `default` for an optional boolean when its fallback can be `true`.
Sprig considers `false` empty, so `get $spec "forceDestroy" | default true`
always produces `true` for both an absent value and an explicit `false`.[^sprig-dictionary-lookup][^empty-value-defaults]
For a map, test key presence and only then read the value:

```gotemplate
{{ if hasKey $spec "forceDestroy" }}
forceDestroy: {{ get $spec "forceDestroy" }}
{{ else }}
forceDestroy: true
{{ end }}
```

For a value that is genuinely `nil`, `kindIs "invalid" $value` is a common
template guard. Do not substitute `eq $value nil` or `ne $value nil`: template
comparisons require comparable types and can fail on heterogeneous values.[^go-template-comparison-rules]
This guard does not replace `hasKey` for a Sprig `get` result—`get` returns an
empty string for an absent map key, not an invalid value.[^sprig-get-implementation][^reflection-helpers] The `kindIs`
workaround was recorded by a human contributor in Sprig issue #53; treat that
comment as a historical workaround, while the selected release documentation
and code establish the current helper behavior.[^sprig-issue-53-nil-workaround-comment]

# Map indentation and formatting gate

Serialize a tags map at the indentation level of the YAML value, then make the
rendered output—not the template's visual indentation—the authority:

```gotemplate
tags:
  {{- get $spec "tags" | default (dict) | toYaml | nindent 10 }}
```

As an optional local gate after `crossplane composition render`, pipe the output to a
pinned `yq` `eval --prettyPrint '.' -` command. `yq` supports multi-document
YAML, so successful parse and reformatting provides a quick structural check;
still assert the expected documents and resource names separately.[^yq-multi-document-eval-and-pretty-print-support][^cli-flags]

Use the CLI command boundary deliberately: `crossplane composition render`
renders, while `crossplane resource validate` validates resources. There is no
`crossplane composition validate` command.[^crossplane-cli-render-to-resource-validation-pipeline]

The selected function-go-templating README still shows the historical
`crossplane beta render` spelling. Do not copy that invocation into a current
CLI workflow; the current CLI documents `crossplane composition render`.[^current-cli-composition-render-command][^historical-function-readme-render-example]

# Relationships

See [GoTemplate input](../input.md) for the Inline schema and
[rendered resources](../rendered-output.md) for the resource-name annotation
used to identify composed resources. The catalog's
[local Composition rendering guide](../../../cli/local-composition-rendering.md)
describes Crossplane CLI rendering prerequisites and observed-resource fixtures.

[^inline-multi-manifest-template-guidance]: [Inline multi-manifest template guidance](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L52)
[^go-text-template-whitespace-trimming]: [Go text/template whitespace trimming](https://github.com/golang/go/blob/28622c19591d95c9a83f706f2ed1b303d58da85f/src/text/template/doc.go#L39-L53)
[^kubernetes-dns-label-length]: [Kubernetes DNS label length](https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/apimachinery/pkg/util/validation/validation.go#L158-L170)
[^sprig-dictionary-lookup]: [Sprig dictionary lookup](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L11-L48) and [empty-value defaults](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L5-L25)
[^empty-value-defaults]: [empty-value defaults](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L5-L25)
[^go-template-comparison-rules]: [Go-template comparison rules](https://github.com/golang/go/blob/28622c19591d95c9a83f706f2ed1b303d58da85f/src/text/template/doc.go#L411-L441)
[^sprig-get-implementation]: [Sprig `get` implementation](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/dict.go#L8-L27) and [reflection helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L12-L27)
[^reflection-helpers]: [reflection helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L12-L27)
[^sprig-issue-53-nil-workaround-comment]: [Sprig issue #53 nil-workaround comment](https://github.com/Masterminds/sprig/issues/53#issuecomment-483414063), authored by a human contributor on 2019-04-15.
[^yq-multi-document-eval-and-pretty-print-support]: [yq multi-document, eval, and pretty-print support](https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L350-L353) and [CLI flags](https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L399-L402)
[^cli-flags]: [CLI flags](https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L399-L402)
[^crossplane-cli-render-to-resource-validation-pipeline]: [Crossplane CLI render-to-resource-validation pipeline](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/validate/help/validate.md#L61-L71)
[^current-cli-composition-render-command]: [Current CLI Composition render command](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/render/xr/help/render.md#L86-L99)
[^historical-function-readme-render-example]: [Historical function README render example](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L149-L157)
