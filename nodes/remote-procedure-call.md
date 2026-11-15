---
id: remote-procedure-call
title: Remote procedure call
summary: A remote procedure call invokes a named operation on another process through a request and response, while exposing network failures that a local call does not have.
type: concept
tags: [networking]
prereqs: [network-stack]
sources: [https://grpc.io/docs/what-is-grpc/introduction/]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Remote procedure call

## Summary

A **remote procedure call (RPC)** asks a program elsewhere to execute a named operation and return a result. Its client-facing syntax can resemble a local function call, but the operation crosses a network boundary.

## Grounded explanation

A client invokes `GetUser(id=42)`. Its RPC client encodes the operation name and argument into a request, sends it through the [[network-stack]], and waits. A server receives the request, dispatches it to an implementation, then sends a result or error back. A generated client method hides this communication; it does not eliminate it.

The key difference from a local call is **partial failure**. The request can be lost, the server can fail after performing the operation, or the reply can be lost. A timeout means the client did not receive a timely answer; it does not prove the operation never happened. Retrying an operation with side effects therefore requires deliberate semantics, such as an idempotency key. Deadlines, cancellation, authentication, and version compatibility also matter at this boundary.

An RPC framework specifies how callers address operations and how requests, responses, and failures are represented. It does not automatically make distributed calls reliable or exactly-once.

## Prerequisites

- [[network-stack]]

## Sources

- [gRPC introduction](https://grpc.io/docs/what-is-grpc/introduction/).
