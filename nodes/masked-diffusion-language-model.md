---
id: masked-diffusion-language-model
title: Masked Diffusion Language Model
summary: A masked diffusion language model generates a fixed set of token positions by repeatedly predicting masked tokens and revealing selected positions, rather than extending a prefix one token at a time.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, subword-tokenization, probability-distribution]
sources: [https://arxiv.org/abs/2502.09992]
status: explained
created: 2026-10-15
updated: 2026-10-15
---

# Masked Diffusion Language Model

## Summary

A **masked diffusion language model** starts generation with unknown token positions and iteratively fills them. The “diffusion” analogy refers to a forward corruption process and a learned reverse process; unlike image diffusion, the corruption here can be discrete masking rather than added Gaussian noise.

## Grounded explanation

During training, select a subset of [[subword-tokenization]] positions and replace them with a mask symbol. A network built with [[transformer-attention]] predicts the original tokens at masked positions, conditioned on visible tokens and a corruption level. The objective estimates a [[probability-distribution]] over missing tokens under different mask patterns. LLaDA is one published instance that trains a Transformer with a forward masking and reverse generation process; its reported benchmark comparisons are specific to that study, not a general property of every diffusion language model.

For generation, choose an output length or length policy, initialize the unknown positions as masks, and run several refinement steps. At each step the model proposes tokens for unresolved positions and a schedule decides which predictions to accept or remask. Multiple positions can be predicted in one model pass, so the dependency pattern differs from left-to-right autoregression. This does not imply an automatic speedup: repeated full-sequence passes, length selection, confidence errors, and remasking can dominate cost. Nor does “parallel” mean all token choices are independent—the model conditions each pass on the currently visible sequence.

A useful small example begins with `The [MASK] is [MASK]`. One pass may propose `cat` and `sleeping`; a later pass can revise an uncertain position after the other is committed. The schedule must define what is frozen and what can change. Compare against an autoregressive model with matched quality and hardware, measuring wall-clock latency, model passes, tokens per pass, memory, length errors, and consistency under repeated decoding. Evaluate order-sensitive tasks separately, since bidirectional revision can help some constraints but can also produce incompatible local choices.

## Prerequisites

- [[transformer-attention]]
- [[subword-tokenization]]
- [[probability-distribution]]

## Sources

- [Nie et al., “Large Language Diffusion Models”](https://arxiv.org/abs/2502.09992): masked forward corruption, reverse token prediction, and the LLaDA implementation.
