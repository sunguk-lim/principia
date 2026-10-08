# Advantage Baseline in Policy Optimization

## Meaning

An advantage compares a sample reward with a baseline: reward above expectation is reinforced; reward below it can be discouraged. The reference level, not the raw pass/fail label alone, shapes the update.

## Mechanism

For samples from the current policy, a baseline independent of the sampled action can center a policy-gradient estimate without changing its expectation. Group-relative methods estimate a baseline from peer attempts. Noisy rewards or groups with identical outcomes give weak signals; variance reduction is an empirical question.

## One example

An easy prompt yields nine successes in ten attempts. One more success contributes little relative information; the rare failure can be informative. On a hard prompt, a rare success may receive a stronger positive relative signal.

## Check your understanding

**Question:** Does subtracting any arbitrary baseline guarantee less gradient variance? **Answer:** No. The baseline must be well chosen, and its effect must be measured.
