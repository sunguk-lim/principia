---
id: directed-acyclic-graph
title: Directed Acyclic Graph
summary: A directed acyclic graph is a graph whose directed edges contain no path that starts at a vertex and follows arrows back to that same vertex.
type: concept
tags: [algorithms]
prereqs: [graph]
sources: [https://mathworld.wolfram.com/AcyclicDigraph.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Directed Acyclic Graph

## Summary

A **directed acyclic graph** (DAG) is a set of vertices joined by one-way edges with no directed cycle. Its arrows define a partial order: every edge can point from an earlier vertex to a later one in at least one linear arrangement.

## Grounded explanation

Start with a [[graph]], but give each edge an orientation $u\to v$. A directed path follows these arrow directions. The graph is acyclic when no nonempty directed path begins and ends at the same vertex.

This prohibition has a useful consequence. At least one vertex must have no incoming edge; otherwise, repeatedly following an incoming edge in a finite graph would eventually revisit a vertex and form a cycle. Remove such a vertex, repeat on what remains, and record the removal order. The result is a **topological order**, a list in which every edge points forward. Conversely, any graph with such an order cannot contain a directed cycle, because a cycle would have to keep moving forward and still return to its starting position.

### Worked example

Take vertices $A,B,C,D$ and edges

$$
A\to B,\qquad A\to C,\qquad B\to D,\qquad C\to D.
$$

Initially only $A$ has no incoming edge, so place it first. Removing $A$ leaves both $B$ and $C$ available; choose $B$ then $C$. Finally choose $D$. The order $(A,B,C,D)$ puts every arrow forward. The order $(A,C,B,D)$ also works, showing that a DAG can express constraints without forcing a unique total order.

Adding $D\to A$ would create the directed path $A\to B\to D\to A$. No topological order could put each of those three arrows forward, so the result would no longer be a DAG.

DAGs represent one-way dependency without feedback: build prerequisites, data transformations, and candidate causal directions can all be encoded as arrows while the no-cycle invariant prevents an object from becoming its own ancestor.

## Prerequisites

- [[graph]]

## Sources

- Wolfram MathWorld, “Acyclic Digraph” — definition of a directed graph containing no directed cycle.
