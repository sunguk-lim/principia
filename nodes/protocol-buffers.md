---
id: protocol-buffers
title: Protocol Buffers
summary: Protocol Buffers is a schema-based binary serialization format and code-generation toolchain for structured messages shared across programs and languages.
type: concept
tags: [networking]
prereqs: [data-serialization]
sources: [https://protobuf.dev/overview/]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Protocol Buffers

## Summary

**Protocol Buffers (protobuf)** defines structured messages in a `.proto` schema and serializes them into compact binary form. A compiler can generate language-specific code for constructing, encoding, and decoding those messages.

## Grounded explanation

In [[data-serialization]], both sides need an agreed interpretation of bytes. Protobuf supplies that agreement with a schema:

```proto
message UserRequest {
  int64 user_id = 1;
}
```

`user_id` is a typed field, and `1` is its stable **field number** on the wire. The sender encodes a value such as `user_id = 42`; the receiver uses the same schema to recover it. Field numbers, rather than source-code names, identify fields in the binary representation. Reusing a field number can therefore break compatibility even if the new name looks harmless.

Schemas can evolve by adding fields while older readers ignore fields they do not recognize, provided changes follow protobuf compatibility rules. Protobuf handles message structure and encoding; it does not specify how messages are transported or which remote operation to call. A service definition can also live in a `.proto` file, but serialization and RPC are different responsibilities.

## Prerequisites

- [[data-serialization]]

## Sources

- [Protocol Buffers overview](https://protobuf.dev/overview/).
