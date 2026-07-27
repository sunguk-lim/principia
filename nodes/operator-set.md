---
id: operator-set
title: Operator set
summary: An operator set is a versioned vocabulary of operation schemas that fixes each operation's name, inputs, outputs, attributes, types, and meaning.
type: concept
tags: [ml/model-portability]
prereqs: [tensor]
sources: [https://onnx.ai/onnx/repo-docs/IR.html, https://onnx.ai/onnx/operators/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Operator set

## Summary

An **operator set** is a versioned vocabulary of operation schemas. Each schema
fixes an operation's name, accepted inputs and outputs, attributes, allowed types,
and meaning, giving producers and consumers the same contract.

## Grounded explanation

An operation name alone is ambiguous. To execute `Add`, a consumer must know how
many inputs it accepts, which [[tensor]] element types are legal, how shapes combine,
and what output values must result. An **operator schema** supplies that contract.
An operator set groups such schemas under a domain and publishes a numbered snapshot.

Versioning protects compatibility. A model imports a particular `(domain, version)`
pair, and a consumer either supports every operation the model uses from that
snapshot or rejects the model. A later snapshot may add a type or introduce a new
schema version, but a stable old schema keeps its established meaning. The model
therefore does not merely say “use Add”; it says which published contract defines
that Add.

**Worked instance.** Suppose snapshot 13 permits `Add` for `float32` tensors, while
snapshot 14 also permits `int8`. A model containing `int8` inputs and importing
version 14 is valid under that contract. A consumer supporting only version 13 must
reject or convert it rather than silently guessing. The explicit version turns an
operation name into a reproducible interface.

## Prerequisites

- [[tensor]]

## Sources

- https://onnx.ai/onnx/repo-docs/IR.html
- https://onnx.ai/onnx/operators/
