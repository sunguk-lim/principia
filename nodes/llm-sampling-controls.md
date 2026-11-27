---
id: llm-sampling-controls
title: LLM Sampling Controls
summary: Temperature reshapes next-token probabilities while top-k and nucleus sampling truncate candidate support by rank or cumulative mass, without guaranteeing factual quality.
type: concept
tags: [ml/llm/inference]
prereqs: [softmax]
sources: [https://huggingface.co/docs/transformers/main_classes/text_generation]
status: explained
created: 2026-10-17
updated: 2026-11-28
---

# LLM Sampling Controls

## Summary

A decoder turns next-token scores into a distribution with [[softmax]], then chooses a token. **Temperature** and **top-p (nucleus) sampling** change that choice in different ways. Temperature changes the relative probabilities; top-p removes the low-probability tail before sampling. Neither makes a model more knowledgeable or guarantees a correct answer.

## Grounded explanation

For logits $z_i$, temperature $T>0$ produces $p_i(T)=\exp(z_i/T)/\sum_j\exp(z_j/T)$. Lower $T$ sharpens differences; higher $T$ flattens them. At the limiting low-temperature end, choice approaches an argmax, but exact behavior also depends on any other decoding filters. Temperature does not change the model's learned scores, only how they are converted into selection probabilities.

Top-p first orders tokens by probability, keeps the smallest prefix whose cumulative mass reaches at least $p$, renormalizes that set, and samples within it. Unlike a fixed top-k, its number of candidates varies with the distribution. Temperature and top-p may be composed, so their order and implementation defaults matter. A restrictive top-p can remove a rare but correct token; a high temperature can amplify poor continuations.

## Validation

Hold model, prompt set, token budget, and seed protocol fixed while sweeping temperature and top-p separately and together. Measure task success and calibrated uncertainty where applicable, not just lexical diversity. Include latency, invalid structured outputs, rare-label errors, and multi-run variability. For deterministic requirements, test the implementation's actual greedy path instead of assuming a near-zero temperature is identical.


## Fixed top-k versus cumulative top-p

Top-k keeps a fixed number of highest-scoring candidates before renormalization, subject to the implementation's handling of ties and other processors. Top-p instead adapts the number to the cumulative probability mass. For an invented ordered distribution `[0.50, 0.25, 0.15, 0.10]`, top-k with k=2 keeps the first two entries and renormalizes them to `[2/3, 1/3]`. Top-p with p=0.8 needs the first three entries because 0.50+0.25=0.75 is insufficient while adding 0.15 reaches 0.90; their conditional probabilities are `[5/9, 5/18, 1/6]`.

These controls limit candidate support, not semantic relevance. A low-probability token may be required for a rare correct name. Test repetition, factual or code correctness and useful diversity across representative prompts and seeds. Do not confuse top-k next-token sampling with top-k document retrieval: they select different objects at different stages. Processor order, zero-temperature conventions and backend nondeterminism must be checked in the deployed implementation.

## Prerequisites

- [[softmax]]

## Sources

- [Hugging Face Transformers generation configuration](https://huggingface.co/docs/transformers/main_classes/text_generation): temperature and top-p parameter semantics.
