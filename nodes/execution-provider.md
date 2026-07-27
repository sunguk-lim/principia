---
id: execution-provider
title: Execution provider
summary: An execution provider lets a runtime ask a hardware-specific backend which graph regions it can execute and then delegates those regions through a common interface.
type: concept
tags: [ml/model-portability]
prereqs: [computation-graph, operator-set, graph]
sources: [https://onnxruntime.ai/docs/execution-providers/, https://onnxruntime.ai/docs/reference/high-level-design.html]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Execution provider

## Summary

An **execution provider** lets a runtime ask a hardware-specific backend which
parts of a model it can execute. The runtime assigns supported subgraphs to that
provider through one common interface and sends unsupported work to another provider.

## Grounded explanation

Each node in a [[computation-graph]] invokes an operation defined by an
[[operator-set]]. A hardware backend may implement only some of those operations,
types, and shapes. An execution provider reports that capability to the runtime,
supplies implementations for the claimed work, and manages the memory needed on its
device. The runtime remains responsible for the whole model and for connecting values
across provider boundaries.

Providers are considered in priority order. Using the node-edge connectivity of a
[[graph]], the first provider claims the largest regions it can handle; the next provider considers what remains. A default provider
comes last and supplies fallback implementations, so partial accelerator support does
not make the entire model unusable. Each claimed connected region becomes a subgraph
owned by one provider, which may execute its nodes individually or compile the whole
region into a specialized operation.

**Worked instance.** Consider the path `MatMul → Add → Custom`. A preferred
accelerator reports support for `MatMul` and `Add` but not `Custom`, so it claims the
first two connected nodes as one subgraph. The default CPU provider claims `Custom`.
The runtime executes the accelerator subgraph, transfers its named output across the
provider boundary, and executes `Custom` on the CPU. Without the common provider
interface, the application would need separate scheduling code for every backend.

## Prerequisites

- [[computation-graph]]
- [[operator-set]]
- [[graph]]

## Sources

- https://onnxruntime.ai/docs/execution-providers/
- https://onnxruntime.ai/docs/reference/high-level-design.html
