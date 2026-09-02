---
id: minimum-cost-flow
title: Minimum-Cost Flow
summary: Minimum-cost flow chooses a feasible capacitated flow that satisfies supplies and demands while minimizing total per-unit transport cost.
type: concept
tags: [algorithms]
prereqs: [flow-network, residual-network, shortest-path]
sources: [https://developers.google.com/optimization/flow/mincostflow]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Minimum-Cost Flow

## Summary

**Minimum-cost flow** routes required supply through a [[flow-network]] while respecting capacities and conservation, and among all feasible routings chooses the one with the smallest sum of flow times unit cost.

## Grounded explanation

Each directed edge $(u,v)$ has capacity $c_{uv}$, unit cost $k_{uv}$, and chosen flow $f_{uv}$. Each vertex has balance $b_v$: positive for supply, negative for demand, and zero for transshipment. Feasibility requires

$$0\le f_{uv}\le c_{uv},\qquad
\sum_w f_{vw}-\sum_u f_{uv}=b_v.$$

The objective is

$$\min \sum_{(u,v)} k_{uv}f_{uv}.$$

The balance equation is the conservation law from [[flow-network]], extended so a source adds its declared supply and a sink consumes its declared demand.

A successive-shortest-path method starts with zero flow, views editable choices through the [[residual-network]], and repeatedly sends as much as possible along a minimum-cost [[shortest-path]] from an unsatisfied supply to an unsatisfied demand. Reverse residual edges carry the negative of the original edge's cost, so a later augmentation can undo an expensive earlier decision.

### Worked example

Factory $S$ supplies 3 units. Customer $T$ demands 3. There are two routes: direct edge $S\to T$ has capacity 1 and cost 1 per unit; route $S\to A\to T$ has capacities 3 and costs 2 and 1 per unit. Send 1 unit directly for cost $1\times1=1$. The remaining 2 units take the indirect route, each costing $2+1=3$, for $2\times3=6$. Total cost is $7$. Sending all three indirectly would cost $9$, while sending more than one directly violates capacity.

The result is not merely a cheap path: it is a globally feasible assignment across all edges. Applications include shipping, assignment, and scheduling whenever quantities, bottlenecks, and per-unit costs coexist.

## Prerequisites

- [[flow-network]]
- [[residual-network]]
- [[shortest-path]]

## Sources

- Google OR-Tools, “Minimum Cost Flows” — supplies, demands, capacities, unit costs, conservation, and objective.
