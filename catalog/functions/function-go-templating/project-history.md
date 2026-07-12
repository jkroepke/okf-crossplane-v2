---
type: reference
title: function-go-templating v0.12.2 project history
description: Human-authored release changes, version-scoped reports, and post-release developments researched on 2026-07-12.
resource: https://github.com/crossplane-contrib/function-go-templating
tags: [crossplane, composition-function, project-history]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane-contrib/function-go-templating
source_tag: v0.12.2
source_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
research_timestamp: 2026-07-12
feature_state: Not stated by selected sources
---

# Included in selected release

Human-authored PR #580 is the sole commit between v0.12.1 and v0.12.2.
It updated Go and selected indirect dependencies as a security remediation.
Its merge commit is the selected release commit, proving containment; the released `go.mod` corroborates the dependency result.[1][2]

# Known reports for selected release

No open report below was shown to reproduce on v0.12.2. They remain version-scoped reports, not established behavior:

- #579 reports missing observed composite spec fields on initial reconciliation against function v0.11.0 and Crossplane v1.19.x.[3]
- #536 reports ExtraResources differing between local render and in-cluster execution against function v0.11.3 and Crossplane 2.1.1.[4]
- #535 reports `getExtraResourcesFromContext` unavailable at render time against v0.11.3.[5]
- #501 reports `matchName` not finding an XR while `matchLabels` did against v0.9.0.[6]
- #61 reports template parse errors without a useful source filename; selected-release applicability is unverified.[7]
- #40 reports misleading legacy connection-detail error handling against v0.3.0. It does not establish v2 connection behavior.[8]

# Post-release proposals or developments

After v0.12.2, issue #591 and merged PR #592 addressed a function-specific gRPC receive-size setting on `main`; this is not contained in v0.12.2.[9] Open PR #593 proposes renaming that setting and remains an unmerged proposal.[10]

# Research boundaries

Research was performed on 2026-07-12.
Bot/app issues, pull requests, comments, and reviews were excluded, including Renovate activity.
Claim-readiness issue #99 was excluded as legacy material.
Project history is not used to establish API shape, runtime behavior, recommendations, or feature maturity; maturity is **Not stated by selected sources**.

# Citations

[1] [v0.12.1...v0.12.2 comparison](https://github.com/crossplane-contrib/function-go-templating/compare/v0.12.1...v0.12.2)
[2] [PR #580](https://github.com/crossplane-contrib/function-go-templating/pull/580) and [released go.mod](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod)
[3] [Issue #579](https://github.com/crossplane-contrib/function-go-templating/issues/579)
[4] [Issue #536](https://github.com/crossplane-contrib/function-go-templating/issues/536)
[5] [Issue #535](https://github.com/crossplane-contrib/function-go-templating/issues/535)
[6] [Issue #501](https://github.com/crossplane-contrib/function-go-templating/issues/501)
[7] [Issue #61](https://github.com/crossplane-contrib/function-go-templating/issues/61)
[8] [Issue #40](https://github.com/crossplane-contrib/function-go-templating/issues/40)
[9] [Issue #591](https://github.com/crossplane-contrib/function-go-templating/issues/591) and [PR #592](https://github.com/crossplane-contrib/function-go-templating/pull/592)
[10] [PR #593](https://github.com/crossplane-contrib/function-go-templating/pull/593)
