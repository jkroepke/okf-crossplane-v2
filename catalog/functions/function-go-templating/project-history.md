---
type: reference
title: function-go-templating v0.12.2 project history
description: Human-authored release changes, version-scoped reports, reported workarounds, and post-release developments researched on 2026-07-14.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, project-history]
timestamp: 2026-07-14T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
research_timestamp: 2026-07-14
feature_state: Not stated by selected sources
---

# Included in selected release

Human-authored PR #580 is the sole commit between v0.12.1 and v0.12.2.
It updated Go and selected indirect dependencies as a security remediation.
Its merge commit is the selected release commit, proving containment; the released `go.mod` corroborates the dependency result.[1][2]

Earlier human-authored PR #498 introduced the ExtraResources `namespace` field
while updating function-sdk-go. Its merge commit is an ancestor of v0.12.2,
proving release containment. The released conversion code shows that the PR's
namespace assignment is reached only for `matchName`; the `matchLabels` branch
returns first.[15][16]

# Known reports for selected release

No open report below was shown to reproduce on v0.12.2. They remain version-scoped reports, not established behavior:

- #579 reports that fields from the XR spec were absent from
  `.observed.composite.resource.spec` during initial reconciliation against
  function v0.11.0 and Crossplane v1.19.x. In the report, `with` blocks for
  those fields emitted no resources, while another failing resource was said
  to prevent a later successful render.[3]
- #536 reports ExtraResources differing between local render and in-cluster execution against function v0.11.3 and Crossplane 2.1.1.[4]
- #535 reports `getExtraResourcesFromContext` unavailable at render time against v0.11.3.[5]
- #501 reports `matchName` not finding an XR while `matchLabels` did against v0.9.0.[6]
- #61 reports template parse errors without a useful source filename; selected-release applicability is unverified.[7]
- #40 reports misleading legacy connection-detail error handling against v0.3.0. It does not establish v2 connection behavior.[8]

## Reported workarounds for #579

The issue reporter described these mitigations; they are not selected-release
recommendations or proof of the reported root cause:

- Read user-intent fields from `.desired.composite.resource.spec` instead of
  `.observed.composite.resource.spec`. The reporter said this resolved the
  reproduction. The selected v0.12.2 README independently confirms that both
  desired and observed composite state are available to templates, but does
  not document issue #579 or prefer one for this use case.[3][11]
- Use the desired spec with the observed spec as a fallback:

  ```gotemplate
  {{- $spec := .desired.composite.resource.spec | default .observed.composite.resource.spec -}}
  ```

  This is adapted from the reporter's workaround. Sprig `default` treats an
  empty desired spec as absent, so templates using this form must decide
  whether that fallback behavior is appropriate.[3][12]
- Split the rendered resources across multiple pipeline steps. The reporter
  proposed this after observing convergence with fewer resources, but the
  issue does not independently validate it as a general fix.[13]

Issue #579 remains open. A collaborator asked for reproduction with current
Crossplane and function releases because the reported Crossplane v1.19 line is
old. No response, linked fix, or evidence that the report reproduces on v0.12.2
was present at the research timestamp.[13][14]

# Post-release proposals or developments

After v0.12.2, issue #591 and merged PR #592 addressed a function-specific gRPC receive-size setting on `main`; this is not contained in v0.12.2.[9] Open PR #593 proposes renaming that setting and remains an unmerged proposal.[10]

# Research boundaries

Research was performed on 2026-07-14.
Bot/app issues, pull requests, comments, and reviews were excluded, including Renovate activity.
Claim-readiness issue #99 was excluded as legacy material.
Project history is not used to establish API shape, runtime behavior, recommendations, or feature maturity; maturity is **Not stated by selected sources**.

# Citations

[1] [v0.12.1...v0.12.2 comparison](https://github.com/crossplane-contrib/function-go-templating/compare/548ae34fd9c843f0747981894fb7fa0ff1ba47fa...0a1e6d386f4363fae257ddbfb5b497416370e830)
[2] [PR #580](https://github.com/crossplane-contrib/function-go-templating/pull/580) and [released go.mod](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod)
[3] [Issue #579](https://github.com/crossplane-contrib/function-go-templating/issues/579)
[4] [Issue #536](https://github.com/crossplane-contrib/function-go-templating/issues/536)
[5] [Issue #535](https://github.com/crossplane-contrib/function-go-templating/issues/535)
[6] [Issue #501](https://github.com/crossplane-contrib/function-go-templating/issues/501)
[7] [Issue #61](https://github.com/crossplane-contrib/function-go-templating/issues/61)
[8] [Issue #40](https://github.com/crossplane-contrib/function-go-templating/issues/40)
[9] [Issue #591](https://github.com/crossplane-contrib/function-go-templating/issues/591) and [PR #592](https://github.com/crossplane-contrib/function-go-templating/pull/592)
[10] [PR #593](https://github.com/crossplane-contrib/function-go-templating/pull/593)
[11] [Selected-release request data](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73)
[12] [Pinned Sprig `default` documentation](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L5-L31)
[13] [Issue #579 reporter follow-up](https://github.com/crossplane-contrib/function-go-templating/issues/579#issuecomment-4699609327)
[14] [Issue #579 collaborator request for current-release reproduction](https://github.com/crossplane-contrib/function-go-templating/issues/579#issuecomment-4803746103)
[15] [PR #498 and its merge commit](https://github.com/crossplane-contrib/function-go-templating/pull/498)
and [containment in v0.12.2](https://github.com/crossplane-contrib/function-go-templating/compare/fba11b570e75660b1ff52b05979ba805baae1a51...0a1e6d386f4363fae257ddbfb5b497416370e830)
[16] [Released ExtraResources selector conversion](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/extraresources.go#L41-L62)
