---
id: multi-head-attention
title: Multi-Head Attention
summary: One transformer-attention produces a single weighting of the tokens — so it can emphasize only one kind of relationship at a time.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, matrix-multiplication, softmax]
sources: ["Vaswani et al., Attention Is All You Need (2017), arXiv:1706.03762"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Multi-Head Attention

## Summary

One [[transformer-attention]] produces a **single** weighting of the tokens — so it can emphasize only
one kind of relationship at a time. **Multi-head attention** runs $h$ attentions *in parallel*, each on
its own learned slice of the representation, then glues the results back together. Because every head
works in a space $h$ times narrower, the $h$ heads together cost about the same as one full-size
attention — so the model attends to several relationships at once, essentially **for free**.

## Grounded explanation

**1 · Symbols** — 🟦 scalar · 🟩 vector · 🟧 matrix

| Symbol | Type | Shape | Meaning |
|--------|------|-------|---------|
| $X$ | 🟧 matrix | $n\times d$ | input — one $d$-dimensional row per token |
| $h$ | 🟦 scalar | — | number of heads |
| $d_\text{head}$ | 🟦 scalar | — | per-head width, $= d/h$ |
| $W_q^i, W_k^i, W_v^i$ | 🟧 matrix | $d\times d_\text{head}$ | head $i$'s learned projections |
| $\text{head}_i$ | 🟧 matrix | $n\times d_\text{head}$ | the output of one [[transformer-attention]] |
| $W_o$ | 🟧 matrix | $d\times d$ | output projection that mixes the heads |
| $\text{MHA}(X)$ | 🟧 matrix | $n\times d$ | final output |

**2 · Equation**

$$\text{MHA}(X) = \mathrm{Concat}(\text{head}_1,\dots,\text{head}_h)\,W_o,
\qquad \text{head}_i = \mathrm{Attention}\!\left(X W_q^i,\; X W_k^i,\; X W_v^i\right)$$

where $\mathrm{Attention}$ is exactly [[transformer-attention]], run inside head $i$'s own subspace.

**What it is.** Each head $i$ first **projects** the input into its own $d_\text{head}$-dimensional
subspace via [[matrix-multiplication]]: $X W_q^i$, $X W_k^i$, $X W_v^i$. It then runs an ordinary [[transformer-attention]] there to get
$\text{head}_i$ (shape $n\times d_\text{head}$), and then the $h$ head outputs are **concatenated** back
to width $d$ and recombined by a single $W_o$. The defining object is not the attention inside a head
(that is the prerequisite) — it is the *parallel bank of heads on different projections* plus the
concat-and-mix.

**Why split instead of using one big head.** A single attention emits **one** [[transformer-attention]]
weighting per query, so its output is one weighted average — it can express only one relationship
pattern at a time (e.g. "look at the previous token"). Give the model $h$ heads on different projections
and it produces $h$ **independent** weightings of the same tokens; the concatenation lets the result
carry all of them at once (one head can track the subject, another the adjacent word, another a
long-range referent). The identity that makes this affordable: with $d_\text{head} = d/h$, the $h$
projection matrices $W^i$ stack into the *same* $d\times d$ matrix a single full-width attention would
use — so $h$ narrow heads cost the **same** parameters and [[matrix-multiplication]]s as one wide head.
Multi-relational mixing comes essentially for free.

**Worked instance.** Take $d = 4$, $h = 2$ (so $d_\text{head} = 2$), two tokens, with token 1 as the
query. To keep the arithmetic visible, let each head's projection simply *select* two coordinates: head
1 reads dimensions 1–2, head 2 reads dimensions 3–4.

- **Head 1** (dims 1–2): query $q = [1,0]$; keys $k_1 = [1,0],\, k_2 = [0,1]$; values $v_1 = [2,0],\,
  v_2 = [0,2]$. Scores $q\!\cdot\!k_1 = 1,\ q\!\cdot\!k_2 = 0$; scale by $\sqrt{d_\text{head}} = \sqrt2$
  to get $[0.71,\,0]$; [[softmax]] $\to [0.67,\,0.33]$. So
  $\text{head}_1 = 0.67\,[2,0] + 0.33\,[0,2] = [1.34,\,0.66]$.
- **Head 2** (dims 3–4): query $q = [0,1]$; same keys; values $v_1 = [3,0],\, v_2 = [0,3]$. Scores
  $[0,\,1]$, scaled to $[0,\,0.71]$; [[softmax]] $\to [0.33,\,0.67]$. So
  $\text{head}_2 = 0.33\,[3,0] + 0.67\,[0,3] = [0.99,\,2.01]$.
- **Concat** $\to [1.34,\,0.66,\;0.99,\,2.01]$, back to width $d = 4$; with $W_o = I$ this is
  $\text{MHA}(X)$.

The payoff is right there in the numbers: from the **same** two tokens, head 1 leaned on token 1
(weight $0.67$) while head 2 leaned on token 2 (weight $0.67$) — two *different* relationships captured
at the same time, precisely because the heads look at different subspaces. A single head could have
reported only one of them.

**Where it runs.** The $h$ heads are independent, so hardware computes them as one batched set of matrix
multiplications — no slower than the single wide attention they replace. One consequence matters later:
each head keeps its **own** keys and values, and during generation those accumulate per head — which is
exactly the per-head memory cost that grouped-query attention is built to cut.

## Prerequisites

- [[transformer-attention]]
- [[matrix-multiplication]]
- [[softmax]]

## Sources

- Vaswani, Shazeer, Parmar, et al. — *Attention Is All You Need* (2017), arXiv:1706.03762
