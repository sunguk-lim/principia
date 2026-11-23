---
id: pairwise-preference-model
title: "Pairwise Preference Model"
summary: "A pairwise preference model maps prompt-conditioned candidate score differences to comparison probabilities and fits them against observed choices without treating the score as objective truth."
type: concept
tags: [ml/evaluation]
prereqs: [binary-cross-entropy, model-calibration]
sources: [https://arxiv.org/html/2305.18290v3]
status: explained
created: 2026-11-24
updated: 2026-11-24
---

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

## Validation and check

Specify rater population, rubric, candidate-generation process and randomization of display order. Hold out prompts and important rater/task slices; measure ranking errors, agreement, calibration, position effects and contradictory choices. A scalar-score model imposes a structure on preferences that may not capture every context-dependent or cyclic choice. Model fit does not prove the structure is appropriate.

After optimizing a generator against the fitted score, gather fresh independent comparisons. The generator may exploit artifacts outside the reward model's training coverage. Separate learning a comparison proxy from demonstrating that optimization improves deployment outcomes.

**Check:** Can comparison data identify an absolute reward offset for one prompt? Not in this model; a common offset cancels.

## Prerequisites

- [[binary-cross-entropy]]
- [[model-calibration]]

## Sources

- <https://arxiv.org/html/2305.18290v3>
