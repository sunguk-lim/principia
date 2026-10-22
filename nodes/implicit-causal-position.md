---
id: implicit-causal-position
title: Implicit Causal Positional Information
summary: A causal attention mask can provide asymmetric position cues even without explicit positional embeddings, but does not guarantee reliable length generalization.
type: concept
tags: [ml/llm/architecture]
prereqs: [causal-language-model-training, positional-encoding]
sources: [https://arxiv.org/abs/2203.16634]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# Implicit Causal Positional Information

## Meaning

No positional embedding does not mean no possible positional information. In a causal model, different positions are permitted to see different prefixes. That structural asymmetry can supply cues a trained model uses to infer order. The NoPE paper reports such learned behavior and proposes an explanation; it does not establish that every masked network can exactly count positions or generalize indefinitely.

## Mechanism

[[causal-language-model-training]] supplies a lower-triangular attention mask. [[positional-encoding]] supplies the explicit position vectors or rotations omitted in a NoPE experiment. At position t, the visible keys are positions 0 through t rather than the same unrestricted set at every query. Boundary tokens and nonidentical content can produce different aggregated representations as prefix membership changes. Later layers may exploit those differences as positional signals.

Mask asymmetry alone is not an exact counter. Attention normalizes its weights: averaging two identical values gives the same result as averaging ten identical values. Without another distinguishable cue, prefix cardinality need not appear in the output. The primary paper explicitly frames predecessor counting as a conjectured mechanism and supports implicit position information with probing experiments. Keep observed representation behavior separate from a universal theorem.

## Worked example

Use a scalar attention output with all allowed scores equal, so weights are uniform. Let the start token's value be 2 and every following token's value be 1. A query seeing [2,1] returns 3/2=1.5; one seeing [2,1,1,1] returns 5/4=1.25. The distinct boundary makes prefix length affect the output. If every visible value is 1 instead, both averages are 1 and this example supplies no length cue. These are illustrative attention calculations, not measurements of a learned position counter.

Compare trained models with and without explicit encodings at matched architecture and budget. Probe recoverable absolute and relative position, vary boundary tokens and repeated content, and evaluate lengths beyond training on task correctness rather than probe accuracy alone. Removing embeddings does not remove cache coordinates, masks, data-order conventions or implementation limits. Better results in one extrapolation experiment do not prove that explicit positional mechanisms are generally unnecessary.

## Check your understanding

**Question:** Must normalized attention reveal how many identical keys it sees? **Answer:** No; normalization can make every prefix return the same value.

## Prerequisites

- [[causal-language-model-training]]
- [[positional-encoding]]

## Sources

- <https://arxiv.org/abs/2203.16634>
