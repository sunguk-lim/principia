# Softmax

## Meaning

**Goal:** turn scores into normalized weights and explain why subtracting a common number changes nothing.

A score ranks an option but is not yet a probability. Softmax converts a finite list of real scores into positive weights whose total is one. It preserves their ordering without choosing only the winner.

## Mechanism

For scores $z_1,\ldots,z_n$, let $m$ be their maximum. The weight of option $i$ is

$$
p_i=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}.
$$

The [[exponential-function]] makes each numerator positive; dividing by the sum normalizes them into a [[probability-distribution]]. Subtracting $m$ multiplies every numerator and the denominator by the same factor, so it cancels. It also keeps exponentials at most one, avoiding exponential overflow. Finite-precision arithmetic can still round tiny weights to zero.

## One example

For scores $[0,\log 2]$, exponentiation gives $[1,2]$. Dividing by three gives weights $[1/3,2/3]$. Adding 100 to both scores leaves those weights unchanged. Multiplying the scores by 100 does not: it sharpens their relative differences.

## Check your understanding

Would scores $[5,5]$ give different weights from $[0,0]$?

**Answer:** no. Both yield $[1/2,1/2]$ because only score differences matter. Normalization alone does not guarantee that these weights are calibrated predictions of real-world frequencies.

Reference: [online normalizer paper](https://arxiv.org/abs/1805.02867).
