---
id: online-softmax
title: Online Softmax
summary: Online softmax (also called streaming softmax) computes a numerically-stable softmax over a long list of values while seeing them one block at a time, in a single pass — never…
type: concept
tags: [ml/llm/architecture]
prereqs: [softmax, probability-distribution]
sources: ["FlashAttention (Dao et al., 2022), arXiv:2205.14135"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Online Softmax

## Summary

**Online softmax** (also called *streaming softmax*) computes a numerically-stable
[[softmax]] over a long list of values while seeing them **one block at a time, in a single
pass** — never holding the whole list at once. It keeps a small **running summary** as blocks
arrive and, whenever a later block reveals a value larger than anything seen so far, **rebases**
the summary with one cheap multiplication. After the final block the result is *exactly* the
ordinary [[softmax]] over the full list. This is the engine inside FlashAttention, ring
attention, and paged attention.

## Grounded explanation

Recall from [[softmax]] that turning a list of real values $x_1,\dots,x_n$ into a [[probability-distribution]]
means exponentiating each and dividing by the total: weight
$w_i = e^{x_i}/\sum_j e^{x_j}$. In practice one first subtracts the largest value $m=\max_j x_j$
for **numerical stability**: because subtracting the same constant from every value multiplies
top and bottom by the identical factor $e^{-m}$, which cancels, the answer is unchanged — yet
every exponential is now $\le 1$, so nothing overflows. So the stable form is

$$w_i = \frac{e^{x_i-m}}{\ell}, \qquad m=\max_j x_j, \qquad \ell=\sum_{j} e^{x_j-m}.$$

Here $m$ is the **maximum** of the values and $\ell$ (the *denominator* or *normalizer*) is the
sum of the shifted exponentials. The difficulty: computing $m$ and $\ell$ this way seems to need
**all** the values up front — $m$ is a max over the whole list, and $\ell$ sums over the whole
list. If the values arrive in chunks (and the full list is too large to store), you appear stuck.

**The key insight: the reference $m$ is a free choice, so use the max-so-far and correct it
later.** Online softmax carries two running numbers as it walks the blocks: a running maximum
$m$ (the largest value seen so far) and a running denominator $\ell$ (the sum of shifted
exponentials, each shifted by the *current* $m$). Process one block, fold its values into
$(m,\ell)$, discard the block, fetch the next.

The one non-obvious step is what happens when a new block contains a value larger than the
current $m$. Every exponential already accumulated in $\ell$ was shifted by the **old** maximum
$m_\text{old}$; once the maximum grows to $m_\text{new}$, those terms are shifted by the wrong
(too-small) reference and are therefore too large. The fix is exact and cheap. An old term
$e^{x-m_\text{old}}$ must become $e^{x-m_\text{new}}$; their ratio is

$$\frac{e^{x-m_\text{new}}}{e^{x-m_\text{old}}} = e^{\,m_\text{old}-m_\text{new}},$$

which **does not contain $x$ at all** — it is the *same* factor for every value in the carried
sum. So a single multiplication, $\ell \leftarrow e^{\,m_\text{old}-m_\text{new}}\cdot\ell$,
rebases the entire running denominator at once, no matter how many values it already summed.
After rebasing, set $m \leftarrow m_\text{new}$ and add the new block's shifted exponentials
$\sum e^{x-m_\text{new}}$. (If the new block's values are all below the current $m$, the factor
is $e^0=1$ and nothing changes — but the mechanism still adds the block's terms.) Because every
intermediate $\ell$ is consistent with the maximum seen so far, after the last block $m$ and
$\ell$ equal the true max and the true normalizer, and the weights $w_i=e^{x_i-m}/\ell$ are
**identical** to a one-shot [[softmax]] over the entire list.

**Worked instance.** Take the values $[1,3,2,5]$ split into two blocks, $[1,3]$ then $[2,5]$.

- *Block 1* $[1,3]$: the max so far is $m=3$. Shifted exponentials: $e^{1-3}=0.135$ and
  $e^{3-3}=1$, so $\ell = 0.135+1 = 1.135$.
- *Block 2* $[2,5]$: it contains $5$, larger than the current $m=3$, so the maximum grows to
  $m_\text{new}=5$. Rebase the carried denominator by $e^{\,3-5}=e^{-2}=0.135$:
  $0.135\cdot 1.135 = 0.153$. Now add this block's shifted terms $e^{2-5}=0.0498$ and
  $e^{5-5}=1$: $\ell = 0.153 + 0.0498 + 1 = 1.203$.
- *Check.* A one-shot stable [[softmax]] over all four values uses $m=5$ and
  $\ell = e^{1-5}+e^{3-5}+e^{2-5}+e^{5-5} = 0.0183+0.135+0.0498+1 = 1.203$ — the same number,
  and hence the same weights. The single pass reproduced the exact answer without ever holding
  all four values together.

**Carrying an output too.** In attention each value comes paired with a vector, and one also
wants the weighted average of those vectors, $O = \sum_i w_i\,V_i$. The same trick carries a
running numerator $O = \sum e^{x-m} V$ alongside $\ell$, rebased by the *same* score-independent
factor $e^{\,m_\text{old}-m_\text{new}}$ whenever the maximum grows; the final answer is
$O/\ell$. This block-at-a-time staging is exactly what lets FlashAttention stream key/value
tiles through a GPU's tiny fast memory without ever materializing the full attention matrix,
what lets ring attention split the sequence across devices and combine their partial summaries,
and what lets paged attention consume scattered cache blocks one address at a time — each folds
a block into the running $(m,\ell,O)$ and discards it. (These are applications, not part of the
definition.)

## Prerequisites

- [[softmax]]
- [[probability-distribution]]

## Sources

- Dao, Fu, Ermon, Rudra, Ré — *FlashAttention: Fast and Memory-Efficient Exact Attention with
  IO-Awareness* (2022), arXiv:2205.14135
