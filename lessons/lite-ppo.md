# LitePPO

## Meaning

LitePPO is the deliberately small combination studied in “Tricks or Traps?” It uses group-level mean centering with batch-level standard-deviation scaling and token-level loss aggregation. Its identity is the coordinated normalization and aggregation contract, not merely using fewer PPO hyperparameters.

## Mechanism

Generate several responses per prompt as in [[group-relative-policy-optimization]]. For reward R_i, subtract the mean of its prompt group's rewards. Scale by a standard deviation measured at the declared batch level rather than separately for each prompt group. Use these advantages in the vanilla [[proximal-policy-optimization]] surrogate without a learned critic, and sum over valid tokens with the global token denominator from [[token-sequence-loss-weighting]].

Specify exactly what batch values enter the standard deviation and how workers combine them. “Batch standard deviation” does not imply the mean is also global; mixing the two would implement a different algorithm. Reference penalties, clipping ranges and extra filtering are independent settings rather than implied additions.

## One example

Two prompt groups produce rewards [0,1] and [2,4]. Their group-centered rewards are [-.5,.5] and [-1,1]. The population standard deviation of the original batch rewards [0,1,2,4] is sqrt(2.1875)≈1.479. If that is the selected batch-scale convention, normalized advantages are approximately [-.338,.338,-.676,.676]. If instead the implementation measures spread after group centering, it obtains sqrt(.625)≈.791 and different magnitudes. The paper's group-mean/batch-scale design must be mapped to the actual implementation; an example's convention is not permission to silently swap definitions.

With unequal response lengths, token aggregation then changes each response's total contribution independently of these advantage values.

## Boundaries and check

The primary paper reports controlled comparisons under its setups, not a general law that only two training choices matter. Reward quality, sampling freshness, model initialization and generation length remain consequential. Validate reference calculations, zero-spread safeguards, distributed consistency and per-length gradients. Compare component ablations with matched rollout tokens and report held-out quality, stability and compute. Does sharing a batch scale guarantee equal influence for all prompts? No: reward contrasts, response lengths and clipping determine the actual contributions.
