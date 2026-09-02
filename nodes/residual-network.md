---
id: residual-network
title: Residual Network
summary: A residual network records how much a current flow can still increase on each edge and how much of that flow can be undone through a reverse edge.
type: concept
tags: [algorithms]
prereqs: [flow-network]
sources: [https://cp-algorithms.com/graph/edmonds_karp.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Residual Network

## Summary

A **residual network** is the editable view of a current [[flow-network]]: a forward residual edge shows unused capacity, while a reverse residual edge shows flow that can be cancelled and rerouted.

## Grounded explanation

For an original edge $(u,v)$ with capacity $c(u,v)$ and current flow $f(u,v)$, the forward residual capacity is

$$r(u,v)=c(u,v)-f(u,v).$$

The residual graph also has a reverse edge $(v,u)$ with capacity

$$r(v,u)=f(u,v).$$

Sending one unit forward consumes one unit of unused capacity. Sending one unit on the residual reverse edge subtracts one unit from the earlier choice. That reverse edge is the key: a greedy early route is not permanent.

### Worked example

Suppose edge $s\to a$ has capacity 5 and currently carries 3. Its residual view contains $s\to a$ with capacity $5-3=2$ and $a\to s$ with capacity 3. If a later route needs to reclaim one unit, sending one residual unit $a\to s$ changes the original flow from 3 to 2. The new residual capacities become 3 forward and 2 reverse.

An augmenting algorithm searches this editable network for a source-to-sink path with positive residual capacity. It can therefore combine new forward choices with cancellations of old choices while preserving feasibility in the original network.

## Prerequisites

- [[flow-network]]

## Sources

- cp-algorithms, “Maximum flow — Ford–Fulkerson and Edmonds–Karp” — residual capacities and reverse edges.
