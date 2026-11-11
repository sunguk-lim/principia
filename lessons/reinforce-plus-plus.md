# REINFORCE Plus Plus

## Meaning

REINFORCE++ is a critic-free training framework whose normalization uses statistics from the global batch rather than a small prompt group. The name does not mean it is the bare, unclipped REINFORCE estimator. Its documented variants differ in group sampling and reference-policy regularization.

## Mechanism

In the primary general variant, compute response-return advantages, including the specified per-token reference-divergence reward terms when enabled, then subtract the global-batch mean and divide by its standard deviation plus a stabilizing epsilon. Apply the resulting signals to a [[proximal-policy-optimization]] surrogate without a learned value model. One sampled response per prompt can be used.

The baseline variant samples several responses per prompt, subtracts the prompt group's mean first, then normalizes those centered signals using global-batch statistics. This separates prompt-relative comparison from the scaling measure. Reference regularization can instead be a separate loss in that variant. The [[advantage-baseline]] argument does not make a data-dependent standard-deviation division automatically unbiased.

The [[kl-divergence]] measures policy disagreement with a reference; it is separate from standard-deviation normalization.

## One example

Suppose two groups have rewards [0,1] and [0,3]. Their centered values are [-.5,.5] and [-1.5,1.5]. Using the population standard deviation over all four centered values gives sqrt((.25+.25+2.25+2.25)/4)=sqrt(1.25)≈1.118. Globally scaled values are about [-.447,.447,-1.342,1.342]. Scaling each group by its own standard deviation would instead give [-1,1] in both groups. The choice changes their relative update weights; these numbers illustrate the operation, not a universal preferred reward scale.

## Boundaries and check

Record whether statistics are computed over responses or valid tokens, whether a sample or population denominator is used, and which values enter the distributed global batch. Per-worker normalization is not global normalization. Finite-batch estimates remain data-dependent; asymptotic arguments require their assumptions and do not certify every clipped update. Equal rewards should produce centered zero signals with a guarded denominator, not an assumed explosion.

Test distributed/microbatch equivalence, zero variance, reward-scale shifts and varying lengths. Compare held-out quality, reward exploitation, ratio tails and total tokens. Does global scaling solve an incorrect verifier? No: it redistributes the supplied signal rather than establishing its truth.
