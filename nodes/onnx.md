---
id: onnx
title: ONNX (Open Neural Network Exchange)
summary: ONNX is an open, runtime-agnostic intermediate representation that exchanges machine-learning models as typed computation graphs with versioned operator semantics.
type: concept
tags: [ml/model-portability]
prereqs: [intermediate-representation, computation-graph, operator-set, neural-network, graph]
sources: [https://onnx.ai/onnx/intro/concepts.html, https://onnx.ai/onnx/repo-docs/IR.html, https://onnx.ai/onnx/repo-docs/Versioning.html]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# ONNX (Open Neural Network Exchange)

## Summary

**ONNX (Open Neural Network Exchange)** is an open, runtime-agnostic
[[intermediate-representation]] for exchanging machine-learning models. It packages
a typed [[computation-graph]] with versioned [[operator-set]] imports so a model
exported by one tool can be validated and executed or translated by another.

## Grounded explanation

A trained [[neural-network]] has parameters and a forward calculation, but every
training framework may store them differently. ONNX defines the common contract in
the middle. A model records an IR version, imported operator-set domains and
versions, metadata, and a [[computation-graph]]. Its vertex-edge skeleton is a
[[graph]]; its specialized computation meaning comes from named inputs and outputs,
operation nodes, constant parameter values, and type-and-shape information for the
values flowing between nodes.

The pieces divide responsibility cleanly. The [[computation-graph]] says **which
operation consumes which named value**. Each [[operator-set]] import says **which
published schema gives that operation its meaning**. The
[[intermediate-representation]] specifies how those pieces and their metadata fit
together. A producer exports its private model into this contract; a consumer checks
the IR and operator-set versions before interpreting, optimizing, or translating it.
ONNX specifies the model, not the execution strategy: a consumer may interpret the
[[computation-graph|computation structure]], generate code, or map operations to specialized hardware.

**Worked instance.** Export the two-output affine calculation `y = xW + b` with
`x = [2, 3]`, parameter `W` whose rows are `[1, 4]` and `[2, 5]`, and
`b = [1, -3]`. The ONNX [[computation-graph|computation structure]]
contains a `MatMul` node producing `m`, then an `Add` node consuming `m` and `b`:

1. `MatMul([2,3], W)` produces `m = [2×1 + 3×2, 2×4 + 3×5] = [8, 23]`.
2. `Add(m, b)` produces `y = [8+1, 23-3] = [9, 20]`.

The file also records the shapes and element types of `x`, `W`, `b`, `m`, and `y`,
plus the operator-set version that defines `MatMul` and `Add`. A second framework
does not need the producer's classes or source code; it reconstructs the same two
steps from the shared names, dependencies, types, constants, and schemas. That is
the exchange guarantee. It does not promise identical speed or internal layout,
because those remain choices of the consuming runtime.

## Prerequisites

- [[intermediate-representation]]
- [[computation-graph]]
- [[operator-set]]
- [[neural-network]]
- [[graph]]

## Sources

- https://onnx.ai/onnx/intro/concepts.html
- https://onnx.ai/onnx/repo-docs/IR.html
- https://onnx.ai/onnx/repo-docs/Versioning.html
