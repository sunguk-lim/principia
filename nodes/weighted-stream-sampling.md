---
id: weighted-stream-sampling
title: "Weighted Stream Sampling"
summary: "Weighted stream sampling changes the target selection law through explicit positive item weights, distinguishing sequential draw probabilities from final inclusion probabilities and from recency policies."
type: concept
tags: [math/probability]
prereqs: [reservoir-sampling, logarithm]
sources: [https://arxiv.org/html/1012.0256v2]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Weighted Stream Sampling

## Meaning

A uniform event reservoir is wrong when the intended sample deliberately favors particular records or recent traffic. Weighted sampling makes that preference explicit. Before choosing an algorithm, specify replacement, the meaning of each weight, and whether weights change over time. A sample that favors recent events is not a uniform sample of the entire history.

## Mechanism

[[reservoir-sampling]] maintains a fixed-size uniform sample. For positive weighted sampling without replacement under sequential weight-proportional draws, one key-based method draws independent uniforms $U_i$ strictly between zero and one for each record i with positive weight $w_i$, and keeps the k largest keys $K_i=U_i^{1/w_i}$. Equivalently retain the k smallest values $-\log(U_i)/w_i$, using the [[logarithm]] to avoid underflow. For a threshold x between zero and one, Pr(K_i≤x)=Pr(U_i≤x^{w_i})=x^{w_i}: increasing the weight moves the key distribution upward, making a retained large key more likely. Equivalently, larger weights favor smaller negative-log arrival keys; equal weights recover a uniform ranking. The primary weighted-stream treatment distinguishes this law from requiring final marginal inclusion probabilities proportional to weights. For k>1 they are not generally the same.

## One example

For a one-slot sample with weights 1 and 3, selection probabilities are 1/4 and 3/4 under the proportional draw law. For a two-slot sample from only those same two records, both are included with probability one: final inclusion is no longer in a 1:3 ratio.

## Check your understanding

Can weighted sampling guarantee unbiased training or eliminate drift? No. Validate the intended population, inclusion frequencies, duplicate policy, numerical stability and recovery. A bounded heap can retain the top k keys, but it does not fix an incorrect weight law. If estimating a different population quantity from the sample, derive the required correction from the actual design rather than assuming raw weights are inverse inclusion probabilities.

## Prerequisites

- [[reservoir-sampling]]
- [[logarithm]]

## Sources

- <https://arxiv.org/html/1012.0256v2>
