---
type: Evidence Ledger
title: function-go-templating v0.12.2 claim ledger
---

# Scope

Selected release `v0.12.2` at `0a1e6d386f4363fae257ddbfb5b497416370e830`; supporting Sprig `v3.3.0` at `e708470d529a10ac1a3f02ab6fdd339b65958372`. Feature state is **Not stated by selected sources** for every concept. Claims, deprecated XRD v1, legacy v1 XR semantics, and the README section explicitly labelled `v1 Composite Resources (Legacy)` were excluded.

# Claims

All claims have function scope v0.12.2 unless a narrower version is stated.

| Concept | Exact claim | Class | Source role | Confidence | Evidence |
|---|---|---|---|---|---|
| package | A pipeline references the installed Function name and supplies a v1beta1 GoTemplate input. | API | primary | direct | [README L9-L44](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L9-L44) |
| package | This catalog selected v0.12.2 and pinned its commit. | release-history | primary | direct | [commit 0a1e6d3](https://github.com/crossplane-contrib/function-go-templating/commit/0a1e6d386f4363fae257ddbfb5b497416370e830) and source lock |
| input | The generated CRD serves/stores v1beta1, requires `source`, and defines the six input fields. | API | primary | direct | [CRD L8-L94](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L8-L94) |
| input | Inline requires exactly one of `template` and `templates`. | API | primary | direct | [CRD L56-L69](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L56-L69) |
| input | Default delimiters are `{{` and `}}`; `options` is top-level. | API | primary | direct | [CRD L31-L42](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L31-L42), [L80-L85](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/package/input/gotemplating.fn.crossplane.io_gotemplates.yaml#L80-L85) |
| input | Inline, FileSystem, and Environment load templates as documented. | documented-guidance | primary | direct | [README L46-L59](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L46-L59) |
| request-data | Templates receive observed/desired state, context, and extra resources. | behavior | primary | direct | [README L60-L73](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L60-L73) |
| request-data | Context and ExtraResources special resources update pipeline context. | behavior | primary | direct | [README L159-L277](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L159-L277) |
| request-data | `getCredentialData` returns named request credential bytes. | behavior | primary | direct | [function_maps.go L166-L177](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L166-L177) |
| rendered-output | Resource-name and readiness annotations control composed-resource identity and readiness reporting. | behavior | primary | direct | [function_maps.go L101-L103](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L101-L103), [README L124-L147](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L124-L147) |
| rendered-output | v2 connection details use an explicitly composed Secret. | documented-guidance | primary | direct | [README L101-L122](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L101-L122) |
| rendered-output | Same-type output can update status or create a composed resource; recursion must terminate through another composition. | behavior/guidance | primary | direct | [README L279-L350](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/README.md#L279-L350) |
| template-functions | The selected function map adds eleven named helpers; `include` has a recursion bound. | API/behavior | primary | direct | [function_maps.go L24-L55](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L24-L55), [L105-L121](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L105-L121) |
| template-functions | Sprig v3.3.0 is required; `env` and `expandenv` are removed. | API/behavior | primary | direct | [go.mod L5-L10](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L10), [function_maps.go L56-L62](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62) |
| sprig | Exposed Sprig groups cover data shaping, collections, encoding, paths, dates, SemVer, crypto, randomness, and network. | documented-guidance | supporting, availability gated by primary | corroborated | [Sprig index L3-L25](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/index.md#L3-L25), [function map L56-L62](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62) |
| sprig | Current-time, random, and DNS helpers are non-hermetic. | behavior | supporting | direct | [functions.go L67-L94](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/functions.go#L67-L94) |
| project-history | PR #580 is the sole commit from v0.12.1 to v0.12.2 and is contained in the selected release. | release-history | project-history corroborated by released source | corroborated | [comparison](https://github.com/crossplane-contrib/function-go-templating/compare/v0.12.1...v0.12.2), [released go.mod](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod) |
| project-history | Issues #579, #536, #535, #501, #61, and #40 are older-version or unverified reports, not v0.12.2 facts. | reported-limitation | project-history | direct as reports | Direct issue URLs in `project-history.md`; researched 2026-07-12 |
| project-history | PR #592 is post-release main-branch development and open PR #593 is a proposal, neither part of v0.12.2. | proposal | project-history | direct | Direct PR URLs in `project-history.md`; researched 2026-07-12 |

# Unresolved

- Runtime source-to-field validation is outside the selected generated schema scope.
- The only bundled FileSystem example is legacy-only, so no runnable v2 FileSystem example is retained.
- No open report was shown to reproduce on v0.12.2.
- README nests `options` under `inline`, conflicting with the generated CRD; catalog follows the generated schema.
- Bundled installation examples pin v0.11.5 and use varying Function object names; catalog uses selected v0.12.2 and requires name matching.
