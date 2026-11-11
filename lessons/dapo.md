# DAPO

## Meaning

Decoupled Clip and Dynamic Sampling Policy Optimization (DAPO) is a coordinated language-model RL recipe, not just the larger clipping limit suggested by its name. It changes the objective, the batch-selection process, loss aggregation and treatment of long responses.

## Mechanism

First sample groups of responses per prompt and compute task rewards. [[dynamic-reward-group-sampling]] filters groups without relative reward contrast and replenishes the training batch. Center the accepted group rewards and apply the specified group scaling. In the clipped policy surrogate, [[asymmetric-policy-clipping]] permits a separate upper ratio width. Aggregate contributions across valid response tokens using [[token-sequence-loss-weighting]], rather than giving each complete response equal weight. [[overlong-response-reward-shaping]] supplies a graded cost near the generation limit and requires an explicit truncation policy.

The released core formulation is critic-free and omits an explicit reference-policy KL term. Those omissions are part of that recipe, not a proof that arbitrary rewards remain safe or that policy movement is bounded globally.

## One example

In an invented batch, prompt A yields rewards [0,0] and B yields [0,1]. A has no within-group contrast and is filtered; B is retained while more prompts are generated. B's centered rewards are [-.5,.5] before any dispersion scaling. If the successful response contains six valid tokens and the failed response two, token aggregation gives the successful trajectory three times as many terms, unlike equal-response averaging. A positive-advantage token with ratio 1.25 still has increasing incentive under an upper bound 1.28, while a symmetric 1.2 upper bound would already cap it. A near-limit length cost can change the rewards before these steps, so its interaction cannot be ignored.

## Boundaries and check

Replenishment consumes extra rollouts and changes the prompt population. Token weighting changes long-response influence. Wider clipping changes sensitivity to noisy positive rewards. A bundled benchmark improvement cannot identify which component caused it. Reproduce one change at a time, then their interactions, with equal total generated tokens and training resources. Log accepted/proposed counts, length distributions, ratio tails, reward reliability and held-out quality. Does equal accepted batch size mean equal training cost? No: rejected groups and truncated generations must also be counted.
