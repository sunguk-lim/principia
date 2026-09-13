# Online softmax

## Meaning

**Goal:** update a stable softmax denominator as scores arrive in blocks.

The final [[softmax]] denominator depends on every score. Online normalization summarizes scores seen so far with two numbers: their maximum $m$ and the sum $\ell$ of exponentials shifted by that maximum.

## Mechanism

Start with the first nonempty block. For a new block $B$, compute its maximum and choose the larger of that value and the old maximum:

$$
m'=\max(m,\max_{x\in B}x),\qquad
\ell'=e^{m-m'}\ell+\sum_{x\in B}e^{x-m'}.
$$

The factor $e^{m-m'}$ converts the old sum to the new reference point. It is identical for every old score, so their individual values need not be kept to update the denominator.

## One example

The first block $[0,0]$ gives $m=0$ and $\ell=2$. A second block $[\log 2]$ raises the maximum. The old sum becomes $2\times 1/2=1$; the new term is one. Thus $\ell'=2$, matching a direct calculation with all three scores.

## Check your understanding

Can those two running numbers recover every individual output probability after discarding all scores?

**Answer:** no. They summarize the normalizer, not the original scores. Producing every probability requires retaining or revisiting scores. A fused weighted sum can instead carry an additional numerator; this is an application to [[flash-attention]], not a prerequisite for understanding the recurrence.

Reference: [Milakov and Gimelshein](https://arxiv.org/abs/1805.02867).
