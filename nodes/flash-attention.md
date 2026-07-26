---
id: flash-attention
title: FlashAttention
summary: FlashAttention computes the exact same output as ordinary transformer-attention, but reorganizes the work so a GPU moves far less data.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, softmax, online-softmax]
sources: ["FlashAttention (Dao et al., 2022), arXiv:2205.14135"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# FlashAttention

## Summary

FlashAttention computes the **exact same** output as ordinary [[transformer-attention]], but
reorganizes the work so a GPU moves far less data. The naive method builds the whole $n \times n$
matrix of attention scores in memory; FlashAttention instead **streams** the keys and values in small
**tiles** and keeps a tiny **running summary**, so it never stores the full score matrix. The trick
that makes this possible is [[online-softmax]] — an incremental, streaming form of [[softmax]]. Same answer — but memory
traffic drops from $O(n^2)$ to $O(n)$, a large speedup that makes long context affordable.

![FlashAttention — animated (37 steps, loops): LEFT, the iteration space — the S = Q·Kᵀ block grid (2×2 tiles of 2×2 scores, conceptual, never materialized) swept by a gold cursor under the nested-loop kernel pseudocode with a live line pointer and (i, j) counters; each block is computed once (S11=[[2,0],[1,1]], S12=[[2,4],[2,2]], S21=[[0,2],[1,0]], S22=[[2,0],[1,2]]), folded into the carry, and marked done. RIGHT, the memory substrate — SRAM (on-chip, tiny: resident K_j·V_j pair, Q_i, derived S/P̃/α, and the carry m, ℓ, O that resets each row) over THE LINK (the bottleneck: load arrow up, write arrow down) over HBM (off-chip, huge: Q, K, V, O at true 4×2 shape with tile dividers; not to scale — A100: 40 GB vs 192 KB/SM). Every transfer rides a drawn arrow: K_j,V_j stream up each inner step (evicting the previous pair), Q_i loads once per row, O_i writes back once per row. The worked example (d=2, N=4, Br=Bc=2) runs BOTH outer iterations numerically: row 1 rebases at j=2 (α = e^(2−4) = 0.14 — ONE multiply re-references the whole carry), normalizes O1=[[1.76,1.67],[1.23,1.23]]; the carry visibly resets to (−∞, 0, 0), then row 2 repeats on fresh data (rebase α=0.37, O2=[[0.62,1],[1.46,1.34]]). Invariant: after every folded tile, O/ℓ = exact softmax over the keys seen so far. Payoff: naive ships the n×n score matrix across the link (O(n²) traffic); FlashAttention keeps one block resident — O(n), same output bit-for-bit.|960](flash-attention.svg)

## Grounded explanation

Recall from [[transformer-attention]] that for one query the output is $O = \mathrm{softmax}(S)\cdot V$,
where $S_j = q\cdot k_j/\sqrt{d}$ is the **score** of that query (vector $q$) against key $j$ (vector
$k_j$), there are $n$ keys, and $V_j$ is key $j$'s **value vector**. So the output is a **weighted
average of the value vectors**, the weights coming from [[softmax]] over the scores. The naive route
computes all $n$ scores, softmaxes them, then multiplies by $V$ — it needs the whole score row at once,
and on a GPU the dominant cost is *moving* that data, not the arithmetic.

FlashAttention reaches the identical answer while looking at only a few keys at a time. Three ideas:

**1 — The output is a weighted average; the denominator normalizes it.**
The [[softmax]] weight is $w_j = e^{S_j}/\ell$ with $\ell = \sum_j e^{S_j}$, and the output is
$\sum_j w_j V_j$. Dividing by $\ell$ is exactly what forces the weights to sum to 1 — without it you'd
have a raw sum, not an average. So track two running quantities: a numerator $O = \sum_j e^{S_j} V_j$
and a denominator $\ell = \sum_j e^{S_j}$; the answer is $O/\ell$.

**2 — Subtracting the max changes nothing, so we don't need the whole row at once.**
From [[softmax]], subtracting the same constant from every score leaves the result unchanged (the
common factor cancels top and bottom), and subtracting the **largest** score keeps every exponential
$\le 1$ so nothing overflows. Let $m$ be the **largest score seen so far** and redefine
$w_j = e^{S_j - m}$, $O = \sum w_j V_j$, $\ell = \sum w_j$. Because *any* reference $m$ yields the same
final $O/\ell$, we can use the max-so-far now and correct it later — which is what permits processing
keys incrementally.

**3 — Stream the keys in tiles, carrying $(m, \ell, O)$, and rebase when a bigger score appears — the [[online-softmax]] algorithm applied to attention.**
Walk the keys a **tile** at a time, keeping the running summary $(m, \ell, O)$. When a new tile holds a
score larger than the current $m$, the carried $\ell$ and $O$ were measured against the old, smaller
reference, so they are too large. Fix them with **one multiplication**: each old weight
$e^{S - m_\text{old}}$ must become $e^{S - m_\text{new}}$, and their ratio
$e^{\,m_\text{old} - m_\text{new}}$ is **independent of the score $S$** — so the *same* factor rebases
every carried key at once. Multiply the carried $\ell$ and $O$ by $e^{\,m_\text{old} - m_\text{new}}$,
then add the new tile's contributions. After the last tile, divide: $O/\ell$. At every step $O/\ell$
equals the true [[softmax]] over the keys seen so far, so the final value is the exact full-row result —
yet the whole score row never existed at once.

**Worked instance.** Scores $S = [1, 3, 2, 5]$, values $V = [10, 20, 30, 40]$, two keys per tile.

- *Tile 1* (scores 1, 3): $m = 3$; weights $e^{1-3}, e^{3-3} = 0.135,\, 1$; $\ell = 1.14$;
  $O = 0.135\cdot 10 + 1\cdot 20 = 21.4$; running answer $O/\ell = 18.8$.
- *Tile 2* (scores 2, 5): new max $5 > 3$, so rebase the carry by $e^{3-5} = 0.135$; new weights
  $e^{2-5}, e^{5-5} = 0.050,\, 1$; $\ell = 0.135\cdot 1.14 + (0.050 + 1) = 1.20$;
  $O = 0.135\cdot 21.4 + 0.050\cdot 30 + 1\cdot 40 = 44.4$.
- *Final* $O/\ell = 44.4 / 1.20 = 36.9$ — identical to a one-shot softmax over all four keys.

**Why it matters.** A GPU has a small, fast on-chip memory (**SRAM**) and a large, slow off-chip memory
(**HBM**); the bottleneck is traffic between them. The naive method writes and reads the full
$n \times n$ score matrix in HBM — $O(n^2)$ traffic. FlashAttention keeps only the current tile plus the
small summary $(m, \ell, O)$ in SRAM and never writes the score matrix, so it moves $O(n)$ data. (In
full, both inputs are tiled: an outer loop over blocks of queries wraps an inner loop that streams the
key/value tiles.) The output is bit-for-bit the same as [[transformer-attention]]; only *where* the
computation happens and *how* [[softmax]] is staged change.

## Prerequisites

- [[transformer-attention]]
- [[softmax]]
- [[online-softmax]]

## Sources

- Dao, Fu, Ermon, Rudra, Ré — *FlashAttention: Fast and Memory-Efficient Exact Attention with
  IO-Awareness* (2022), arXiv:2205.14135
