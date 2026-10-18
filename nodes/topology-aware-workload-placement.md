---
id: topology-aware-workload-placement
title: Topology-Aware Workload Placement
summary: Topology-aware placement assigns cooperating workloads to compatible hardware locations according to communication and availability constraints.
type: concept
tags: [os/virtualization]
prereqs: [kubernetes-pod, tensor-parallelism]
sources: [https://github.com/kai-scheduler/KAI-Scheduler/tree/main/docs/topology, https://github.com/ai-dynamo/grove]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# Topology-Aware Workload Placement

## Meaning

Having enough GPUs in the cluster does not mean they are arranged usefully for one application. Placement must consider hardware compatibility and the communication links between the chosen devices, not only a total resource count.

## Mechanism

A [[kubernetes-pod]] requests resources on a node; groups add constraints spanning nodes or accelerator domains. [[tensor-parallelism]] repeatedly communicates between devices, making bandwidth and latency part of a placement decision. Hard constraints reject placements outside a required domain; soft preferences rank feasible placements. Hardware node pools restrict which nodes are eligible, for example by accelerator family or memory capacity. A pool label expresses a selection policy, not proof of a fast interconnect or trustworthy isolation. Concentration can improve locality while spreading replicas across domains improves fault tolerance; these objectives can conflict.

## Worked example

Two domains each have four GPUs, but only two are free in each. A four-GPU group requiring one domain cannot be placed even though the cluster has four free GPUs. A request that allows cross-domain placement may run, but its communication cost must be measured. If an eight-device model instance requires a high-memory accelerator pool, four devices in that pool plus four incompatible devices elsewhere do not satisfy it. Compare queue delay against running-time improvements, and test what happens when labels, links, or nodes change. Report actual topology and collective-communication measurements rather than assuming all GPUs or all links are interchangeable.

## Check your understanding

Should every replica always be packed into the fastest single domain? No. Resource fragmentation, queueing, correlated failures, and replica availability may favor a different placement.

## Prerequisites

- [[kubernetes-pod]]
- [[tensor-parallelism]]

## Sources

- <https://github.com/kai-scheduler/KAI-Scheduler/tree/main/docs/topology>
- <https://github.com/ai-dynamo/grove>
