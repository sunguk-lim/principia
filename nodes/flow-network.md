---
id: flow-network
title: Flow Network
summary: A flow network is a directed graph whose arcs carry bounded amounts and whose internal vertices conserve inflow and outflow.
type: concept
tags: [algorithms]
prereqs: [graph, arithmetic]
sources: [https://developers.google.com/optimization/flow/maxflow]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Flow Network

## Summary

A **flow network** turns a [[graph]] into a transport system: each directed edge has a capacity, each edge receives a nonnegative flow no larger than that capacity, and every ordinary vertex sends out exactly what enters it.

## Grounded explanation

Let $G=(V,E)$ be a directed [[graph]]. For each edge $(u,v)$, let $c(u,v)\ge 0$ be its capacity and $f(u,v)$ its chosen flow. A feasible flow obeys

$$0\le f(u,v)\le c(u,v)$$

and, for every vertex that is neither a source nor a sink,

$$\sum_{u:(u,v)\in E} f(u,v)=\sum_{w:(v,w)\in E} f(v,w).$$

The second equation is conservation: an intermediate vertex cannot create or destroy material. Sources inject flow and sinks remove it. The value of a source-to-sink flow is the total amount leaving the source, computed with ordinary [[arithmetic]].

### Worked example

Take edges $s\to a$ with capacity 4, $s\to b$ with capacity 3, $a\to t$ with capacity 2, $a\to b$ with capacity 2, and $b\to t$ with capacity 4. Choose flows $2,3,2,0,3$ in that order. Vertex $a$ receives 2 and sends 2; vertex $b$ receives 3 and sends 3. Every flow is within capacity, so the assignment is feasible and transports $2+3=5$ units from $s$ to $t$.

Capacity describes what is allowed, not what must be used. Conservation is the invariant that lets local edge choices represent one coherent end-to-end movement.

## Prerequisites

- [[graph]]
- [[arithmetic]]

## Sources

- Google OR-Tools, “Maximum Flows” — capacities, conservation, sources, and sinks.
