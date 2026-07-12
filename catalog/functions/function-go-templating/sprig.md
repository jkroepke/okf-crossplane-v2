---
type: Reference
title: Sprig v3.3.0 in function-go-templating
description: Versioned Sprig capability reference constrained to the function's exposed map.
resource: https://github.com/Masterminds/sprig/tree/e708470d529a10ac1a3f02ab6fdd339b65958372
tags: [crossplane, composition-function, sprig, template-functions]
timestamp: 2026-07-12T00:00:00Z
source_repository: Masterminds/sprig
source_tag: v3.3.0
source_commit: e708470d529a10ac1a3f02ab6fdd339b65958372
selected_by_function_commit: 0a1e6d386f4363fae257ddbfb5b497416370e830
feature_state: Not stated by selected sources
---

# Overview

`function-go-templating` v0.12.2 requires Sprig v3.3.0 and exposes its general function map except `env` and `expandenv`.[1][2] Sprig is a supporting template library, not a Crossplane API or feature.

# Capabilities

| Area | Selected behavior |
|---|---|
| Text, conversion, math | String shaping, scalar/collection conversion, integer and floating-point arithmetic.[3] |
| Lists, dictionaries, defaults | List operations generally return new lists; `set` and `unset` mutate string-keyed dictionaries; defaults use documented empty-value semantics.[4] |
| Encoding, paths, URLs, reflection | Base32/Base64, path-string manipulation without filesystem access, URL dictionaries, and Go kind/type inspection.[5] |
| Dates and semantic versions | Time formatting/modification and SemVer parsing/constraint evaluation.[6] |
| Cryptography, randomness, network | Hashing, key/certificate and password helpers, random values, UUID v4, and DNS lookup.[7] |

# Limitations

`env` and `expandenv` are explicitly unavailable.[2] Current-time, random, and DNS functions are non-hermetic and may produce different output for identical template input.[8] Sprig warns against embedding password material directly in templates.[7]

Sprig's project stability labels are not Crossplane maturity evidence. Feature maturity is **Not stated by selected sources**.

# Citations

[1] [Function dependency on Sprig v3.3.0](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/go.mod#L5-L9)
[2] [Function-map exclusions](https://github.com/crossplane-contrib/function-go-templating/blob/0a1e6d386f4363fae257ddbfb5b497416370e830/function_maps.go#L56-L62)
[3] [Sprig capability index](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/index.md#L3-L25)
[4] [Lists](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/lists.md#L1-L82), [dictionaries](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/dicts.md#L1-L89), and [defaults](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/defaults.md#L1-L87)
[5] [Encoding](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/encoding.md#L1-L6), [paths](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/paths.md#L1-L63), [URLs](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/url.md#L1-L32), and [reflection](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/reflection.md#L1-L50)
[6] [Dates](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/date.md#L1-L90) and [semantic versions](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/semver.md#L1-L62)
[7] [Cryptographic and password helpers](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/crypto.md#L1-L90), [UUID](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/uuid.md#L1-L9), and [network lookup](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/docs/network.md#L1-L10)
[8] [General versus hermetic function maps](https://github.com/Masterminds/sprig/blob/e708470d529a10ac1a3f02ab6fdd339b65958372/functions.go#L67-L94)
