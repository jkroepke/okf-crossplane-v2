---
type: reference
title: Sprig v3.3.0 in function-go-templating
description: Versioned Sprig capability reference constrained to the function's exposed map.
resource: https://github.com/Masterminds/sprig/tree/e708470d529a10ac1a3f02ab6fdd339b65958372
tags: [crossplane, composition-function, sprig, template-functions]
generated: { by: "process:okf-v0.2-migration", at: "2026-08-20T06:45:13Z" }
sources:
  - id: function-dependency-on-sprig-v3-3-0
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L9'
    title: 'Function dependency on Sprig v3.3.0'
  - id: function-map-exclusions
    resource: 'https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62'
    title: 'Function-map exclusions'
  - id: sprig-capability-index
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/index.md#L3-L25'
    title: 'Sprig capability index'
  - id: lists
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/lists.md#L1-L82'
    title: 'Lists'
  - id: dictionaries
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L1-L89'
    title: 'dictionaries'
  - id: defaults
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L1-L87'
    title: 'defaults'
  - id: encoding
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/encoding.md#L1-L6'
    title: 'Encoding'
  - id: paths
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/paths.md#L1-L63'
    title: 'paths'
  - id: urls
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/url.md#L1-L32'
    title: 'URLs'
  - id: reflection
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L1-L50'
    title: 'reflection'
  - id: dates
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/date.md#L1-L90'
    title: 'Dates'
  - id: semantic-versions
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/semver.md#L1-L62'
    title: 'semantic versions'
  - id: cryptographic-and-password-helpers
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/crypto.md#L1-L90'
    title: 'Cryptographic and password helpers'
  - id: uuid
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/uuid.md#L1-L9'
    title: 'UUID'
  - id: network-lookup
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/network.md#L1-L10'
    title: 'network lookup'
  - id: general-versus-hermetic-function-maps
    resource: 'https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/functions.go#L67-L94'
    title: 'General versus hermetic function maps'
source_repository: Masterminds/sprig
source_tag: v3.3.0
source_commit: e708470d529a10ac1a3f02ab6fdd339b65958372
selected_by_function_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Overview

`function-go-templating` v0.12.2 requires Sprig v3.3.0 and exposes its general function map except `env` and `expandenv`.[^function-dependency-on-sprig-v3-3-0][^function-map-exclusions] Sprig is a supporting template library, not a Crossplane API or feature.

# Capabilities

| Area | Selected behavior |
|---|---|
| Text, conversion, math | String shaping, scalar/collection conversion, integer and floating-point arithmetic.[^sprig-capability-index] |
| Lists, dictionaries, defaults | List operations generally return new lists; `set` and `unset` mutate string-keyed dictionaries; defaults use documented empty-value semantics.[^lists][^dictionaries][^defaults] |
| Encoding, paths, URLs, reflection | Base32/Base64, path-string manipulation without filesystem access, URL dictionaries, and Go kind/type inspection.[^encoding][^paths][^urls][^reflection] |
| Dates and semantic versions | Time formatting/modification and SemVer parsing/constraint evaluation.[^dates][^semantic-versions] |
| Cryptography, randomness, network | Hashing, key/certificate and password helpers, random values, UUID v4, and DNS lookup.[^cryptographic-and-password-helpers][^uuid][^network-lookup] |

# Limitations

`env` and `expandenv` are explicitly unavailable.[^function-map-exclusions] Current-time, random, and DNS functions are non-hermetic and may produce different output for identical template input.[^general-versus-hermetic-function-maps] Sprig warns against
embedding password material directly in templates.[^cryptographic-and-password-helpers][^uuid][^network-lookup]

Sprig's project stability labels are not Crossplane maturity evidence. Feature maturity is **Not stated by selected sources**.

[^function-dependency-on-sprig-v3-3-0]: [Function dependency on Sprig v3.3.0](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L9)
[^function-map-exclusions]: [Function-map exclusions](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62)
[^sprig-capability-index]: [Sprig capability index](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/index.md#L3-L25)
[^lists]: [Lists](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/lists.md#L1-L82), [dictionaries](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L1-L89), and [defaults](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L1-L87)
[^dictionaries]: [dictionaries](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L1-L89)
[^defaults]: [defaults](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L1-L87)
[^encoding]: [Encoding](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/encoding.md#L1-L6), [paths](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/paths.md#L1-L63), [URLs](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/url.md#L1-L32), and [reflection](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L1-L50)
[^paths]: [paths](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/paths.md#L1-L63)
[^urls]: [URLs](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/url.md#L1-L32)
[^reflection]: [reflection](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L1-L50)
[^dates]: [Dates](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/date.md#L1-L90) and [semantic versions](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/semver.md#L1-L62)
[^semantic-versions]: [semantic versions](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/semver.md#L1-L62)
[^cryptographic-and-password-helpers]: [Cryptographic and password helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/crypto.md#L1-L90), [UUID](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/uuid.md#L1-L9), and [network lookup](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/network.md#L1-L10)
[^uuid]: [UUID](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/uuid.md#L1-L9)
[^network-lookup]: [network lookup](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/network.md#L1-L10)
[^general-versus-hermetic-function-maps]: [General versus hermetic function maps](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/functions.go#L67-L94)
