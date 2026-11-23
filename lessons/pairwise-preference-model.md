# Pairwise Preference Model

## Meaning

Pairwise preference modeling learns which of two candidates a population of raters tends to choose under a stated task. It can supply a ranking score or a learned reward. A preference is evidence about a comparison protocol, not a declaration that one response is universally correct.

## Mechanism

Let x denote a prompt, a and b two responses, and r(x,a), r(x,b) real-valued scores. The Bradley–Terry form assigns the probability that a is preferred as

$$P(a\succ b\mid x)=\sigma(r(x,a)-r(x,b)),\qquad \sigma(z)=1/(1+e^{-z}).$$

Here e is the exponential base and sigma maps a real score difference into (0,1). Fit observed binary choices with [[binary-cross-entropy]]. A preferred-a label contributes minus the logarithm of the displayed probability. Ties, abstentions and multiway rankings need an explicit extended observation model; silently forcing them into strict binary choices changes the data contract.

Adding the same prompt-specific constant to both scores changes neither their difference nor the comparison probability. Absolute score level is therefore not identified by these comparisons. Fit and evaluate a declared convention rather than interpreting an arbitrary score of seven as seven units of human value.

## One example

Take r(x,a)=2 and r(x,b)=1. Their difference is one, so P(a preferred)=1/(1+exp(-1)), about 0.731. A rater choosing a yields loss -ln(0.731), about 0.313. A rater choosing b instead yields -ln(0.269), about 1.313. Scores 12 and 11 predict the identical comparison; both increased by ten but the gap stayed one.

The result is a model prediction for this labeled comparison, not a calibrated probability of factual correctness. [[model-calibration]] checks predicted preference frequencies against independent observed choices. A response can win on style while losing on truth or task completion.

## Check your understanding

Can comparison data identify an absolute reward offset for one prompt? Not in this model; a common offset cancels.
