---
id: fleet-inference-orchestration
title: Fleet Inference Orchestration
summary: Fleet inference orchestration coordinates request routing, capacity control and reusable model state across engine instances rather than treating single-engine optimization as a complete serving architecture.
type: concept
tags: [ml/llm/inference]
prereqs: [cache-aware-inference-routing, tiered-kv-cache, latency-driven-inference-scaling]
sources: [https://docs.nvidia.com/dynamo/dev/knowledge-base/overview, https://github.com/ai-dynamo/dynamo]
status: explained
created: 2026-10-31
updated: 2026-10-31
---

# Fleet Inference Orchestration

## Meaning

A fleet orchestration layer coordinates multiple inference engine instances into one service. An engine may already span several GPUs; the architectural boundary is responsibility, not device count. The engine executes model work and manages its local scheduling, while the fleet layer coordinates which instance serves a request, how much capacity is ready, and where reusable request state can be found.

## Mechanism

Separate three paths. The request path makes latency-sensitive decisions using [[cache-aware-inference-routing]] and streams results. The control path changes capacity through [[latency-driven-inference-scaling]]. The state path publishes cache availability and moves compatible state across workers or storage tiers through [[tiered-kv-cache]]. In [[prefill-decode-disaggregation]], one request crosses a prompt-to-generation boundary and needs a correct state handoff.

These are coupled but not interchangeable. More ready workers may hold no useful prefixes. A high cache-hit estimate may point to an overloaded worker. A scaling decision can succeed while startup has not completed, and stale state events can direct a request toward an evicted prefix. Give each boundary explicit identities, compatibility rules, readiness signals and fallback behavior. Primary Dynamo architecture documentation describes these separate planes; it does not prove arbitrary backend or feature combinations interchangeable.

## Worked example

A request repeats a long prefix. Worker A has a compatible prefix and an estimated 70 milliseconds of queue delay; B has no prefix and a 10-millisecond queue. Suppose remaining prefill costs 5 milliseconds on A and 40 on B. Before other costs, A's first-token estimate is `70+5=75` milliseconds and B's is `10+40=50`. Reuse alone would choose A, while the workload-conditioned decision chooses B.

Now suppose prefill and decode run in separate pools. The request also pays a measured handoff cost and waits for a ready decode worker. If both choices share those costs, B remains preferable; if their transfer paths differ, recompute the full estimate. A planner may add capacity for sustained overload, but that slower action does not replace today's request decision. This example links routing, state and control rather than reducing orchestration to a list of optimization flags.

## Trade-offs and validation

Compare with a simpler engine-plus-load-balancer baseline at equal model quality and total resources. Test stale discovery, eviction, worker restart, interrupted handoff and overload, retaining request and tenant boundaries. Measure first-token, inter-token and completion latency, state-transfer bytes, recomputation, errors, readiness and cost. Component-level success and isolated kernel speedups do not establish fleet-level improvement.

## Sources

- <https://docs.nvidia.com/dynamo/dev/knowledge-base/overview>
- <https://github.com/ai-dynamo/dynamo>
