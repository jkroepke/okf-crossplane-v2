---
type: Crossplane Example
title: Preserve YAML document boundaries in conditional templates
description: Keep Go-template trim markers away from YAML document and field boundaries, then render every reconciliation stage that changes conditional output.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, go-template, yaml, rendering]
timestamp: 2026-07-16T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Beta
feature_state_basis: The generated GoTemplate input CRD serves and stores gotemplating.fn.crossplane.io/v1beta1.
---

# Overview

An Inline `template` may contain one or more YAML documents.[1] Go template
actions copy surrounding text verbatim by default, but `{{-` removes trailing
whitespace before an action and `-}}` removes leading whitespace after one.[2]
Consequently, trimming at a structural YAML boundary can join a `---` document
separator to adjacent YAML text. Treat this as an output-formatting hazard, not
a provider-reference problem.

# Safe conditional boundaries

For a conditional whole document, leave the separator and the first YAML token
on distinct output lines. Use untrimmed actions around that boundary:

```gotemplate
{{ if $bucketReady }}
---
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: BucketACL
metadata:
  annotations:
    gotemplating.fn.crossplane.io/composition-resource-name: public-acl
{{ end }}
```

Likewise, when a conditional field follows a required field, preserve its
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

# Stage-oriented verification

Render at least the initial stage, where observed prerequisite values are
absent, and a fully observed stage, where every conditional document is
eligible. Check both rendered artifacts as YAML documents and verify the
expected composed-resource names and count. This catches a template that
executes successfully yet silently changes its YAML token boundaries when a
condition becomes true.

The motivating bucket, ownership, public-access, and ACL sequence was supplied
by the user. It is an illustrative composition pattern and was not
independently executed against the pinned releases.

# Identifier and optional-input safety

When constructing an identifier for a DNS-label-limited field, reserve space
for the literal suffix before truncating the variable prefix. The length budget
is `63 - len(suffix)`: for example, `-bucket` leaves 56 characters and
`-public-access` leaves 49. Trim a trailing hyphen from the truncated prefix
before appending the suffix.[3]

```gotemplate
{{- $bucketResourceName := printf "%s-bucket" ($xr.metadata.name | trunc 56 | trimSuffix "-") -}}
{{- $publicAccessResourceName := printf "%s-public-access" ($xr.metadata.name | trunc 49 | trimSuffix "-") -}}
```

This is a size-safety pattern, not a uniqueness guarantee: two long composite
names sharing the retained prefix can still collide. Do not assume a
composition-resource-name annotation itself has a DNS-label limit unless the
particular consumer requires one.

For optional map fields, use `get` before `default` so the fallback is applied
to an absent value without dot-field traversal:

```gotemplate
{{- $providerConfigRef := get $spec "providerConfigRef" | default (dict "kind" "ClusterProviderConfig" "name" "default") -}}
forceDestroy: {{ get $spec "forceDestroy" | default false }}
```

`default` treats `false` as empty. A field for which explicit `false` must be
distinguished from absent therefore needs a presence check rather than this
shortcut.[4]

# Map indentation and formatting gate

Serialize a tags map at the indentation level of the YAML value, then make the
rendered output—not the template's visual indentation—the authority:

```gotemplate
tags:
  {{- get $spec "tags" | default (dict) | toYaml | nindent 10 }}
```

As an optional local gate after `crossplane beta render`, pipe the output to a
pinned `yq` `eval --prettyPrint '.' -` command. `yq` supports multi-document
YAML, so successful parse and reformatting provides a quick structural check;
still assert the expected documents and resource names separately.[5]

Use the CLI command boundary deliberately: `crossplane composition render`
renders, while `crossplane resource validate` validates resources. There is no
`crossplane composition validate` command.[6]

# Relationships

See [GoTemplate input](../input.md) for the Inline schema and
[rendered resources](../rendered-output.md) for the resource-name annotation
used to identify composed resources. The catalog's
[local Composition rendering guide](../../../cli/local-composition-rendering.md)
describes Crossplane CLI rendering prerequisites and observed-resource fixtures.

# Citations

[1] [Inline multi-manifest template guidance](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L52)
[2] [Go text/template whitespace trimming](https://github.com/golang/go/blob/28622c19591d95c9a83f706f2ed1b303d58da85f/src/text/template/doc.go#L39-L53)
[3] [Kubernetes DNS label length](https://github.com/kubernetes/kubernetes/blob/66452049f3d692768c39c797b21b793dce80314e/staging/src/k8s.io/apimachinery/pkg/util/validation/validation.go#L158-L170)
[4] [Sprig dictionary lookup](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L11-L48) and [empty-value defaults](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L5-L25)
[5] [yq multi-document, eval, and pretty-print support](https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L350-L353) and [CLI flags](https://github.com/mikefarah/yq/blob/1b9b4ac5187171d2e5e3129be0cfa827c7f9d53d/README.md#L399-L402)
[6] [Crossplane CLI render-to-resource-validation pipeline](https://github.com/crossplane/cli/blob/ef9b974770a45e085aacee3b2cdda6284ab6cf51/cmd/crossplane/validate/help/validate.md#L61-L71)
