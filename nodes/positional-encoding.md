---
id: positional-encoding
title: Positional Encoding
summary: Positional encoding injects token order into otherwise position-agnostic token representations by assigning each sequence position a distinguishable vector or attention offset.
type: concept
tags: [ml/llm/architecture]
prereqs: [embedding, transformer-attention]
sources: [https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Positional Encoding

## Summary

**Positional encoding** gives a sequence model information about where each token occurs. It combines a token's content representation with a position-dependent signal, allowing identical tokens at different positions—and the same set of tokens in different orders—to produce different computations.

## Grounded explanation

An [[embedding]] maps a token identity to a vector, but the same token receives the same vector wherever it appears. Moreover, [[transformer-attention]] compares queries with keys and takes weighted sums of values; without a position-dependent signal, reordering all input token vectors merely reorders the outputs. The mechanism can compare content, but it cannot infer order from content alone.

Let $e_t\in\mathbb{R}^d$ be the content vector for the token at integer position $t$, and let $p_t\in\mathbb{R}^d$ be a positional vector of the same dimension. An absolute additive encoding forms

$$
x_t=e_t+p_t.
$$

The attention layer then derives its queries, keys, and values from $x_t$, so both content and position can affect every attention score and output. Learned encodings store one trainable $p_t$ per supported position. Fixed sinusoidal encodings instead use waves at several frequencies:

$$
p_{t,2i}=\sin\!\left(t/10000^{2i/d}\right),\qquad
p_{t,2i+1}=\cos\!\left(t/10000^{2i/d}\right),
$$

where $i$ selects a pair of vector coordinates. Nearby positions have smoothly related vectors, while the multiple frequencies keep distant positions distinguishable.

### Worked example

Use two-dimensional toy token vectors and positional vectors

$$
e_{\text{A}}=(1,0),\quad e_{\text{B}}=(0,1),\qquad
p_0=(0,0),\quad p_1=(0.5,-0.5).
$$

For the sequence “A B,” the layer receives

$$
x_0=e_{\text{A}}+p_0=(1,0),\qquad
x_1=e_{\text{B}}+p_1=(0.5,0.5).
$$

For “B A,” it instead receives

$$
x'_0=e_{\text{B}}+p_0=(0,1),\qquad
x'_1=e_{\text{A}}+p_1=(1.5,-0.5).
$$

The unordered token inventory is identical, but the four vectors are not a mere exchange of the original content vectors: position has changed what attention compares. The repeated token “A” is also distinguishable at positions $0$ and $1$ because $(1,0)\ne(1.5,-0.5)$.

Not every positional method adds a vector to the input. Relative methods modify an attention score according to the offset between query position $t$ and key position $s$; rotary methods transform queries and keys by position-dependent rotations so their dot product depends on $t-s$. These are different implementations of the same requirement: expose order or distance to a computation that otherwise sees token content but no position.

## Prerequisites

- [[embedding]]
- [[transformer-attention]]

## Sources

- Vaswani et al., “Attention Is All You Need,” §3.5 — the position-agnostic attention motivation and learned or sinusoidal positional encodings.
