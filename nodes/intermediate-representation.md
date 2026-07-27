---
id: intermediate-representation
title: Intermediate representation
summary: An intermediate representation is a shared, tool-independent form of a program or model that a producer emits and multiple consumers can validate, transform, or execute.
type: concept
tags: [ml/model-portability]
prereqs: [graph]
sources: [https://onnx.ai/onnx/repo-docs/IR.html]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Intermediate representation

## Summary

An **intermediate representation (IR)** is a shared, tool-independent form of a
program or model. A producer translates its private form into the IR, and different
consumers can validate, transform, or execute that same representation.

## Grounded explanation

Two tools rarely store a calculation in exactly the same internal form. Directly
supporting every producer-to-consumer pair creates a separate translator for every
pair. An IR inserts a stable contract in the middle: each producer emits one agreed
form, and each consumer reads that form. With three producers and two consumers,
pairwise translation needs `3 × 2 = 6` paths; a shared IR needs `3 + 2 = 5` adapters,
and each new tool adds only one more.

Many IRs describe structure as a [[graph]]. Vertices record operations or objects,
edges record relationships or value flow, and metadata fixes details that names
alone cannot express. The IR is not necessarily executable by itself. Its purpose
is to preserve meaning across the boundary: a consumer may interpret it directly,
optimize it, or translate it again, provided the observable calculation stays the
same.

**Worked instance.** Producer `P` stores “multiply, then add” in its own object
tree, while consumers `C1` and `C2` use different internal layouts. `P` emits the
shared graph `input → multiply → temporary → add → output`. Both consumers rebuild
their preferred structures from that one graph. Portability comes from agreeing on
the middle representation, not from forcing every tool to share an implementation.

## Prerequisites

- [[graph]]

## Sources

- https://onnx.ai/onnx/repo-docs/IR.html
