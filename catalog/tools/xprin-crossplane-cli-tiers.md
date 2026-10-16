---
type: Crossplane Test Tool
title: xprin Crossplane CLI tier detection
description: Understand how xprin, since v0.3.0, probes the installed Crossplane CLI and chooses the validate subcommand and render flags for it.
resource: https://github.com/crossplane-contrib/xprin
tags: [crossplane, testing, cli, xprin]
generated: { by: "process:crossplane-okf-generation", at: "2026-10-16T23:00:00Z" }
sources:
  - id: tier-definitions
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L20-L46'
    title: 'CLI tier names and descriptions'
  - id: tier-capabilities
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L60-L93'
    title: 'Capabilities per tier'
  - id: tier-detection
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/detect.go#L26-L82'
    title: 'Behavior-based tier detection'
  - id: default-subcommands
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/loader.go#L46-L65'
    title: 'Default render and validate subcommands'
  - id: detection-at-load
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/loader.go#L111-L166'
    title: 'Detection when loading configuration'
  - id: subcommand-overrides
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/checker.go#L230-L280'
    title: 'Accepted subcommand overrides'
  - id: override-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/configuration.md#L72-L80'
    title: 'Overriding auto-detection'
  - id: validate-subcommand-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/configuration.md#L49-L59'
    title: 'Validate subcommand per CLI version'
  - id: xrd-flag-docs
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/configuration.md#L61-L68'
    title: 'Documented patches.xrd behaviour'
  - id: check-output
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/checker.go#L217-L223'
    title: 'xprin check tier report'
  - id: xpcli-info-flag
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/check/check.go#L31-L45'
    title: 'xprin check --xpcli-info'
  - id: xpcli-info-output
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/checker.go#L143-L154'
    title: '--xpcli-info output fields'
  - id: xrd-patch-by-tier
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L561-L604'
    title: 'patches.xrd handling by tier'
  - id: v0-3-0-cli-tiers
    resource: 'https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/internal/xpcli/tier.go#L40-L45'
    title: 'xprin v0.3.0 CLI tiers'
  - id: docker-network-on-v2
    resource: 'https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L588-L598'
    title: 'Docker network flag on the v2 tier'
source_repository: crossplane-contrib/xprin
source_tag: v0.5.0
source_commit: eb5d7131c596e9a5663da349149184d54d704f42
source_paths: [internal/xpcli/tier.go, internal/xpcli/detect.go, internal/config/loader.go, internal/config/checker.go, cmd/xprin/check/check.go, internal/testexecution/runner/runner.go, docs/configuration.md]
introduced_in: v0.3.0
feature_state: Not stated by selected sources
feature_state_basis: xprin labels neither tier detection nor its documentation Alpha, Beta, Preview, Stable, or Deprecated, and it is not a served API.
---

# Overview

Since v0.3.0, xprin probes the configured `crossplane` binary and adapts to
it.[^v0-3-0-cli-tiers][^tier-detection][^validate-subcommand-docs] Detection checks what the binary
does rather than parsing its version: a CLI whose `render --help` lacks `--xrd`
is tier `v1`; otherwise a failing `resource validate --help` means tier
`v2legacy`; otherwise the tier is `v2`.[^tier-detection]

| Tier | Meaning | Validate subcommand | `--xrd` on render | `--crossplane-version` on render |
| --- | --- | --- | --- | --- |
| `v2` | CLI v2.3.0 or later | `resource validate` | yes | yes |
| `v2legacy` | CLI v2.0 to v2.2 | `beta validate` | yes | no |
| `v1` | Crossplane v1.x CLI binary | `beta validate` | no | no |

The tier sets these capabilities.[^tier-definitions][^tier-capabilities] On the
`v2` tier, xprin also passes `--crossplane-docker-network` to render when it
reuses function containers.[^docker-network-on-v2] The
`v1` tier refers to the CLI binary only; this catalog documents v2 workflows.

# Defaults and overrides

- The default render command is `render --include-full-xr` on every tier; only
  the default validate command changes, as `<validate subcommand>
  --error-on-missing-schemas`.[^default-subcommands][^detection-at-load]
- Explicit `subcommands.render` and `subcommands.validate` values in the xprin
  config file take precedence. Render must start with `render` or `beta render`,
  validate with `resource validate` or `beta validate`, followed only by
  flags.[^subcommand-overrides][^override-docs]

# patches.xrd by tier

On the `v2` and `v2legacy` tiers, xprin passes a test case's `patches.xrd` file
to `crossplane render` as `--xrd` and skips its own XRD-default patch; on the
`v1` tier it applies the defaults itself.[^xrd-patch-by-tier]

The project documentation instead says that on CLI v2.0 and later the defaults
are applied by `xprin-helpers patch-xr` and `--xrd` is also passed.[^xrd-flag-docs]
The code at v0.5.0 does not run that patch on tiers that support `--xrd`. This
page records the code behavior and keeps the disagreement visible.

# Inspect the tier

`xprin check` reports the detected CLI description and, when known, the
client version.[^check-output] `xprin check --xpcli-info` prints the tier,
description, and version in a fixed form and exits; its help text says it is
intended for xprin's own end-to-end tests.[^xpcli-info-flag][^xpcli-info-output]

# Limitations

- The documentation's rationale for `--xrd` concerns legacy XRD scopes and is
  excluded from this catalog.
- Claim conversion, which also reads `patches.xrd`, is excluded as legacy.

# Relationships

- [xprin test suites](xprin-test-suites.md) uses these commands to render and
  validate suites.
- [Render a Composition locally](../cli/local-composition-rendering.md)
  describes the CLI commands xprin invokes.

[^tier-definitions]: [CLI tier names and descriptions](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L20-L46)
[^tier-capabilities]: [Capabilities per tier](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/tier.go#L60-L93)
[^tier-detection]: [Behavior-based tier detection](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/xpcli/detect.go#L26-L82)
[^default-subcommands]: [Default render and validate subcommands](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/loader.go#L46-L65)
[^detection-at-load]: [Detection when loading configuration](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/loader.go#L111-L166)
[^subcommand-overrides]: [Accepted subcommand overrides](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/checker.go#L230-L280)
[^override-docs]: [Overriding auto-detection](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/configuration.md#L72-L80)
[^validate-subcommand-docs]: [Validate subcommand per CLI version](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/configuration.md#L49-L59)
[^xrd-flag-docs]: [Documented patches.xrd behaviour](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/docs/configuration.md#L61-L68)
[^check-output]: [xprin check tier report](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/checker.go#L217-L223)
[^xpcli-info-flag]: [xprin check --xpcli-info](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/cmd/xprin/check/check.go#L31-L45)
[^xpcli-info-output]: [--xpcli-info output fields](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/config/checker.go#L143-L154)
[^xrd-patch-by-tier]: [patches.xrd handling by tier](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L561-L604)
[^v0-3-0-cli-tiers]: [xprin v0.3.0 CLI tiers](https://github.com/crossplane-contrib/xprin/blob/92a24a66e5e243b67c22b9d58bd9e8d857bc85a4/internal/xpcli/tier.go#L40-L45)
[^docker-network-on-v2]: [Docker network flag on the v2 tier](https://github.com/crossplane-contrib/xprin/blob/eb5d7131c596e9a5663da349149184d54d704f42/internal/testexecution/runner/runner.go#L588-L598)
