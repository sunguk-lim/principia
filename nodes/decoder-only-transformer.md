---
id: decoder-only-transformer
title: Decoder-Only Transformer
summary: A decoder-only Transformer uses causally masked self-attention over one token stream to predict continuations without a separate encoder or encoder–decoder cross-attention.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-encoder-decoder, causal-language-model-training, kv-cache]
sources: [https://arxiv.org/abs/2005.14165, https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Decoder-Only Transformer

## Summary

A decoder-only Transformer reuses the masked self-attention style of the original decoder but removes the separate source encoder and its cross-attention block. Prompts and generated tokens occupy one causal stream.

## Grounded explanation

[[causal-language-model-training]] teaches each position to predict the following token from its prefix. A decoder-only stack composes masked attention and feed-forward transformations so position $t$ sees no later positions. During generation, a [[kv-cache]] retains prior keys and values; one new token extends the stream, then the model predicts the next. This differs from [[transformer-encoder-decoder]], where a decoder can attend to a separately encoded source sequence.

If a question and supporting document appear in the prompt, the model can attend to both as earlier tokens; no independent encoder has summarized them. That flexibility also means long prompts cost prefill work and cache memory. A decoder-only model can be adapted for classification or extraction, but its architecture does not make those outcomes calibrated or faithful.

Validate causal masks and cache positions on toy sequences. Compare prefill, per-token decode, quality, and memory at matched context and model size. A one-stream architecture is not synonymous with any particular tokenizer, parameter count, training data, or instruction-following capability. GPT-style models are primary examples, not proof of general superiority.

## Sources

- [Brown et al., GPT-3](https://arxiv.org/abs/2005.14165): autoregressive language-model example.
- [Vaswani et al., Transformer](https://arxiv.org/abs/1706.03762): masked decoder mechanism from which the variant is derived.
