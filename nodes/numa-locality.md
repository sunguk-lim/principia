---
id: numa-locality
title: NUMA Locality
summary: NUMA locality aligns processor placement and memory placement so a workload accesses most of its pages and nearby devices from the same NUMA node.
type: concept
tags: [os/memory]
prereqs: [numa-memory-policy, processor-affinity]
sources: [https://docs.kernel.org/admin-guide/cgroup-v1/cpusets.html, https://ronaknathani.com/blog/2026/05/keeping-gpu-workloads-numa-local-in-kubernetes]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# NUMA Locality

## Summary

**NUMA locality** is the coordinated placement of execution and data on the same NUMA node: [[processor-affinity]] keeps work near a processor set, and [[numa-memory-policy]] places its pages near that set.

## Grounded explanation

Pinning a worker without its pages leaves remote memory traffic; placing pages without constraining execution lets the worker migrate away. NUMA locality requires both controls to describe one hardware neighborhood.

### Worked example

A GPU is attached to NUMA node 1. A serving worker uses 8 CPU threads and a 16-GB host buffer before copying batches to the GPU. In a mismatched placement, the threads run on node 0, the buffer is allocated on node 0, and transfers must cross the socket link before reaching the GPU on node 1. In a local placement, [[processor-affinity]] selects node-1 CPUs and [[numa-memory-policy]] allocates the buffer on node 1. CPU reads and host-to-device transfers avoid the extra hop.

The invariant is path alignment: CPU, memory pages, and relevant device should share the shortest available topology. A scheduler or orchestrator may express this as one topology-aware resource allocation, but the durable mechanism is not specific to any product.

Validate with topology inspection, per-node page counts, CPU placement, remote-access counters, and end-to-end latency. A lower remote-access ratio that does not improve the real workload is not sufficient evidence; pinning can also create contention or starve other tasks.

## Prerequisites

- [[numa-memory-policy]]
- [[processor-affinity]]

## Sources

- Linux kernel documentation, “CPUSETS” — coordinated CPU and memory-node restrictions.
- Ronak Nathani, “Keeping GPU Workloads NUMA-Local in Kubernetes” — GPU-workload placement boundary; product-specific details are not part of this node.
