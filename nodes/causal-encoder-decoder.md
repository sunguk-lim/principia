---
id: causal-encoder-decoder
title: Causal Encoder–Decoder for Autoregressive Serving
summary: A causal encoder–decoder can process supplied context through a shorter causal path while generated tokens use an additional decoder path and shared context memory.
type: concept
tags: [ml/llm/inference]
prereqs: [prefill-vs-decode, transformer-attention, kv-cache]
sources: [https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Causal Encoder–Decoder for Autoregressive Serving

## Summary

A **causal encoder–decoder** separates the path that reads supplied context from the path that generates new tokens. A causal encoder forms reusable representations of earlier tokens; a decoder reads that memory while producing each next token. Unlike a bidirectional encoder, the context path remains causal so a position cannot use later positions. The central trade-off is cheaper [[prefill-vs-decode|prefill]] versus memory quality and per-token decode work.

## Grounded explanation

A conventional decoder-only transformer runs every prompt and generated token through every layer. Its [[kv-cache]] retains layer-specific keys and values so a new query can attend to earlier positions. An asymmetric design can stop most prompt positions after a causal encoder and project the final encoder states into a shared global cache for the decoder. The generated position still needs the decoder path to predict the next token. This changes *where* computation and cache storage occur, not the autoregressive output contract.

DeepSeek's V4.1 Flash model card reports a 20-layer causal encoder followed by a 20-layer decoder within a 40-layer model. It describes shared global KV projected from encoder states, plus a recent-context path and additional sparse/cache mechanisms. These are author-reported implementation details; the card's parameter, speed, quality, and byte figures are not independently validated here. The reusable concept is the separation of input reading and output generation, not a claim that one layer split is optimal.

The design may help input-heavy workloads, but shortening the prompt path can discard representations that later generation needs. Shared memory may reduce duplicate cache state but creates a bottleneck if many decoder layers require different information. A full decoder-only model, a smaller model, retrieval, or ordinary prompt caching are alternative ways to reduce cost. Do not attribute a measured gain to the encoder split alone when sparse indexing, quantization, replay, or batching also changed.

At fixed hardware, quality target, concurrency, and prompt/output distributions, compare prefill time, time to first token, inter-token latency, generated-token throughput, peak and persistent cache bytes, and long-context retrieval quality. Ablate the encoder split independently of other cache changes. Causality and numerical equivalence are separate questions: an asymmetric model is trained for this architecture and is not a drop-in bit-identical rewrite of an existing decoder-only checkpoint.

## Sources

- [DeepSeek V4.1 Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash): primary architecture description; reported efficiency and quality remain vendor claims.
