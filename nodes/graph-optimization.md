---
id: graph-optimization
title: Graph optimization
summary: Graph optimization rewrites a computation graph into an equivalent graph that performs less work, moves less data, or better matches the target executor.
type: concept
tags: [ml/model-portability]
prereqs: [computation-graph, graph]
sources: [https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Graph optimization

## Summary

**Graph optimization** rewrites a [[computation-graph]] into an equivalent graph
that performs less work, moves less data, or better matches the target executor.
The structure changes, but every permitted input must still produce the same result.

## Grounded explanation

A [[computation-graph]] makes calculation structure explicit: its [[graph]] skeleton
provides nodes and edges that a tool can change before execution. A rewrite matches a known pattern, checks the
conditions that make the replacement valid, and substitutes a cheaper pattern.
The key invariant is **semantic preservation**: optimization may change nodes and
edges, but not the calculation observed at the graph outputs.

Three common rewrites show the mechanism. **Constant folding** evaluates a region
whose inputs are all fixed constants and stores its result, so that region does no
runtime work. **Elimination** removes an identity or other redundant node and wires
its input directly to its consumers. **Fusion** replaces a chain such as
`MatMul → Add` with one node whose implementation performs both operations without
materializing the intermediate value. Layout rewrites may arrange values differently
when the selected executor can process that arrangement faster.

**Worked instance.** Start with `x → Identity → Add(2, 3) → Multiply`. Folding
`Add(2, 3)` produces constant `5`. Eliminating `Identity` connects `x` directly to
`Multiply`. The original path executes three nodes; the optimized path executes one
node, `Multiply(x, 5)`. For `x = 4`, both paths return `20`, but the optimized graph
avoids two runtime operations. A rewrite is acceptable because this equality holds
for every valid `x`, not merely for the example.

## Prerequisites

- [[computation-graph]]
- [[graph]]

## Sources

- https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html
