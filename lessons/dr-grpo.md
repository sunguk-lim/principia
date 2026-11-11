# Dr. GRPO

## Meaning

Dr. GRPO, “GRPO Done Right,” is a specific revision of group-relative policy optimization. Its key changes concern two normalization factors: each response's own length and the prompt group's reward standard deviation. It is not a generic name for any improved GRPO implementation.

## Mechanism

[[group-relative-policy-optimization]] centers rewards within a prompt group. Dr. GRPO keeps that centering but omits division by the group's standard deviation. Its policy objective also replaces the response-dependent token denominator with a shared constant, such as a configured maximum response length. The [[proximal-policy-optimization]] minimum and ratio clipping still supply the surrogate form.

The [[token-sequence-loss-weighting]] mechanism explains the first change: averaging every response by its own length gives each token in a long response less weight. A fixed denominator avoids that particular length-dependent scaling, but the total magnitude and treatment of batch tokens still depend on the chosen constant. Removing within-group spread scaling also avoids automatically reweighting prompts by noisy inverse dispersion.

## One example

Take two responses of lengths 2 and 6, with group-centered advantages +.5 and -.5. At ratio one, suppose each token's unclipped contribution equals its response advantage. Response-wise averaging gives (+.5-.5)/2=0. With a shared denominator 8 and two-response averaging, the contribution is [2×.5+6×(-.5)]/(2×8)=-.125. This exposes a different weighting of long negative responses; it does not predict a future response-length trend for every model.

For two groups with the same centered difference but different reward spreads, division by each group's spread would further change their relative magnitudes. Omitting that step is a separate choice from the length denominator.

## Boundaries and check

The paper diagnoses normalization-induced biases under its formulation. “Unbiased” in that discussion does not establish unbiasedness of every finite-group baseline, clipped surrogate or stale-data update. Changing the denominator can change effective learning-rate scale. Record the constant, masks, group size and reward scale; compare each change independently on correctness, length by outcome, gradient magnitude and actual generated tokens. Does a fixed denominator make every response equally weighted? No: responses with more included tokens now contribute more summed terms.
