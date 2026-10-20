---
id: relative-position-embeddings
title: Learned Relative Position Embeddings
summary: Learned relative position embeddings add clipped query-key offset representations to attention scores and optionally values instead of relying only on absolute input positions.
type: concept
tags: [ml/llm/architecture]
prereqs: [positional-encoding]
sources: [https://arxiv.org/abs/1803.02155]
status: explained
created: 2026-10-21
updated: 2026-10-21
---

# Learned Relative Position Embeddings

## Meaning

Learned relative position embeddings expose the offset between a query and a key directly inside attention. This is one specific implementation of [[positional-encoding]], distinct from adding absolute position vectors at the input or rotating queries and keys.

## Mechanism

Let i be a query position, j a key position, and L a nonnegative maximum represented distance. Define r=clip(j-i,-L,L): offsets below -L become -L, offsets above L become L. Learn a key-side vector aK_r and optionally a value-side vector aV_r for each of the 2L+1 offsets.

For query vector q_i, key k_j and value v_j of head dimension d, the score is q_i·(k_j+aK_r)/sqrt(d). Normalize the scores across permitted keys with attention's usual softmax to obtain weights alpha_ij. The output is the sum over j of alpha_ij(v_j+aV_r). Position therefore changes which content is selected and, in the value-side variant, what relation information is returned.

The learned vectors match the attention-head representation used in these additions; they are not automatically model-width vectors. Shaw and colleagues describe sharing relation representations across heads. Clipping saves parameter categories but deliberately loses exact distance distinctions beyond L; it does not make attention local or remove all distant keys.

## Worked example

Use a scalar toy head, so d=1, query position i=3 and causal key positions j=1,2,3. With L=1, raw offsets -2,-1,0 become -1,-1,0. Set q=1, content keys (1,2,1), and key-side embeddings aK_-1=0.5, aK_0=-0.5. Scores are (1.5,2.5,0.5); normalized weights are approximately (0.245,0.665,0.090).

With values (2,4,1), value-side embeddings aV_-1=0.2 and aV_0=-0.1, the output is approximately 0.245×2.2+0.665×4.2+0.090×0.9=3.413. The first two keys share a clipped distance label but retain different content scores. The distant key was not removed.

## Check your understanding

**Question:** Does distance clipping impose a sliding window? **Answer:** No. It merges offset representations; an independent mask determines which keys remain accessible.

## Prerequisites

- [[positional-encoding]]

## Sources

- <https://arxiv.org/abs/1803.02155>
