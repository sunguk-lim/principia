---
id: rmsnorm
title: RMSNorm
summary: RMSNorm rescales an activation vector by its root mean square without subtracting its mean, then applies learned coordinate gains.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network]
sources: [https://arxiv.org/abs/1910.07467, https://docs.pytorch.org/docs/stable/generated/torch.nn.RMSNorm.html]
status: explained
created: 2026-06-23
updated: 2026-11-13
---

# RMSNorm

## Summary

Root mean square normalization (RMSNorm) rescales an activation vector by a shared root-mean-square denominator without subtracting its mean. Learned coordinate gains then allow the next layer to use different scales. It is a conditioning operation inside a [[neural-network]], not a promise that every final output has unit size or that training cannot become unstable.

## Grounded explanation

Let x=(x_1,...,x_d) be an activation vector with d coordinates, g=(g_1,...,g_d) a learned gain vector of the same shape, and epsilon a positive numerical stabilizer. Define r, a scalar denominator, and y, the output vector, by

$$r=\sqrt{\frac{1}{d}\sum_{j=1}^{d}x_j^2+\varepsilon},\qquad y_i=g_i\frac{x_i}{r}.$$

All coordinates share r, but have their own g_i. Omitting mean subtraction distinguishes RMSNorm from the usual centered layer-normalization operation. This reduces arithmetic in the normalization formula; actual speed depends on kernels, shapes, precision, fusion and hardware. Comparable quality or a speedup must be measured for the specific architecture and training setup, not inferred universally from fewer operations.

Before the learned gain, dividing by a positive scalar preserves the direction and coordinate ratios of a nonzero vector. It deliberately removes much of the overall scale information; it is not generally information-preserving. Nonuniform gains can then change direction. A model may encode useful information in activation magnitude, so discarding scale is an architectural choice rather than a theorem that magnitude never matters.

With epsilon=0 and nonzero x, the intermediate vector x/r has exactly unit RMS. With positive epsilon its RMS is smaller than one, except as an approximation when the squared input RMS greatly exceeds epsilon. The final y need not have unit RMS because g is learned. At x=0 and positive epsilon, the output is zero rather than an undefined division. Thus neither the stabilized intermediate nor the final output universally satisfies the old exact-unit-RMS claim.

### One worked instance

Take x=(3,0,4), d=3 and epsilon=1/3, chosen large only to make the arithmetic visible. The mean square is (9+0+16)/3=25/3. Adding epsilon gives 26/3, so r is approximately 2.944. The intermediate vector is approximately (1.019,0,1.359), with RMS sqrt(25/26), approximately .981, not one.

With gains g=(2,1,.5), y is approximately (2.038,0,.679). The first-to-third coordinate ratio changes from 3:4 before gain to 3:1 after gain. The denominator preserved direction; the unequal gains did not. In an implementation epsilon is normally much smaller than this illustrative choice, and its default may depend on the dtype or library.

### Boundaries and validation

Test zero and near-zero vectors, very large values, supported dtypes, normalized axes and nonuniform gains against the stated formula. Pin the implementation’s epsilon placement and accumulation precision. A positive stabilizer changes exact rescaling invariance near zero. RMSNorm does not center the vector, does not ensure a bounded network-wide gain and does not alone establish convergence. Architectural placement, such as normalization before a block, is another design decision.

## Prerequisites

- [[neural-network]]

## Sources

- <https://arxiv.org/abs/1910.07467>
- <https://docs.pytorch.org/docs/stable/generated/torch.nn.RMSNorm.html>
