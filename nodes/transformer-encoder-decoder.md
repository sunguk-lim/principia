---
id: transformer-encoder-decoder
title: Transformer Encoder–Decoder
summary: The original Transformer encoder–decoder encodes a source sequence with self-attention and generates a target sequence using masked self-attention plus attention to the encoder outputs.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, positional-encoding, layer-normalization]
sources: [https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Transformer Encoder–Decoder

## Summary

The original **Transformer encoder–decoder** maps one sequence to another without recurrent state. The encoder builds contextual source representations; the decoder generates target tokens while attending both to earlier target tokens and to the encoded source. The model is a composition of attention, position information, feed-forward transformations, residual paths, and normalization—not merely a single attention equation.

## Grounded explanation

An encoder layer applies multi-head [[transformer-attention]] across source positions, followed by a position-wise feed-forward network. The input includes [[positional-encoding]] because attention alone does not provide sequence order. Residual connections and [[layer-normalization]] support deep optimization. The original paper specifies stacks of these layers, rather than one universal layer count for all Transformers.

A decoder layer first uses *masked* self-attention: target position $t$ may read target positions up to $t$, not future tokens. A second attention block uses decoder queries and encoder keys/values, allowing the generated token to select source information. A feed-forward block follows. During training, target tokens can be processed in parallel under the causal mask; during autoregressive use, outputs are emitted one token at a time. Cross-attention is therefore a different relation from encoder self-attention or decoder self-attention.

For translation, the encoder reads the complete source sentence while the decoder predicts the next target word from the target prefix and relevant source positions. An encoder-only classifier can omit the decoder; a decoder-only language model can omit the source encoder and cross-attention. These are architectural variants, not evidence that one design wins on every task. The newer causal encoder–decoder design serves a different objective: its source-reading path is causal and deliberately asymmetric for inference cost.

Validate by checking attention masks, source/target positions, teacher-forcing inputs, and generation stopping behavior. Compare variants at matched data and compute budgets using task quality, latency, memory, and length generalization. Do not infer that recurrence is obsolete or that scaling is effortless from the historical paper.

## Sources

- [Vaswani et al., “Attention Is All You Need”](https://arxiv.org/abs/1706.03762): original encoder/decoder blocks, masking, cross-attention, and training architecture.
