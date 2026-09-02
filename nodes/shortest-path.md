---
id: shortest-path
title: Shortest Path
summary: A shortest path minimizes the sum of edge costs from a start vertex to a destination in a weighted graph.
type: concept
tags: [algorithms]
prereqs: [graph, heap]
sources: [https://cp-algorithms.com/graph/dijkstra.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Shortest Path

## Summary

A **shortest path** in a weighted [[graph]] is a route whose edge weights add to the smallest possible total between two vertices.

## Grounded explanation

For a path $v_0,v_1,\ldots,v_k$ with edge weight $w(v_{i-1},v_i)$, its length is

$$L=\sum_{i=1}^{k}w(v_{i-1},v_i).$$

When all edge weights are nonnegative, Dijkstra's method maintains a tentative distance for each vertex. A [[heap]] repeatedly returns the unsettled vertex with the smallest tentative distance. Once that vertex is removed, no later route can improve it: every alternative must first reach another unsettled vertex whose distance is at least as large and then add a nonnegative edge.

### Worked example

Let edges be $A\to B$ of weight 4, $A\to C$ of weight 1, $C\to B$ of weight 2, and $B\to D$ of weight 1. Start with $d(A)=0$ and all other distances infinite. Settling $A$ gives $d(B)=4$ and $d(C)=1$. The heap returns $C$, which improves $B$ to $1+2=3$. Then $B$ improves $D$ to $3+1=4$. The shortest route is $A\to C\to B\to D$ with total 4, not the visually shorter three-vertex route through the weight-4 edge.

Negative edges break the settling argument because a later edge could reduce an already settled distance. The concept is the minimizing route; Dijkstra's algorithm is one valid mechanism under the nonnegative-weight condition.

## Prerequisites

- [[graph]]
- [[heap]]

## Sources

- cp-algorithms, “Dijkstra's algorithm” — nonnegative-weight invariant and priority-queue execution.
