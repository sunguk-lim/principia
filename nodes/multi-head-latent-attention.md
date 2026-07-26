---
id: multi-head-latent-attention
title: Multi-Head Latent Attention
summary: The kv-cache is the memory bottleneck of generation, and in multi-head-attention it stores the keys and values of every head for every past token.
type: concept
tags: [ml/llm/architecture]
prereqs: [multi-head-attention, kv-cache, low-rank-factorization]
sources: ["DeepSeek-V2 (2024), arXiv:2405.04434"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Multi-Head Latent Attention

## Summary

The [[kv-cache]] is the memory bottleneck of generation, and in [[multi-head-attention]] it stores the
keys and values of **every head** for every past token. **Multi-head latent attention (MLA)** shrinks
that cache with a [[low-rank-factorization]]: instead of caching all the heads' `K` and `V`, it caches a
**single small latent vector** per token and **reconstructs** each head's `K`/`V` from it on demand.
Crucially, each head reconstructs from its *own* up-projection, so the heads stay distinct — MLA gets a
cache as small as sharing one head, while keeping the quality of full multi-head attention.

## Grounded explanation

**1 · Symbols** — 🟦 scalar · 🟩 vector · 🟧 matrix

| Symbol | Type | Shape | Meaning |
|--------|------|-------|---------|
| $x_t$ | 🟩 vector | $d$ | input of token $t$ ($d$ = model width) |
| $h$ | 🟦 scalar | — | number of heads (from [[multi-head-attention]]) |
| $d_\text{head}$ | 🟦 scalar | — | per-head width |
| $c_t$ | 🟩 vector | $d_c$ | **latent** for token $t$; $d_c \ll h\,d_\text{head}$ |
| $W^{DKV}$ | 🟧 matrix | $d_c \times d$ | down-projection (compress) |
| $W^{UK,i}, W^{UV,i}$ | 🟧 matrix | $d_\text{head}\times d_c$ | head $i$'s up-projections (reconstruct) |
| $q_t^i, k_t^i, v_t^i$ | 🟩 vector | $d_\text{head}$ | head $i$'s query / key / value for token $t$ |

**2 · Equations**

$$c_t = W^{DKV} x_t \quad\text{(compress — this latent is all that is cached)}$$

$$k_t^i = W^{UK,i}\, c_t, \qquad v_t^i = W^{UV,i}\, c_t \quad\text{(reconstruct head } i \text{ when needed)}$$

**What it is.** MLA keeps the $h$ parallel heads of [[multi-head-attention]] unchanged, but changes what
the [[kv-cache]] holds. Ordinary multi-head decoding caches every head's key and value — $2\,h\,
d_\text{head}$ numbers per token. MLA instead **down-projects** the token into a low-rank latent $c_t$ of
size $d_c \ll h\,d_\text{head}$ (a [[low-rank-factorization]] of the key/value content), and **caches
only $c_t$**. Each head's `K` and `V` are recovered by its own **up-projection** $W^{UK,i}, W^{UV,i}$
applied to that shared latent.

**Why it works — and the step that looks too cheap.** Two questions: does the tiny cache lose
information, and doesn't reconstructing $K$/$V$ every step cost extra compute? 

- *Quality.* Because each head has a **distinct** up-projection, two heads recover **different** keys
  from the *same* latent — the head diversity that gives [[multi-head-attention]] its expressiveness is
  preserved. (Contrast grouped-query attention, which shrinks the cache by making heads *share* `K`/`V`,
  giving up some of that diversity.)
- *Compute — the absorption identity.* You never actually have to rebuild $k_j^i$. A score is a dot
  product, and a dot product against a projected vector can be re-associated:
  $$q_t^i \cdot k_j^i = q_t^i \cdot \big(W^{UK,i} c_j\big) = \big(W^{UK,i\top} q_t^i\big)\cdot c_j .$$
  So $W^{UK,i}$ **folds into the query** once, and the score is taken **directly against the cached
  latent** $c_j$ — no per-head key reconstruction at all. The same trick folds $W^{UV,i}$ into the
  output projection on the value side. The small cache costs essentially nothing at attention time.

(One honest wrinkle: a small position-dependent part of the key is kept separate and uncompressed,
because that absorption no longer holds once positions are mixed in; the latent compresses the bulk
content part.)

**Worked instance.** Take $d = 4$, $h = 2$, $d_\text{head} = 2$, and a latent of size $d_c = 2$. With
multi-head attention the cache would hold $2\,h\,d_\text{head} = 8$ numbers per token (both heads' `K`
and `V`); MLA will hold just $d_c = 2$.

- Token $x_t = [2,0,1,0]$. Down-project with $W^{DKV} = \begin{bmatrix}1&0&0&0\\0&0&1&0\end{bmatrix}$
  (it reads dims 1 and 3): $c_t = [2,\,1]$. **Cache only these two numbers.**
- Reconstruct the keys with each head's up-projection:
  head 1 uses $W^{UK,1} = \begin{bmatrix}1&0\\0&1\end{bmatrix} \Rightarrow k_t^1 = [2,1]$;
  head 2 uses $W^{UK,2} = \begin{bmatrix}0&1\\1&0\end{bmatrix} \Rightarrow k_t^2 = [1,2]$.
  Same latent, **two different keys** — head diversity survives the compression.
- Check the absorption identity with queries $q^1 = q^2 = [1,0]$:
  - head 1, direct: $q^1\!\cdot k^1 = [1,0]\!\cdot[2,1] = 2$; absorbed:
    $(W^{UK,1\top}q^1)\!\cdot c_t = [1,0]\!\cdot[2,1] = 2$. ✓
  - head 2, direct: $q^2\!\cdot k^2 = [1,0]\!\cdot[1,2] = 1$; absorbed:
    $(W^{UK,2\top}q^2)\!\cdot c_t = [0,1]\!\cdot[2,1] = 1$. ✓
  Both heads' scores come out identical whether you reconstruct the key or score against the cached
  latent — so MLA stores 2 numbers, not 8, with no change to the attention result.

**Where it runs.** From [[kv-cache]], cache memory $\propto 2 \times n_\text{tokens} \times
n_\text{layers} \times (\text{KV size per token})$, and for long context or large batch it dominates
inference. MLA cuts the per-token term from $2\,h\,d_\text{head}$ to $d_c$ — a cache comparable to
sharing a single head, but, because of the per-head up-projections, with the quality of full
[[multi-head-attention]].

## Prerequisites

- [[multi-head-attention]]
- [[kv-cache]]
- [[low-rank-factorization]]

## Sources

- DeepSeek-AI — *DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*
  (2024), arXiv:2405.04434
