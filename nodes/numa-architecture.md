---
id: numa-architecture
title: NUMA Architecture
summary: A NUMA architecture partitions processors and memory into nodes so local memory is faster to access than memory attached to another node.
type: concept
tags: [os/memory]
prereqs: [memory-hierarchy]
sources: [https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# NUMA Architecture

## Summary

A **non-uniform memory access (NUMA) architecture** divides a machine into hardware nodes, each containing processors and directly attached memory; every processor can address all memory, but local-node access has lower latency and usually higher bandwidth than remote-node access.

## Grounded explanation

A uniform shared-memory machine presents one memory cost. NUMA preserves one addressable memory space while adding distance. A processor reaches its local memory controller directly; reaching another node's memory crosses a socket-to-socket interconnect. NUMA is therefore an extra physical level in the [[memory-hierarchy]]: the same RAM capacity is not equally close to every processor.

### Worked example

Consider two NUMA nodes. Node 0 has CPUs 0–7 and 64 GB of RAM; node 1 has CPUs 8–15 and 64 GB. A thread on CPU 2 repeatedly scans a 1 GB array. If the array's pages reside on node 0, accesses use the local path. If they reside on node 1, every cache miss crosses the inter-node link. The program still returns identical values, but remote latency and shared-link traffic can reduce throughput.

The topology is not simply “two CPUs.” It is a distance map among processor sets, memory controllers, and often nearby devices. Correctness does not require locality; performance does. That is why NUMA problems are often silent: the workload works while consuming more time and interconnect bandwidth.

## Prerequisites

- [[memory-hierarchy]]

## Sources

- Linux kernel documentation, “NUMA Memory Policy” — memory nodes, local allocation, and distance-based fallback.
