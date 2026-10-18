---
id: gpu-sharing-enforcement
title: GPU Sharing Enforcement
summary: GPU sharing needs separate contracts for memory limits, compute access, interference, and fault isolation rather than merely fractional resource accounting.
type: concept
tags: [os/virtualization]
prereqs: [gpu-memory-spaces, kubernetes-operator, device-driver]
sources: [https://github.com/kai-scheduler/gpu-fractioning, https://docs.nvidia.com/deploy/mps/index.html, https://docs.nvidia.com/datacenter/tesla/mig-user-guide/]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# GPU Sharing Enforcement

## Meaning

A scheduler can assign half a GPU on paper without enforcing any memory or compute boundary. GPU sharing is usable only when accounting, device exposure, and runtime enforcement agree about what each client may consume.

## Mechanism

Clients allocate in [[gpu-memory-spaces]]. A [[kubernetes-operator]] may reconcile node agents that set per-container limits before launch; the supported [[device-driver]] then enforces the actual device-memory boundary. Current fractioning implementations document version-specific driver and runtime requirements. A memory cap does not by itself reserve half the arithmetic throughput, isolate all failure modes, or establish a security boundary. Time slicing multiplexes execution; MPS supports cooperating process execution; hardware partitions expose a different isolation/resource contract. Device support and deployment configuration matter, so these choices are not synonyms or interchangeable guarantees.

## Worked example

Two clients share a 40-GiB device with configured caps of 12 and 20 GiB, leaving eight GiB before system overhead. If the first client attempts 14 GiB, enforced fractioning should reject or terminate that allocation according to its documented behavior rather than silently stealing from the second. Yet a compute-heavy first client may still slow the second unless compute scheduling provides a separate guarantee. Validate allocation overruns, process termination, restart, metric attribution, and noisy-neighbor latency on the exact supported stack. Compare exclusive allocation and hardware partitions as alternatives. Never infer real enforcement from a simulated device plugin or a “Ready” control-plane condition alone.

## Check your understanding

Does a 25% GPU memory allocation imply 25% of GPU throughput? No: memory capacity, compute scheduling, bandwidth contention, and workload shape are different constraints.

## Prerequisites

- [[gpu-memory-spaces]]
- [[kubernetes-operator]]
- [[device-driver]]

## Sources

- <https://github.com/kai-scheduler/gpu-fractioning>
- <https://docs.nvidia.com/deploy/mps/index.html>
- <https://docs.nvidia.com/datacenter/tesla/mig-user-guide/>
