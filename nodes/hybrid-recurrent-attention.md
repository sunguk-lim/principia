---
id: hybrid-recurrent-attention
title: Hybrid Recurrent–Attention Decoder
summary: A hybrid decoder interleaves fixed-size recurrent memory layers with full-attention layers that retain token-addressable KV caches, trading lower cache growth for retained token-addressable read paths.
type: concept
tags: [ml/llm/architecture]
prereqs: [gated-delta-network, kv-cache]
sources: [https://huggingface.co/Qwen/Qwen3.5-27B/raw/main/config.json, https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct, https://arxiv.org/abs/2412.06464]
status: explained
created: 2026-10-12
updated: 2026-11-12
---

# Hybrid Recurrent–Attention Decoder

## Summary

A hybrid decoder combines layers that compress past tokens into a bounded state with layers that keep an addressable [[kv-cache]]. The combination can reduce long-context cache growth relative to an all-full-attention stack while preserving some token-level lookup paths. It does **not** make the entire model's context memory constant.

## Grounded explanation

A recurrent layer such as [[gated-delta-network]] updates a fixed-size state when a new token arrives. Its decode-state size stays roughly constant with sequence length, but the state must share capacity across many past events. A full-attention layer retains a key and value for each earlier token in its [[kv-cache]], so it can score individual positions at the price of memory and read work that grow with context.

Interleaving the two gives both mechanisms in one network. For example, the published configuration of **Qwen3.5-27B** lists three `linear_attention` layers followed by one `full_attention` layer, repeated through the stack (`full_attention_interval: 4`). This configuration establishes the architecture, not a quality or throughput advantage. The saved source called the model “Qwen3.8-27B”; that name is not supported by this primary configuration and is omitted here.

The official Qwen3-Next model card independently reports a layout of three Gated DeltaNet mixers followed by one gated-attention mixer, with an MoE feedforward block after each mixer. That **3:1 layout is fixed across depth**: every token traverses the same configured mixer positions. The MoE router instead chooses experts from the current token representation. Mixer placement and expert selection are different decisions, even though both affect execution cost. Total parameters count dormant experts; activated parameters omit some routing, memory traffic, state/KV storage, and hardware overhead. Neither number alone predicts latency or memory use. Compare model variants using measured time-to-first-token, time-per-output-token, throughput, state and KV bytes, and quality at matched hardware and context. The model-card performance claims remain vendor reports, not general guarantees.

For $L_f$ full-attention layers, KV storage still grows with sequence length $T$ approximately as $O(L_f T d_{kv})$, in addition to recurrent states. Reducing $L_f$ changes the coefficient, not the sequence-length order. Prefill, batching, and hardware kernels can shift the latency trade-off.

## Count growing caches and bounded states separately

For one sequence, let T be retained tokens, L_a the number of attention layers, H the stored KV-head count, D_k and D_v the key and value head widths, and b the bytes per value. An uncompressed attention payload is T×L_a×H×(D_k+D_v)×b. Multiply by concurrent sequences when state is not shared. Add recurrent matrices and any convolution state, scales, alignment and temporary buffers separately. Fixed state means fixed with respect to T, not zero bytes or fixed total serving memory.

For an invented 12-layer stack with three attention layers, T=4,096, H=2, D_k=D_v=64 and b=2, attention state is 4,096×3×2×128×2=6,291,456 bytes, or 6 MiB. An otherwise equal 12-attention-layer stack needs 24 MiB. If the nine recurrent layers each retain four 64-by-64 matrices at four bytes per element, they add 9×4×64×64×4=589,824 bytes, or .5625 MiB. These counted state terms give 6.5625 MiB versus 24 MiB, not a claim of fourfold reduction in total model memory or measured runtime. The recurrent dimensions and precision must come from the actual implementation.

Attention keeps position-addressable keys and values; it does not guarantee that a model will retrieve every fact correctly. A hybrid's recall, few-shot behavior and throughput must therefore be tested rather than inferred from the layer ratio. Changing the number of attention layers changes both the state budget and the learned computation, so a memory-only comparison does not establish equal task quality.

## Validation

Compare all-full, all-recurrent, and mixed stacks under matched training data, parameter count, tokenization, and serving hardware. Sweep context length and batch size; record KV/state bytes, prefill and decode latency, and accuracy on both exact early-token retrieval and changing-instruction tasks. Ablate the full-attention interval rather than attributing results to a model name alone.

## Prerequisites

- [[gated-delta-network]]
- [[kv-cache]]

## Sources

- [Official Qwen3.5-27B configuration](https://huggingface.co/Qwen/Qwen3.5-27B/raw/main/config.json)
- [Gated Delta Networks paper](https://arxiv.org/abs/2412.06464)
- [Official Qwen3-Next model card](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
