---
id: layer-normalization
title: Layer Normalization
summary: Layer normalization standardizes each individual activation vector across its features, then restores learnable per-feature scale and offset so a neural network receives consistently scaled inputs.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network]
sources:
  - https://arxiv.org/abs/1607.06450
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# Layer Normalization

## Summary

**Layer normalization** normalizes one activation vector at a time: it centers
that vector's features around their own mean and scales them by their own
spread. Learned scale and offset parameters then let a [[neural-network]] keep
whatever feature-wise range is useful.

## Grounded explanation

A layer of a [[neural-network]] passes an activation vector to the next layer.
When the scale of those activations varies substantially, subsequent layers
must continually adapt to changing input ranges. Layer normalization makes the
coordinates of *each one vector* comparable before the next computation. It
does not compute statistics across the batch, so its result for one example is
the same whether that example is evaluated alone or alongside other examples.

Let an activation vector be $x=(x_1,\ldots,x_d)$, where $d$ is its number of
features. Its feature mean and variance are

$$
\mu = \frac{1}{d}\sum_{i=1}^d x_i,
\qquad
\sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i-\mu)^2.
$$

Layer normalization first produces a centered, unit-scale coordinate and then
applies learned per-feature gain $\gamma_i$ and offset $\beta_i$:

$$
y_i = \gamma_i\frac{x_i-\mu}{\sqrt{\sigma^2+\varepsilon}}+\beta_i.
$$

Here $\varepsilon$ is a small positive constant that prevents division by zero.
Subtracting $\mu$ makes the normalized coordinates sum to zero; dividing by the
square root of the variance makes their average squared deviation approximately
one. The gain and offset matter because normalization should stabilize the
representation without forcing every feature to have the same final preferred
scale or mean.

For a concrete vector $x=(2,4,6)$, the mean is $\mu=4$. The squared deviations
are $4,0,4$, so $\sigma^2=8/3$. Ignoring the tiny $\varepsilon$, the normalized
vector is approximately $(-1.225,0,1.225)$. With $\gamma=(2,1,1)$ and
$\beta=(1,0,-1)$, the output becomes approximately
$(-1.449,0,0.225)$. Thus the operation removes the input vector's shared shift
and scale, while the learned parameters can still deliberately reshape each
coordinate.

Layer normalization is distinct from normalizing over examples in a mini-batch:
its statistics are local to one activation vector. That locality is useful for
sequence models and for inference, where batch composition can change. It does
not guarantee training stability by itself; placement in a residual block,
