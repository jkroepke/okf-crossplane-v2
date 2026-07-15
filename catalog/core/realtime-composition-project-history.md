---
type: reference
title: Real-time composition reconciliation project history
description: Human-authored reconciliation-churn reports, a selected-release runtime fix, and a post-release GA proposal researched for Crossplane v2.3.3.
resource: https://github.com/crossplane/crossplane/issues/6453
tags: [crossplane, core, composition, reconciliation, realtime, project-history]
timestamp: 2026-07-14T00:00:00Z
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
  established.[1]
- **crossplane/crossplane #6824 (closed by stale automation, not fixed):**
  reports increased CPU and audit traffic after the feature became
  default-enabled Beta. Maintainers point to field fights or flapping and the
  XR circuit breaker as areas to inspect. The report was not closed by a
  verified fix.[2]
- **crossplane/crossplane #7024 (reporter-closed):** reports a high-CPU loop
  associated with an empty metadata label; the reporter says assigning a value
  stopped the reproduction. This is an environment-specific outcome, not
  evidence of a released Core fix.[3]
- **provider-kubernetes #421 (open):** reports no-change `Object` status and
  apply events feeding a reconciliation cycle. The reporter says it persisted
  with real-time compositions disabled and later narrowed the reproduction to
  legacy `v1alpha1 Object`, not `v1alpha2`. It is retained as a version-bounded
  report, not current API guidance.[4]

# Included in selected release

- **crossplane-runtime #902 / PR #906:** issue #902 reported that a
  provider-supplied `Synced` condition without `observedGeneration` compared
  unequal on every poll, changing transition time and producing watch events.
  PR #906 defensively ignores generation when either side is zero; its merge
  commit is contained in crossplane-runtime v2.3.3. The released equality
  behavior is also present in selected Crossplane v2.3.3 source. The
  provider-kubernetes #421 reporter explicitly considered that issue a
  different cause.[5][6]

# Post-release proposal or development

- **crossplane/crossplane #6453 (open):** tracks promotion of real-time
  compositions from Beta to GA and proposes removing the disable switch only
  after implementation bugs are addressed. It does not establish GA maturity
  or a committed release.[7]

# Limitations

- The linked issues have distinct or unresolved causes. They do not establish that real-time composition alone causes every reported loop.

# Relationships

See [real-time composition reconciliation](realtime-composition-reconciliation.md)
for the selected-release behavior and operational safeguards.

# Citations

[1] [Issue #6898](https://github.com/crossplane/crossplane/issues/6898) and [maintainer trigger analysis](https://github.com/crossplane/crossplane/issues/6898#issuecomment-3518376485)
[2] [Issue #6824](https://github.com/crossplane/crossplane/issues/6824)
[3] [Issue #7024](https://github.com/crossplane/crossplane/issues/7024) and [reporter outcome](https://github.com/crossplane/crossplane/issues/7024#issuecomment-3793358748)
[4] [provider-kubernetes issue #421](https://github.com/crossplane-contrib/provider-kubernetes/issues/421) and [reported version boundary](https://github.com/crossplane-contrib/provider-kubernetes/issues/421#issuecomment-3894626461)
[5] [crossplane-runtime issue #902](https://github.com/crossplane/crossplane-runtime/issues/902) and [maintainer analysis](https://github.com/crossplane/crossplane-runtime/issues/902#issuecomment-3792053064)
[6] [Released defensive condition equality in Crossplane v2.3.3](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/apis/core/v2/condition.go#L105-L124)
and [PR #906 merge containment in runtime v2.3.3](https://github.com/crossplane/crossplane-runtime/compare/311ca76bbd30f86e196438771062091a39e39e0d...fcf6aaa11ef4b56b9a8b1b91a446e0f6b8fc2827)
[7] [GA promotion proposal #6453](https://github.com/crossplane/crossplane/issues/6453)
