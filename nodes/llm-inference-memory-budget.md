---
id: llm-inference-memory-budget
title: LLM Inference Memory Budget
summary: An LLM inference memory budget separates fixed model weights from request-dependent KV cache, temporary workspace, runtime reservations, and safety headroom so capacity is planned for the workload rather than the checkpoint alone.
type: concept
tags: [ml/llm/inference]
prereqs: [post-training-quantization, kv-cache, prefill-vs-decode, paged-attention]
sources: [https://arxiv.org/abs/2309.06180, https://docs.pytorch.org/docs/2.14/notes/cuda.html#cuda-memory-management]
status: explained
created: 2026-09-18
updated: 2026-09-18
---

# LLM Inference Memory Budget

## Summary

An **LLM inference memory budget** accounts for every allocation that must coexist at the workload's peak:

$$
M_{\text{required}} = M_{\text{weights}} + M_{\text{KV}} + M_{\text{temporary}} + M_{\text{runtime}} + M_{\text{headroom}}.
$$

A checkpoint fitting in GPU memory proves only that the mostly fixed weight term fits. It does not prove that the intended context lengths, concurrent requests, kernels, and allocator behavior fit at the same time.

## Grounded explanation

### The five terms have different scaling rules

**Model weights** are the learned parameters loaded for inference. For $P$ parameters stored at $b$ bits each, the first-order footprint is $P b / 8$ bytes, plus quantization scales, metadata, and any duplicated or sharded state. [[post-training-quantization]] reduces this term, but a smaller checkpoint does not constrain the other four terms.

The **[[kv-cache]]** stores keys and values for prior tokens. For a dense decoder cache, an approximate footprint is

$$
M_{\text{KV}} = 2 L T H_{kv} D_h C B,
$$

where $L$ is the number of layers, $T$ is cached tokens per active sequence, $H_{kv}$ is key/value heads, $D_h$ is head width, $C$ is active sequences, $B$ is bytes per stored value, and the factor 2 counts keys and values. This term grows linearly with context and concurrency. [[paged-attention]] reduces allocation waste and enables block reuse; it does not make live KV data free.

**Temporary memory** holds intermediate activations, output buffers, attention or matrix-multiplication workspace, sampling buffers, and communication scratch space. These allocations are commonly reused rather than retained for every layer, so capacity planning needs their *peak*, not their sum across the model. Their peak also changes across [[prefill-vs-decode]]: prefill processes many prompt tokens together, while decode processes new tokens for the active batch.

**Runtime memory** includes device contexts, loaded kernels, graph captures, scheduler state, communication libraries, and allocator bookkeeping. A caching allocator may retain freed blocks for reuse, so memory *reserved by the runtime* can exceed memory occupied by live tensors. Fragmentation can also prevent a large allocation even when smaller free regions add up to enough bytes.

**Headroom** is deliberately unassigned capacity. It absorbs shape variation, allocator fragmentation, library changes, and short-lived peaks. Treating the physical device limit as the operating target turns ordinary traffic variation into out-of-memory failures.

### Worked capacity check

Consider one 40-GiB GPU serving an 8-billion-parameter model in 16-bit weights.

- Weights: $8\times10^9\times2$ bytes is about **14.9 GiB** before metadata; budget **16 GiB**.
- KV cache: let $L=32$, $T=4096$, $H_{kv}=8$, $D_h=128$, $C=16$, and $B=2$. Then

$$
2\times32\times4096\times8\times128\times16\times2
= 8{,}589{,}934{,}592\text{ bytes}=8\text{ GiB}.
$$

- Peak temporary workspace: measured at **3 GiB** for the chosen kernels and batch.
- Runtime reservations: measured at **1.5 GiB** after warm-up.
- Headroom: reserve **3 GiB**.

The planned peak is $16+8+3+1.5+3=31.5$ GiB, leaving 8.5 GiB. But doubling the cached context to 8192 tokens doubles the KV term to 16 GiB, raising the total to **39.5 GiB**. The checkpoint still fits; the workload is now too close to the limit to be robust. A capacity decision could reduce concurrency, context, KV precision, or weight precision, or distribute the model—each changes a different term and has different quality and latency costs.

### Measure the budget under the real scheduler

Estimate first, then measure after warm-up with representative prompt lengths, output lengths, concurrency, and kernel choices. Record live tensor memory, allocator-reserved memory, peak temporary memory, KV-pool occupancy, failed-allocation size, and fragmentation indicators. Sweep context and concurrency independently so their linear KV effects are visible. Pair memory measurements with time to first token, inter-token latency, throughput, and output-quality checks: a configuration that fits by shrinking precision or batch size can still fail its service objective.

The invariant is simple: every term that can peak together must fit together. Capacity planning is therefore a workload experiment, not a comparison between checkpoint bytes and advertised VRAM.

## Prerequisites

- [[post-training-quantization]]
- [[kv-cache]]
- [[prefill-vs-decode]]
- [[paged-attention]]

## Sources

- [Kwon et al., “Efficient Memory Management for Large Language Model Serving with PagedAttention,” SOSP 2023](https://arxiv.org/abs/2309.06180): dynamic KV-cache growth, fragmentation, duplication, and block-based management.
- [PyTorch, “CUDA semantics — CUDA memory management”](https://docs.pytorch.org/docs/2.14/notes/cuda.html#cuda-memory-management): allocated versus allocator-reserved memory and CUDA memory diagnostics.
