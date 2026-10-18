---
id: cluster-bin-packing
title: Cluster Bin Packing
summary: Cluster bin packing concentrates compatible resource requests onto fewer nodes to preserve useful free nodes while respecting placement constraints.
type: concept
tags: [os/virtualization]
prereqs: [kubernetes-pod]
sources: [https://github.com/kai-scheduler/KAI-Scheduler]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# Cluster Bin Packing

## Meaning

Bin packing is a placement heuristic: fit workloads tightly into eligible nodes rather than spreading every request evenly. Its benefit is often preserving whole free nodes for large future groups or for powering down idle capacity.

## Mechanism

Treat each node as a capacity vector and each [[kubernetes-pod]] as a request vector. A placement is feasible only when all dimensions and labels fit; a low remaining GPU count alone does not prove a good fit. Scoring rules may prefer already-used nodes, but online arrivals mean a locally attractive choice can hurt a future job. This cluster-level fragmentation is distinct from unused memory blocks inside a GPU allocator. Packing can increase interference and correlated failure exposure; spreading is an alternative when resilience or contention dominates. Neither is globally optimal without assumptions about future demand and constraints.

## Worked example

Two nodes each have eight GPUs. Placing two three-GPU pods on one node leaves capacities (2,8); spreading them leaves (5,5). Both use six GPUs, but only the packed result can immediately accept an eight-GPU single-node job. Conversely, if those two pods must survive a single-node failure, spreading may be required. If each also requests 60 CPU cores and a node has only 96, packing both is infeasible despite the GPU arithmetic. Evaluate realistic arrival traces, future unschedulable gangs, utilization, completion time, and failure behavior. Do not conflate high occupancy with a faster application.

## Check your understanding

Is total free capacity enough to characterize fragmentation? No. The sizes, types, and topology of the free pieces determine which future requests fit.

## Prerequisites

- [[kubernetes-pod]]

## Sources

- <https://github.com/kai-scheduler/KAI-Scheduler>
