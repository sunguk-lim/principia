# Probability Chain Rule

## Meaning

The probability chain rule computes the probability that several events all occur by multiplying probabilities conditioned on the earlier events. It is an identity, not an assumption that the events are independent.

## Mechanism

Let A, B and C be events, and P denote probability. By [[conditional-probability]], P(B|A)=P(A and B)/P(A), when P(A)>0. Rearranging gives P(A and B)=P(A)P(B|A). Apply the same identity to C and the joint event A and B:

$$P(A\cap B\cap C)=P(A)P(B\mid A)P(C\mid A\cap B).$$

Every conditioning event used in a ratio must have positive probability; a zero-probability earlier joint event makes the final joint event zero directly. Repeating the rearrangement extends the rule to any finite sequence. Independence permits replacing conditional factors with unconditional ones; the chain rule itself does not.

For next-token generation, each factor is conditioned on a particular preceding token sequence. Multiplying these factors gives the probability assigned to that exact sequence. The probability of any acceptable answer may instead require summing over many sequences. A dataset-wide token accuracy is an empirical average, not automatically any of these conditional factors.

## Worked example

A system passes an input check with probability 0.8. Given that pass, a tool selection is correct with probability 0.75. Given both successes, arguments are correct with probability 0.9. Complete success is 0.8×0.75×0.9=0.54. The second and third factors already include the relevant dependency; no independent-error assumption was needed.

If the same three numbers were only unconditional marginal success rates, 0.54 would not follow without additional dependence assumptions. Likewise, 0.99 raised to 300 is about 0.049 only under a model supplying those particular factors, not merely because an aggregate accuracy is 99%.

## Check your understanding

**Question:** Does a product of probabilities prove independence? **Answer:** No. Inspect what each factor is conditioned on. Conditional products are the general rule; marginal products need stronger assumptions.
