---
id: rmsnorm
title: RMSNorm
summary: "RMSNorm (root-mean-square normalization) is a small layer placed between the layers of a neural-network that rescales each activation vector to a stable size: it divides the…"
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network]
sources: [llm_parallelism_strategies.jsx]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# RMSNorm

## Summary

**RMSNorm** (root-mean-square normalization) is a small layer placed between
the layers of a [[neural-network]] that rescales each activation vector to a
stable size: it divides the vector by its root mean square and then multiplies
each coordinate by a learned gain. Holding activations near a fixed scale keeps
training well-conditioned, and because RMSNorm does this with fewer operations
than the older LayerNorm, it has become the standard normalization layer in
modern large language models.

## Grounded explanation

Recall from [[neural-network]] that a layer takes a vector, multiplies it by a
weight matrix, adds a bias, and applies a nonlinearity, and that many such layers
are stacked. The output of each layer is an **activation vector**: the list of
numbers passed forward to the next layer. As these vectors flow through a deep
stack, their overall magnitude can drift — growing or shrinking layer by layer —
and that drift makes learning unstable, because the size of the updates a layer
should make depends on the size of the numbers reaching it. A **normalization
layer** fixes this by rescaling each activation vector to a predictable size
before the next layer sees it.

**The central object.** RMSNorm normalizes by the *root mean square* of the
vector. Write the activation vector as $x = (x_1, x_2, \dots, x_d)$, where $d$ is
its **dimension** (the number of coordinates). The root mean square is the square
root of the average of the squared coordinates:

$$\mathrm{RMS}(x) = \sqrt{\tfrac{1}{d}\sum_{i=1}^{d} x_i^2}.$$

Here $\sum_{i=1}^{d} x_i^2$ means "add up the squares of all $d$ coordinates," and
$\tfrac{1}{d}$ averages them. RMS is one single positive number that measures the
typical size of a coordinate of $x$. RMSNorm divides every coordinate by it:

$$\hat{x}_i = \frac{x_i}{\mathrm{RMS}(x)}.$$

After this division the rescaled vector $\hat{x}$ has root mean square equal to
$1$, regardless of how large or small $x$ was. That is the **invariant** RMSNorm
maintains: every activation vector leaves the layer at unit RMS, so downstream
layers always receive numbers at the same scale.

**Why it works, and what it preserves.** Dividing by a single positive number does
not change the *direction* of the vector — it only changes its *length*. So
RMSNorm throws away the magnitude of $x$ (which is the part that drifts and causes
trouble) while keeping the pattern of relative values among the coordinates (which
is the part that carries information). This is the one non-obvious point: rescaling
by a scalar is information-preserving in the only sense that matters here, because
the meaningful content of an activation lives in the *ratios* between coordinates,
not in their absolute size.

**The learned gain.** A fixed unit scale is not always what the next layer wants,
so RMSNorm restores flexibility with a **gain** vector $g = (g_1, \dots, g_d)$ —
one learned number per coordinate, adjusted during training like any other
parameter of the [[neural-network]]. The final output multiplies coordinate by
coordinate:

$$y_i = g_i \,\hat{x}_i = g_i \,\frac{x_i}{\mathrm{RMS}(x)}.$$

(In practice a tiny constant $\varepsilon$ is added inside the square root to avoid
dividing by zero when $x$ is all zeros; it does not change the idea.)

**Contrast with LayerNorm — the "why fewer operations".** The layer RMSNorm
replaced is **LayerNorm**, which does three things: it subtracts the *mean* of the
coordinates (re-centering the vector around zero), divides by the *standard
deviation* (the spread of the coordinates around that mean), and adds a learned
*bias* vector. RMSNorm keeps only the rescaling and drops the other two: no mean is
computed, no centering happens, and there is no bias. The payoff is that RMSNorm is
cheaper — computing a mean and re-centering is extra arithmetic over every
coordinate, and RMSNorm skips it — yet across modern models it trains just as well.
That combination, cheaper and no worse, is why it has largely displaced LayerNorm.

**Worked instance.** Take the activation vector $x = (3, 0, 4)$, so $d = 3$. Square
each coordinate: $3^2 = 9$, $0^2 = 0$, $4^2 = 16$. Sum them: $9 + 0 + 16 = 25$.
Average over the three coordinates: $25 / 3 = 8.333$. Take the square root:
$\mathrm{RMS}(x) = \sqrt{8.333} = 2.887$. Now divide each coordinate by $2.887$:

$$\hat{x} = \left(\tfrac{3}{2.887},\ \tfrac{0}{2.887},\ \tfrac{4}{2.887}\right)
= (1.039,\ 0,\ 1.386).$$

With a gain of $g = (1, 1, 1)$ the output equals $\hat{x}$ itself. Notice two
things. The middle coordinate was $0$ and stays $0$, while the first and fourth
keep their ratio: $3 : 4$ before, $1.039 : 1.386$ after — the same $3 : 4$. So the
*direction* of the vector is untouched; only its *scale* changed, from an RMS of
$2.887$ down to an RMS of $1$. That is exactly the behavior RMSNorm promises:
fix the size, leave the meaning.

**Where it sits.** In a modern model such as LLaMA or Mamba, an RMSNorm layer sits
at the entrance of each block, mapping a vector of activations to a vector of the
same shape, normalized and re-scaled by the gain, just before the block's heavier
computation runs. It is a lightweight conditioning step that the rest of the
[[neural-network]] relies on to stay numerically stable.

## Prerequisites

- [[neural-network]]

## Sources

- `llm_parallelism_strategies.jsx` — Mamba block diagram, RMSNorm stage:
  `x̂ = γ · x / √(mean(x²)+ε)`, shown as the `(L,D)→(L,D)` normalization at the
  entrance of the Mamba block.
