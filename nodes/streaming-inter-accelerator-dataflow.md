---
id: streaming-inter-accelerator-dataflow
title: "Streaming Inter-Accelerator Dataflow"
summary: "Streaming inter-accelerator dataflow pipelines bounded pieces of dependent state between devices while preserving transfer ordering, buffer ownership and backpressure."
type: concept
tags: [computing/performance]
prereqs: [spatial-dataflow-execution, message-passing]
sources: [https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/p2p.html]
status: explained
created: 2026-11-20
updated: 2026-11-20
---

# Streaming Inter-Accelerator Dataflow

## Meaning

Streaming inter-accelerator dataflow sends bounded pieces of a producer's output to another device as the downstream computation becomes ready. It extends [[spatial-dataflow-execution]] beyond a single device. The objective is to overlap useful computation and communication or reduce unnecessary staging; it cannot remove the cost of moving required information.

## Mechanism

Partition an intermediate into pieces with explicit sequence identity, shape, type and destination. A receiver may process one ready piece while another travels. [[message-passing]] still requires a compatible communication contract and a completion event before data is consumed or a send buffer is overwritten. NCCL's primary point-to-point documentation describes matching sends and receives, grouped operations for concurrent progress and ordering constraints. Those APIs are a concrete communication substrate, not proof that an entire model has become a spatial hardware pipeline.

Bounded queues create backpressure: when downstream capacity fills, upstream production must slow or retain data elsewhere. Buffering, network topology, link bandwidth and transfer startup cost join the compute-stage constraints of [[pipeline-bottleneck-localization]]. Small pieces expose earlier overlap but add more dispatch and bookkeeping; large pieces amortize transfer overhead while delaying the consumer. A direct device transfer may avoid host staging, but can still touch device memory and need synchronization.

Distinguish a layer pipeline from expert dispatch. Neighboring stages can pass sequential layer outputs; routed experts may need many-to-many traffic and result combination. Placement and communication semantics differ. Neither pattern implies that every transfer is free, that links are saturated or that all stages can remain busy for a single dependent token.

## One example

Suppose a producer emits four chunks, a link takes two microseconds per chunk and a consumer takes three. With independent resources and no startup overhead, consuming the first chunk finishes after five microseconds and subsequent chunks finish every three. The fourth finishes after fourteen. Serial transfer-then-compute for all chunks would take twenty. These hypothetical figures illustrate overlap; they are not a bound for a system where producer work, shared links or synchronization dominate.

## Check your understanding

Will smaller chunks always improve latency? No. Measure per-stage and per-link utilization, queue occupancy, idle gaps, transfer count, buffer lifetime and end-to-end latency under representative contention. Test delayed or failed peers, shape mismatches and cancellation without reusing an in-flight buffer. Compare an optimized materialized baseline at the same numerical and workload contract. A named vendor communication unit is one implementation detail, not sufficient evidence for a device-family ranking.

## Prerequisites

- [[spatial-dataflow-execution]]
- [[message-passing]]

## Sources

- <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/p2p.html>
