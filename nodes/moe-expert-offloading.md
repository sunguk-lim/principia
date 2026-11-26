---
id: moe-expert-offloading
title: Mixture-of-Experts Expert Offloading
summary: Expert offloading keeps selected MoE weights in host memory and transfers or caches them on demand, exchanging GPU capacity for transfer latency and scheduling complexity.
type: concept
tags: [ml/llm/inference]
prereqs: [mixture-of-experts, llm-inference-memory-budget, gpu-data-flow]
sources: [https://arxiv.org/html/2401.14361v3, https://arxiv.org/abs/2401.14361]
status: explained
created: 2026-10-16
updated: 2026-11-27
---

# Mixture-of-Experts Expert Offloading

## Summary

A [[mixture-of-experts]] model activates only a subset of experts per token, but all experts still occupy storage somewhere. **Expert offloading** places some weights outside GPU memory and moves selected experts to the device when required.

## Grounded explanation

Sparse activation reduces arithmetic per token; it does not make inactive weights vanish from the [[llm-inference-memory-budget]]. When GPU capacity is insufficient, host RAM or storage can hold less frequently used experts. A GPU-side expert cache retains weights likely to be routed again. On a miss, the system transfers an expert before its kernel can run. The transfer path, placement policy, and schedule become part of inference, not a free memory optimization. MoE-Infinity is primary research on activation-aware expert caching for limited-memory machines.

Suppose a layer has 64 experts but routes each token to two. Keeping eight experts resident may serve repeated common routes cheaply, but a cold or changing route triggers host-to-device transfers. Batch size and route diversity matter: a single stream of similar tokens can reuse a cache, while many concurrent requests may activate most experts and erase the advantage. Quantizing expert weights can shrink both storage and transfer bytes, but it adds accuracy and kernel-support questions. [[gpu-data-flow]] clarifies why PCIe or other interconnect bandwidth and synchronization can dominate even when GPU arithmetic is sparse.

Compare this design with all-GPU residency, more GPU capacity, a smaller dense model, and lower-bit weights without offloading. Measure cache hit rate and eviction, expert transfer bytes, p50/p95 decode latency, prefill throughput, host RAM, VRAM, and concurrent-request interference. Keep model, tokenizer, sampling, and task set fixed when assessing output quality. A claim that a model “fits on two GPUs” should explicitly include host RAM and transfer costs; hardware purchase price alone is not total inference cost.

## Disk-backed paging and bandwidth bounds

A disk-backed expert store adds another tier before host-to-device transfer. GPU residency, host staging capacity and durable weight storage must be budgeted separately. A sparse route chooses few experts for one token, but the total model files can remain large. The union of requested experts across a batch, cache reuse and eviction determine actual reads; active-parameter count alone is not a disk-traffic estimate. Low-bit expert storage can reduce bytes but needs compatible unpacking, scales and validated operators.

For an illustrative cold-miss workload that reads 1.2 GB of expert data per output token from a store sustaining 3 GB/s, storage service alone needs at least 1.2/3=0.4 seconds per token. That is a best-case storage ceiling of 2.5 tokens/s for this serialized stream, before transfer or compute. If 75% of those bytes are served from a resident cache, disk demand is 0.3 GB/token and the corresponding service time is 0.1 seconds; it does not imply a fourfold end-to-end speedup. Overlapped stages share a critical path, while serialized stages add. These are independent calculations, not a measurement of a named system.

Measure cold and warm expert bytes, cache misses, read amplification, storage queueing, staging memory, host/device copies, synchronization and token latency. Compare a browser or native implementation with the same weights, quantizer and operators; one correct completion and a handful of matching layer values do not prove full-model equivalence. Do not confuse loading a weight file once with paging expert weights during every generated token.

## Reuse-aware residency and bounded prefetch

Expert-cache policy should estimate reuse within the relevant request or workload phase, not just count historical popularity forever. MoE-Infinity uses activation traces to guide replacement and prefetching in its evaluated personal-machine setting. A frequent expert can become cold after a topic change; retaining it may evict a newly useful expert. Compare reuse-aware admission with recency-based and demand-only baselines under equal capacity.

Prefetch moves a predicted expert before it is required. It helps only if useful reads overlap independent work and finish before consumption. Wrong predictions compete with demand traffic and consume staging space. In a toy schedule, one layer has 8 ms of independent work and the next expert transfer takes 5 ms: starting it early may hide that transfer. A 12 ms transfer still leaves at least 4 ms exposed under ideal overlap; shared-bandwidth contention can make the result worse. Measure useful prefetched bytes and critical-path stalls, not just queued I/O.

## Prefill and speculative verification working sets

A long prefill can touch many experts and evict the small hot set useful during decode. Phase-aware admission or protected capacity can preserve that set, at the cost of space unavailable to other work. This is an independently testable scheduling policy, not a claim that every engine provides it. Compare cold and warm decode after short and long prompts, including concurrent requests.

Speculative verification can also expand the requested expert union. If one verification examines three proposed positions routed to sets {A,B}, {B,C} and {C,D}, their union contains four experts, not two. Rejected proposals can still incur reads. Jointly measure accepted output tokens, union size, misses, staging memory and complete draft/verify latency when selecting speculation width. Larger speculative batches are not free simply because each token activates few experts.

## Prerequisites

- [[mixture-of-experts]]
- [[llm-inference-memory-budget]]
- [[gpu-data-flow]]

## Sources

- [MoE-Infinity](https://arxiv.org/abs/2401.14361): activation-aware expert caching and offloading under constrained GPU capacity.

- <https://arxiv.org/html/2401.14361v3>
