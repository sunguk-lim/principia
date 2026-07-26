---
id: lora
title: LoRA (Low-Rank Adaptation)
summary: LoRA (Low-Rank Adaptation) adapts a large pretrained model to a new task by freezing the original weight matrix W and learning only a small low-rank update ΔW = B·A.
type: concept
tags: [ml/deep-learning]
prereqs: [low-rank-factorization, fine-tuning, transformer-attention]
sources: [arxiv:2106.09685]
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# LoRA (Low-Rank Adaptation)

## Summary

LoRA (Low-Rank Adaptation) adapts a large pretrained model to a new task by
*freezing* the original weight matrix `W` and learning only a small low-rank
update `ΔW = B·A`. At inference the model uses `W + B·A`. Because only `B` and
`A` are trained, the number of trainable parameters drops by orders of magnitude.

## Grounded explanation

The whole idea rests on [[low-rank-factorization]]: instead of updating all `d²`
entries of `W`, LoRA assumes the *change* needed to adapt the model is itself
low-rank, so it represents `ΔW` as `B·A` with a tiny `r`. Training touches only
`2dr` parameters while `W` stays fixed.

Where these weight matrices live inside the model is now grounded in
[[transformer-attention]] — LoRA injects its low-rank update into the query and
value projections ($W_q$, $W_v$). What is being *adapted* — [[fine-tuning]] — is
the one prerequisite of LoRA still on the frontier.

## Prerequisites

- [[low-rank-factorization]]
- [[fine-tuning]]
- [[transformer-attention]]

## Visual

**1 · Symbols** — 🟦 scalar · 🟩 vector · 🟧 matrix

| Symbol | Type | Shape | Meaning |
|--------|------|-------|---------|
| $W$ | 🟧 matrix | $d\times d$ | frozen pretrained weight (never trained) |
| $\Delta W$ | 🟧 matrix | $d\times d$ | the learned update, forced to be low-rank |
| $B$ | 🟧 matrix | $d\times r$ | trainable factor, initialized to $0$ |
| $A$ | 🟧 matrix | $r\times d$ | trainable factor, initialized random |
| $x$ | 🟩 vector | $d$ | input activation |
| $h$ | 🟩 vector | $d$ | output activation |
| $r$ | 🟦 scalar | — | rank of the update; $r \ll d$ |
| $\alpha$ | 🟦 scalar | — | scaling constant (update scaled by $\alpha/r$) |
| $d$ | 🟦 scalar | — | model dimension |

**2 · Equation**

$$\Delta W = B\,A \qquad \text{(the update is low-rank)}$$


$$h = W x + \tfrac{\alpha}{r}\,B\,A\,x \qquad \text{(forward pass — only } B,\,A \text{ are trained)}$$

**3 · Shape**

![LoRA: the effective weight W-prime equals the frozen W plus the low-rank update B times A](lora.svg)

Trainable parameters: $2dr$ (just $B$ and $A$) instead of $d^2$ — $W$ never
moves. At inference, $B\,A$ folds back into $W$, so LoRA adds **zero** latency.

## Sources

- arxiv:2106.09685
