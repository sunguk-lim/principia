---
id: http-2
title: HTTP/2
summary: HTTP/2 preserves HTTP request and response semantics while carrying them as binary frames on multiplexed streams over one connection.
type: concept
tags: [networking]
prereqs: [http]
sources: [https://httpwg.org/specs/rfc9113.html]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# HTTP/2

## Summary

**HTTP/2** keeps the request and response meaning of [[http]] but changes the wire format: messages are split into binary frames assigned to streams. Multiple streams can be active on one connection.

## Grounded explanation

The [[http]] methods, headers, and responses still exist. Instead of sending each complete message as a contiguous text exchange, HTTP/2 divides headers and bodies into frames. Each frame carries a stream identifier, so frames from different requests can be interleaved and reassembled by the receiver.

A client can start requests A and B without waiting for A's response before sending B. Their frames share one connection but belong to separate streams. Per-stream flow control limits how much data a receiver must buffer. Long-lived streams also support streaming APIs.

Multiplexing reduces application-layer blocking between requests, but all streams on an ordinary HTTP/2 connection still share its underlying transport. A lost transport packet can delay progress on that connection. HTTP/2 is not an RPC service definition by itself.

## Prerequisites

- [[http]]

## Sources

- [RFC 9113: HTTP/2](https://httpwg.org/specs/rfc9113.html).
