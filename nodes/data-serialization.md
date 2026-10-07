---
id: data-serialization
title: Data serialization
summary: Data serialization encodes a structured value into bytes according to an agreed format so another process can reconstruct its meaning.
type: concept
tags: [networking]
prereqs: []
sources: [https://protobuf.dev/overview/]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Data serialization

## Summary

**Data serialization** turns a structured value into bytes under a shared format; deserialization interprets the bytes to reconstruct the value. Sending bytes alone is not enough: both sides must agree on their meaning.

## Grounded explanation

Imagine a record with `name = "Ada"` and `age = 37`. A sender can encode its fields as text or binary numbers. The receiver must know where each field begins, its type, and which version of the format applies. Otherwise the same bytes may be interpreted differently.

Serialization determines the representation of a message; the network carries that representation. A schema can define field names, types, and compatibility rules so programs in different languages agree on the same data. A useful test is a round trip: decoding an encoded value should preserve its intended information. That alone does not guarantee compatibility between different programs or schema versions.

## Prerequisites

None. This is the chosen starting point for structured messages.

## Sources

- [Protocol Buffers overview](https://protobuf.dev/overview/) — one concrete serialization system.

