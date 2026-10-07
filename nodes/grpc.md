---
id: grpc
title: gRPC
summary: gRPC is an RPC framework that defines service methods and message types, generates client and server interfaces, and normally carries calls over HTTP/2 with Protocol Buffers messages.
type: concept
tags: [networking]
prereqs: [remote-procedure-call, protocol-buffers, http-2]
sources: [https://grpc.io/docs/what-is-grpc/core-concepts/]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# gRPC

## Summary

**gRPC** is a framework for [[remote-procedure-call]]s. A service contract names methods and their input/output message types; generated clients invoke them and server implementations handle them. By default, [[protocol-buffers]] defines and encodes the messages, while [[http-2]] carries the calls.

## Grounded explanation

A `.proto` contract might declare `rpc GetUser(UserRequest) returns (UserReply);`. The protobuf compiler and gRPC plugin generate message classes and a client stub/server interface. The server implements `GetUser`; the client calls its generated method with a `UserRequest` rather than constructing an HTTP request. The client library serializes the message, sends it on an HTTP/2 stream, and interprets the response and final gRPC status.

This is a **division of responsibilities**: the RPC contract says *which operation* is called; protobuf normally says *how structured values become bytes*; HTTP/2 says *how requests and responses travel concurrently*. Protobuf is the default, not a requirement of every gRPC integration. gRPC adds method naming, metadata, status codes, deadlines, and cancellation above the transport.

gRPC supports four method shapes: one request/one response (**unary**), one request/many responses (**server streaming**), many requests/one response (**client streaming**), and streams in both directions (**bidirectional streaming**). Messages remain ordered within a stream; bidirectional peers can send independently. A deadline prevents indefinite waiting, but timeout or cancellation does not prove the server never performed a side effect. As with any [[remote-procedure-call]], retries require care.

It is useful for strongly typed service-to-service APIs, especially across languages, and for streaming. The tradeoff is a shared contract and compatible generated code; raw binary traffic is less readable than a text API. gRPC does not itself provide exactly-once execution or application authorization.

## Prerequisites

- [[remote-procedure-call]]
- [[protocol-buffers]]
- [[http-2]]

## Sources

- [gRPC introduction](https://grpc.io/docs/what-is-grpc/introduction/).
- [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/).
