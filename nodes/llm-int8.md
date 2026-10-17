---
id: llm-int8
title: LLM.int8 Mixed-Precision Decomposition
summary: LLM.int8 separates outlier input-feature dimensions into a higher-precision matrix product while using vector-wise 8-bit quantization for the remaining dimensions.
type: concept
tags: [ml/llm/inference]
prereqs: [post-training-quantization, numeric-precision-formats, matrix-multiplication]
sources: [https://arxiv.org/abs/2208.07339]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# LLM.int8 Mixed-Precision Decomposition

## Summary

LLM.int8 separates outlier input-feature dimensions into a higher-precision matrix product while using vector-wise 8-bit quantization for the remaining dimensions.

## Grounded explanation

A small number of very large activation features can force a shared quantization range to waste most of its available levels. LLM.int8 addresses this with two mechanisms: vector-wise scaling for most of a product, and a separate high-precision path for outlier feature dimensions. It is more specific than merely loading all weights into an 8-bit container.

Let $X$ be an activation matrix with $n$ rows and $d$ input features, and $W$ a weight matrix with $d$ rows and $r$ output features. Their [[matrix-multiplication]] yields $Y=XW$. Let $O$ be the selected set of outlier input-feature indices, and let $N$ contain the remaining indices. Partitioning the contracted dimension gives the exact identity

$$XW=X_{:,N}W_{N,:}+X_{:,O}W_{O,:}.$$

LLM.int8 approximates the first term with vector-wise 8-bit quantization and computes the second in higher precision, then combines the outputs. Vector-wise normalization gives different activation rows and weight columns their own scaling factors rather than forcing an entire matrix to share one range. This is a [[post-training-quantization]] deployment procedure. The distinction between 8-bit storage/arithmetic and the higher-precision path rests on [[numeric-precision-formats]]; the decomposition itself does not imply that training is occurring.

For an illustrative row $x=[1,2,100]$ and column $w=[3,4,5]^\top$, selecting the last feature as an outlier gives ordinary contribution $1\cdot3+2\cdot4=11$ and outlier contribution $100\cdot5=500$. Their sum is $511$ before any approximation. The 8-bit path can focus its range on the first two activation coordinates instead of accommodating $100$. Selecting a dimension preserves its entire contribution, including the matching weight slice; dropping that slice would be pruning, not this decomposition.

The threshold for outlier selection trades approximation error against extra higher-precision work. Too many outlier dimensions can reduce memory savings and add gather, conversion, and launch overhead. Distributions and outlier locations can differ across layers and inputs. A numerical format alone does not establish performance: measure target-kernel support, peak memory, batch-dependent latency, throughput, and end-to-end task quality against the same unquantized baseline. Source-specific claims of unchanged quality apply only to the experiments that measured them, not every deployment.

## Prerequisites

- [[post-training-quantization]]
- [[numeric-precision-formats]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/abs/2208.07339>
