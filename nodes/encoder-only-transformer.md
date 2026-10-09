---
id: encoder-only-transformer
title: Encoder-Only Transformer
summary: An encoder-only Transformer builds bidirectional token representations with self-attention over the available input, making it suitable for understanding tasks rather than native left-to-right generation.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-encoder-decoder, transformer-attention, positional-encoding]
sources: [https://arxiv.org/abs/1810.04805, https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Encoder-Only Transformer

## Summary

An encoder-only Transformer keeps the source-side stack of the original encoder–decoder architecture. Each token can condition on positions on both sides of it within the supplied input, subject to padding and task masks.

## Grounded explanation

In [[transformer-encoder-decoder]], the encoder's [[transformer-attention]] forms contextual representations without the decoder's causal future mask or encoder–decoder cross-attention. [[positional-encoding]] supplies order. BERT demonstrates pretraining such representations with a masked-token objective, then attaching task heads for classification or span selection. The architecture and the objective are separate choices: “encoder-only” does not itself imply BERT's exact training recipe.

For “the bank flooded,” the representation at “bank” can use “flooded” to disambiguate meaning. That is useful when the whole input is available. It is not a standard autoregressive generator: if future target tokens were visible during next-token training, the model could leak the answer. A generation task needs a causal mask or a different architecture/objective.

Check the implemented attention mask on a short input, then evaluate on held-out understanding tasks with the same tokenizer, input length, and compute budget as alternatives. Compare accuracy, calibration, throughput, and memory. Bidirectional visibility is a capability, not evidence that every encoder-only model beats a decoder-only model on every task.

## Sources

- [Devlin et al., BERT](https://arxiv.org/abs/1810.04805): bidirectional encoder representations and masked-token pretraining.
- [Vaswani et al., Transformer](https://arxiv.org/abs/1706.03762): source-side encoder architecture.
