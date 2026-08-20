---
type: reference
title: Real-time composition reconciliation project history
description: Human-authored reconciliation-churn reports, a selected-release runtime fix, and a post-release GA proposal researched for Crossplane v2.3.3.
resource: https://github.com/crossplane/crossplane/issues/6453
tags: [crossplane, core, composition, reconciliation, realtime, project-history]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: issue-6898
    resource: 'https://github.com/crossplane/crossplane/issues/6898'
    title: 'Issue #6898'
  - id: maintainer-trigger-analysis
    resource: 'https://github.com/crossplane/crossplane/issues/6898#issuecomment-3518376485'
    title: 'maintainer trigger analysis'
  - id: issue-6824
    resource: 'https://github.com/crossplane/crossplane/issues/6824'
    title: 'Issue #6824'
  - id: issue-7024
    resource: 'https://github.com/crossplane/crossplane/issues/7024'
    title: 'Issue #7024'
  - id: reporter-outcome
    resource: 'https://github.com/crossplane/crossplane/issues/7024#issuecomment-3793358748'
    title: 'reporter outcome'
  - id: provider-kubernetes-issue-421
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/issues/421'
    title: 'provider-kubernetes issue #421'
  - id: reported-version-boundary
    resource: 'https://github.com/crossplane-contrib/provider-kubernetes/issues/421#issuecomment-3894626461'
    title: 'reported version boundary'
  - id: crossplane-runtime-issue-902
    resource: 'https://github.com/crossplane/crossplane-runtime/issues/902'
    title: 'crossplane-runtime issue #902'
  - id: maintainer-analysis
    resource: 'https://github.com/crossplane/crossplane-runtime/issues/902#issuecomment-3792053064'
    title: 'maintainer analysis'
  - id: released-defensive-condition-equality-in-crossplane-v2-3-3
    resource: 'https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/condition.go#L105-L124'
    title: 'Released defensive condition equality in Crossplane v2.3.3'
  - id: pr-906-merge-containment-in-runtime-v2-3-3
    resource: 'https://github.com/crossplane/crossplane-runtime/compare/311ca76bbd30f86e196438771062091a39e39e0d...fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827'
    title: 'PR #906 merge containment in runtime v2.3.3'
  - id: ga-promotion-proposal-6453
    resource: 'https://github.com/crossplane/crossplane/issues/6453'
    title: 'GA promotion proposal #6453'
crossplane_release: v2.3.3
project_history_researched_at: 2026-07-14
---

# Project history

Research timestamp: **2026-07-14**. The following are human-authored reports or proposals. Bot and app activity was excluded, and issue closure alone is not treated as proof of a released fix.

# Known reports for the selected release model

- **crossplane/crossplane #6898 (open):** reports repeated no-op
  composed-resource patches and high API/audit traffic. Maintainer analysis
  distinguishes XR changes, CompositionRevision changes, composed-resource
  watch events, periodic reconciliation without real-time mode, and informer
  resync. Later reports identify short function TTLs and unwatched external
  inputs as additional churn and freshness tradeoffs. No released fix is
  established.[^issue-6898][^maintainer-trigger-analysis]
- **crossplane/crossplane #6824 (closed by stale automation, not fixed):**
  reports increased CPU and audit traffic after the feature became
  default-enabled Beta. Maintainers point to field fights or flapping and the
  XR circuit breaker as areas to inspect. The report was not closed by a
  verified fix.[^issue-6824]
- **crossplane/crossplane #7024 (reporter-closed):** reports a high-CPU loop
  associated with an empty metadata label; the reporter says assigning a value
  stopped the reproduction. This is an environment-specific outcome, not
  evidence of a released Core fix.[^issue-7024][^reporter-outcome]
- **provider-kubernetes #421 (open):** reports no-change `Object` status and
  apply events feeding a reconciliation cycle. The reporter says it persisted
  with real-time compositions disabled and later narrowed the reproduction to
  legacy `v1alpha1 Object`, not `v1alpha2`. It is retained as a version-bounded
  report, not current API guidance.[^provider-kubernetes-issue-421][^reported-version-boundary]

# Included in selected release

- **crossplane-runtime #902 / PR #906:** issue #902 reported that a
  provider-supplied `Synced` condition without `observedGeneration` compared
  unequal on every poll, changing transition time and producing watch events.
  PR #906 defensively ignores generation when either side is zero; its merge
  commit is contained in crossplane-runtime v2.3.3. The released equality
  behavior is also present in selected Crossplane v2.3.3 source. The
  provider-kubernetes #421 reporter explicitly considered that issue a
  different cause.[^crossplane-runtime-issue-902][^maintainer-analysis][^released-defensive-condition-equality-in-crossplane-v2-3-3][^pr-906-merge-containment-in-runtime-v2-3-3]

# Post-release proposal or development

- **crossplane/crossplane #6453 (open):** tracks promotion of real-time
  compositions from Beta to GA and proposes removing the disable switch only
  after implementation bugs are addressed. It does not establish GA maturity
  or a committed release.[^ga-promotion-proposal-6453]

# Limitations

- The linked issues have distinct or unresolved causes. They do not establish that real-time composition alone causes every reported loop.

# Relationships

See [real-time composition reconciliation](realtime-composition-reconciliation.md)
for the selected-release behavior and operational safeguards.

[^issue-6898]: [Issue #6898](https://github.com/crossplane/crossplane/issues/6898) and [maintainer trigger analysis](https://github.com/crossplane/crossplane/issues/6898#issuecomment-3518376485)
[^maintainer-trigger-analysis]: [maintainer trigger analysis](https://github.com/crossplane/crossplane/issues/6898#issuecomment-3518376485)
[^issue-6824]: [Issue #6824](https://github.com/crossplane/crossplane/issues/6824)
[^issue-7024]: [Issue #7024](https://github.com/crossplane/crossplane/issues/7024) and [reporter outcome](https://github.com/crossplane/crossplane/issues/7024#issuecomment-3793358748)
[^reporter-outcome]: [reporter outcome](https://github.com/crossplane/crossplane/issues/7024#issuecomment-3793358748)
[^provider-kubernetes-issue-421]: [provider-kubernetes issue #421](https://github.com/crossplane-contrib/provider-kubernetes/issues/421) and [reported version boundary](https://github.com/crossplane-contrib/provider-kubernetes/issues/421#issuecomment-3894626461)
[^reported-version-boundary]: [reported version boundary](https://github.com/crossplane-contrib/provider-kubernetes/issues/421#issuecomment-3894626461)
[^crossplane-runtime-issue-902]: [crossplane-runtime issue #902](https://github.com/crossplane/crossplane-runtime/issues/902) and [maintainer analysis](https://github.com/crossplane/crossplane-runtime/issues/902#issuecomment-3792053064)
[^maintainer-analysis]: [maintainer analysis](https://github.com/crossplane/crossplane-runtime/issues/902#issuecomment-3792053064)
[^released-defensive-condition-equality-in-crossplane-v2-3-3]: [Released defensive condition equality in Crossplane v2.3.3](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/condition.go#L105-L124) and [PR #906 merge containment in runtime v2.3.3](https://github.com/crossplane/crossplane-runtime/compare/311ca76bbd30f86e196438771062091a39e39e0d...fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827)
[^pr-906-merge-containment-in-runtime-v2-3-3]: [PR #906 merge containment in runtime v2.3.3](https://github.com/crossplane/crossplane-runtime/compare/311ca76bbd30f86e196438771062091a39e39e0d...fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827)
[^ga-promotion-proposal-6453]: [GA promotion proposal #6453](https://github.com/crossplane/crossplane/issues/6453)
