---
id: computation-graph
title: Computation graph
summary: A computation graph represents a calculation as operation nodes connected by named tensor values, so dependencies determine a valid execution order.
type: concept
tags: [ml/model-portability]
prereqs: [graph, tensor]
sources: [https://onnx.ai/onnx/repo-docs/IR.html]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Computation graph

## Summary

A **computation graph** represents a calculation as operation nodes connected by
the values they produce and consume. An edge means “this output is that operation's
input,” so the graph records both the calculation and its dependency order.

## Grounded explanation

Start with a [[graph]]: vertices are things and directed edges say which thing feeds
which next thing. In a computation graph, each vertex invokes an operation, while
the edges carry named [[tensor]] values. Graph inputs enter without a producing
vertex; graph outputs leave after their final consumer.

The direction gives an execution rule. An operation can run only after every input
value it needs exists. If node `A` produces `h` and node `B` consumes `h`, then `A`
must run before `B`. A graph with no dependency cycle can be ordered so every
producer appears before its consumers. That order exposes parallelism too: two
nodes whose inputs are ready and which do not depend on each other may run together.

**Worked instance.** Let input tensor `x = [2, 3]`. Node `Multiply` consumes `x`
and constant tensor `[4, 5]`, producing named value `p = [8, 15]`. Node `Add`
consumes `p` and `[1, -3]`, producing output `y = [9, 12]`. The dependency graph is
`x → Multiply → p → Add → y`. `Add` cannot run first because `p` does not yet
exist; naming the connecting value makes that constraint explicit and portable.

## Prerequisites

- [[graph]]
- [[tensor]]

## Sources

- https://onnx.ai/onnx/repo-docs/IR.html
