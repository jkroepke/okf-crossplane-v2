---
type: developmentguide
title: Composition Functions specification
description: The v2.3.3 specification for composition-function serving, desired-state handling, configuration, packaging, and runtime assumptions.
resource: https://github.com/crossplane/crossplane/blob/v2.3.3/contributing/specifications/functions.md
tags: [crossplane, composition-functions, specification, development]
timestamp: 2026-07-12T00:00:00Z
source_repository: crossplane/crossplane
source_commit: 09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d
source_paths:
  - contributing/specifications/functions.md
---

# Scope

This document summarizes the Composition Functions specification from the selected Crossplane v2.3.3 release. Runtime claims still require protocol, controller, or test corroboration.[1]

Despite its generic filename, the specification explicitly covers **composition functions**: functions that instruct Crossplane how to compose an XR. It does not specify [operation-function](operation-functions.md) 
desired-state or execution semantics.[2]

# Serving contract

A composition function must implement the gRPC `FunctionRunnerService`. It must copy request metadata tags unchanged to corresponding responses and should set a response TTL representing how long Crossplane may cache 
the response for an identical request.[3]

A function must intentionally propagate desired state from earlier pipeline steps when it has no opinion. A Fatal result is reserved for terminating the entire pipeline; Normal and Warning results should indicate 
transitions rather than repeat on every call.[4]

# Desired-state constraints

- A function may set only desired composite-resource status, not its spec or metadata.
- It may set non-status fields of desired composed resources, but not their status.
- It should normally allow Crossplane to generate composed-resource names and may use `crossplane.io/external-name` to influence an external name.
- It should avoid collisions with existing observed or desired composed resources.[5]

These constraints are composition-specific and are not transferred to operation functions, which use different state semantics and may output arbitrary Kubernetes resources.

# Configuration and runtime

The specification requires `--debug`, `--insecure`, and `--tls-certs-dir`, with `TLS_SERVER_CERTS_DIR` support. Functions listen on TCP port 9443 and use gRPC transport security unless explicitly configured 
insecurely.[6]

An implementation must not assume a particular deployment model or network access, and should fail gracefully when required network access is unavailable.[7]

# Packaging

The specification requires xpkg packaging and a package name beginning with `function-`. It recommends the `io.crossplane.xpkg:base` OCI annotation for delivering metadata and the function binary in one image.[8]

# Limitations

The specification recommends the latest service version but gives `v1beta1` as its example and links to a moving `main` protocol directory. The selected v2.3.3 source contains the shared `proto/fn/v1` protocol;
consumers should treat the protocol definition, not the example version string, as authoritative.[3][9]

# Citations

[1] [v2.3.3 Composition Functions specification](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md)
[2] [Specification title and composition-only scope](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L1-L10)
[3] [Service, metadata tag, and TTL requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L12-L27)
[4] [Desired-state propagation and result semantics](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L29-L42) and
[results](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L61-L67)
[5] [Desired composite and composed resource constraints](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L44-L59)
[6] [Configuration and transport requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L69-L86)
[7] [Runtime-environment requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L99-L109)
[8] [Packaging and naming requirements](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/contributing/specifications/functions.md#L88-L97)
[9] [v2.3.3 shared v1 function protocol](https://github.com/crossplane/crossplane/blob/09ffaea39ccaea0f80817e35b5bbd3632b4e7e0d/proto/fn/v1/run_function.proto#L19-L35)
