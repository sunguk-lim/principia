---
id: kimi-delta-attention
title: Kimi Delta Attention
summary: Kimi Delta Attention refines a gated delta-rule recurrent memory with finer-grained forgetting so selected state components can change without uniformly decaying the whole matrix.
type: concept
tags: [ml/llm/architecture]
prereqs: [gated-delta-network]
sources: [https://arxiv.org/abs/2510.26692, https://github.com/MoonshotAI/Kimi-Linear]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Kimi Delta Attention

## Summary

A [[gated-delta-network]] combines forgetting with a corrective write to a bounded key–value state. **Kimi Delta Attention (KDA)** changes the granularity of the gate: instead of treating all state components as if they need the same decay, it allows finer control over which parts persist. It is a recurrent sequence mixer, not a replacement for an entire transformer block or a per-token choice of whether to run an attention layer.

## Grounded explanation

Suppose the state contains several associations and a new token contradicts only one. A coarse decay weakens every association before the delta correction is added. Finer-grained gating can preserve unrelated components while modifying the part implicated by the new key. The core problem is allocation of finite memory, not creation of unlimited memory. Different histories may still collide in the same state, and a full-attention KV cache can still be useful for exact token-position lookup.

The Kimi Linear report pairs KDA layers with Multi-Head Latent Attention layers in a fixed depth pattern. Its authors also describe a chunkwise algorithm for efficient training on matrix hardware. The reported cache and throughput improvements are properties of particular models, kernels, hardware, and workloads; they are not guaranteed by finer gates alone.

## Validation

Ablate fine-grained versus coarse gates at matched parameters and training tokens. Test selective overwriting, exact long-range retrieval, context switches, prefill throughput, decode latency, and state/KV bytes across context lengths and batch sizes. Compare the complete hybrid against full attention as well as the mixer in isolation.

## Prerequisites

- [[gated-delta-network]]

## Sources

- [Kimi Team, *Kimi Linear: An Expressive, Efficient Attention Architecture*](https://arxiv.org/abs/2510.26692).
- [Moonshot AI implementation and model references](https://github.com/MoonshotAI/Kimi-Linear).
