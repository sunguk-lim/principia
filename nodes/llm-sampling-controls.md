---
id: llm-sampling-controls
title: LLM Sampling Controls
summary: Temperature reshapes next-token probabilities while nucleus sampling truncates the candidate set by cumulative mass; both alter diversity without proving factual quality.
type: concept
tags: [ml/llm/inference]
prereqs: [softmax]
sources: [https://huggingface.co/docs/transformers/main_classes/text_generation]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# LLM Sampling Controls

## Summary

A decoder turns next-token scores into a distribution with [[softmax]], then chooses a token. **Temperature** and **top-p (nucleus) sampling** change that choice in different ways. Temperature changes the relative probabilities; top-p removes the low-probability tail before sampling. Neither makes a model more knowledgeable or guarantees a correct answer.

## Grounded explanation

For logits $z_i$, temperature $T>0$ produces $p_i(T)=\exp(z_i/T)/\sum_j\exp(z_j/T)$. Lower $T$ sharpens differences; higher $T$ flattens them. At the limiting low-temperature end, choice approaches an argmax, but exact behavior also depends on any other decoding filters. Temperature does not change the model's learned scores, only how they are converted into selection probabilities.

Top-p first orders tokens by probability, keeps the smallest prefix whose cumulative mass reaches at least $p$, renormalizes that set, and samples within it. Unlike a fixed top-k, its number of candidates varies with the distribution. Temperature and top-p may be composed, so their order and implementation defaults matter. A restrictive top-p can remove a rare but correct token; a high temperature can amplify poor continuations.

## Validation

Hold model, prompt set, token budget, and seed protocol fixed while sweeping temperature and top-p separately and together. Measure task success and calibrated uncertainty where applicable, not just lexical diversity. Include latency, invalid structured outputs, rare-label errors, and multi-run variability. For deterministic requirements, test the implementation's actual greedy path instead of assuming a near-zero temperature is identical.

## Prerequisites

- [[softmax]]

## Sources

- [Hugging Face Transformers generation configuration](https://huggingface.co/docs/transformers/main_classes/text_generation): temperature and top-p parameter semantics.
