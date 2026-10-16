---
id: moe-expert-offloading
title: Mixture-of-Experts Expert Offloading
summary: Expert offloading keeps selected MoE weights in host memory and transfers or caches them on demand, exchanging GPU capacity for transfer latency and scheduling complexity.
type: concept
tags: [ml/llm/inference]
prereqs: [mixture-of-experts, llm-inference-memory-budget, gpu-data-flow]
sources: [https://arxiv.org/abs/2401.14361]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Mixture-of-Experts Expert Offloading

## Summary

A [[mixture-of-experts]] model activates only a subset of experts per token, but all experts still occupy storage somewhere. **Expert offloading** places some weights outside GPU memory and moves selected experts to the device when required.

## Grounded explanation

Sparse activation reduces arithmetic per token; it does not make inactive weights vanish from the [[llm-inference-memory-budget]]. When GPU capacity is insufficient, host RAM or storage can hold less frequently used experts. A GPU-side expert cache retains weights likely to be routed again. On a miss, the system transfers an expert before its kernel can run. The transfer path, placement policy, and schedule become part of inference, not a free memory optimization. MoE-Infinity is primary research on activation-aware expert caching for limited-memory machines.

Suppose a layer has 64 experts but routes each token to two. Keeping eight experts resident may serve repeated common routes cheaply, but a cold or changing route triggers host-to-device transfers. Batch size and route diversity matter: a single stream of similar tokens can reuse a cache, while many concurrent requests may activate most experts and erase the advantage. Quantizing expert weights can shrink both storage and transfer bytes, but it adds accuracy and kernel-support questions. [[gpu-data-flow]] clarifies why PCIe or other interconnect bandwidth and synchronization can dominate even when GPU arithmetic is sparse.

Compare this design with all-GPU residency, more GPU capacity, a smaller dense model, and lower-bit weights without offloading. Measure cache hit rate and eviction, expert transfer bytes, p50/p95 decode latency, prefill throughput, host RAM, VRAM, and concurrent-request interference. Keep model, tokenizer, sampling, and task set fixed when assessing output quality. A claim that a model “fits on two GPUs” should explicitly include host RAM and transfer costs; hardware purchase price alone is not total inference cost.

## Prerequisites

- [[mixture-of-experts]]
- [[llm-inference-memory-budget]]
- [[gpu-data-flow]]

## Sources

- [MoE-Infinity](https://arxiv.org/abs/2401.14361): activation-aware expert caching and offloading under constrained GPU capacity.
