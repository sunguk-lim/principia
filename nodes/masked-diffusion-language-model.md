---
id: masked-diffusion-language-model
title: Masked Diffusion Language Model
summary: A masked diffusion language model learns reconstruction from incomplete token sequences and generates by repeatedly proposing masked tokens and committing a scheduled subset.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, subword-tokenization, probability-distribution]
sources: [https://arxiv.org/abs/2502.09992, https://raw.githubusercontent.com/ML-GSAI/LLaDA/main/generate.py]
status: explained
created: 2026-10-15
updated: 2026-11-28
---

# Masked Diffusion Language Model

## Summary

A **masked diffusion language model** starts generation with unknown token positions and iteratively fills them. The “diffusion” analogy refers to a forward corruption process and a learned reverse process; unlike image diffusion, the corruption here can be discrete masking rather than added Gaussian noise.

## Grounded explanation

During training, select a subset of [[subword-tokenization]] positions and replace them with a mask symbol. A network built with [[transformer-attention]] predicts the original tokens at masked positions, conditioned on visible tokens and a corruption level. The objective estimates a [[probability-distribution]] over missing tokens under different mask patterns. LLaDA is one published instance that trains a Transformer with a forward masking and reverse generation process; its reported benchmark comparisons are specific to that study, not a general property of every diffusion language model.

For generation, choose an output length or length policy, initialize the unknown positions as masks, and run several refinement steps. At each step the model proposes tokens for unresolved positions and a schedule decides which predictions to accept or remask. Multiple positions can be predicted in one model pass, so the dependency pattern differs from left-to-right autoregression. This does not imply an automatic speedup: repeated full-sequence passes, length selection, confidence errors, and remasking can dominate cost. Nor does “parallel” mean all token choices are independent—the model conditions each pass on the currently visible sequence.

A useful small example begins with `The [MASK] is [MASK]`. One pass may propose `cat` and `sleeping`; a later pass can revise an uncertain position after the other is committed. The schedule must define what is frozen and what can change. Compare against an autoregressive model with matched quality and hardware, measuring wall-clock latency, model passes, tokens per pass, memory, length errors, and consistency under repeated decoding. Evaluate order-sensitive tasks separately, since bidirectional revision can help some constraints but can also produce incompatible local choices.


## Prediction is not commitment

A forward pass can propose a token at every remaining mask while the sampler writes only a subset into the persistent sequence. Unwritten proposals are discarded; the next pass recomputes them from the newly visible context. Predictions made in the same pass do not condition on one another's newly sampled values. Shared context creates statistical dependence, but does not supply an internal sequential conversation between those proposals.

Consider an invented four-position output `[MASK, MASK, MASK, MASK]`. One pass proposes `[red, birds, can, fly]`, but the policy commits positions 2 and 4, leaving `[MASK, birds, MASK, fly]`. The next pass predicts positions 1 and 3 with `birds` and `fly` now visible. It may produce `[small, birds, often, fly]`; the discarded proposals `red` and `can` were never committed history. This is a state trace, not a measured output from a real model.

Reveal count and reveal position are separate choices. A sampler can distribute a fixed mask count across steps, then select positions by sampled-token confidence or random scores. The public LLaDA sampler illustrates those policies and writes selected predictions into the sequence. Inspect the exact revision: a parameter named “remasking” does not prove that every committed token is later revised. More simultaneous commitments reduce opportunities to condition on other new values and can freeze inconsistent choices.

Compare schedules under fixed output length, model and quality criteria. Count useful committed tokens, repeated sequence work, model evaluations and wall time; predicting four candidates and committing two is not four completed output tokens. Fixed initial slots, blockwise extension and stop handling are distinct length policies, not interchangeable consequences of the word diffusion.

## Prerequisites

- [[transformer-attention]]
- [[subword-tokenization]]
- [[probability-distribution]]

## Sources

- [Nie et al., “Large Language Diffusion Models”](https://arxiv.org/abs/2502.09992): masked forward corruption, reverse token prediction, and the LLaDA implementation.

- <https://raw.githubusercontent.com/ML-GSAI/LLaDA/main/generate.py>
