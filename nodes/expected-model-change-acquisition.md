---
id: expected-model-change-acquisition
title: "Expected Model-Change Acquisition"
summary: "Expected model-change acquisition scores an unlabeled example by the predicted magnitude of the learning update its possible labels would induce, rather than by uncertainty alone."
type: concept
tags: [ml/training]
prereqs: [active-learning, gradient-descent, expectation, euclidean-distance]
sources: [https://raw.githubusercontent.com/webis-de/small-text/main/small_text/integrations/pytorch/query_strategies/strategies.py, https://burrsettles.com/pub/settles.activelearning.pdf]
status: explained
created: 2026-11-26
updated: 2026-11-26
---

# Expected Model-Change Acquisition

## Meaning

Expected model-change acquisition asks which label would be expected to move the current learner most. The label is not yet known, so the method considers possible labels weighted by the model's predictive probabilities. It is one policy inside [[active-learning]], not a guarantee of improved generalization.

## Mechanism

Let theta be the current parameter vector and x an unlabeled candidate. For possible label y, let p(y|x) be its predicted probability and g_y the gradient of that labeled example's loss. Under [[gradient-descent]] with learning rate eta, the hypothetical single-step update is minus eta times g_y. A gradient-length score uses [[expectation]] to compute E(x)=sum_y p(y|x) times ||g_y||, using [[euclidean-distance]] from the zero vector and an explicitly stated parameter subset. A fixed positive eta scales every score equally under these simplified assumptions.

Take the norm before averaging: a norm of the average gradient can cancel opposing updates and define a different policy. Expected gradient length is also different from expected reduction in evaluation error; a large parameter movement may be harmful. Optimizer state, clipping or adaptive scaling can make raw gradient length an imperfect proxy for the actual update.

The small-text implementation is primary evidence for class-probability-weighted hypothetical gradient scoring and layer-restricted variants. Norm choices differ across its variants; do not silently assume every implementation uses the same norm or parameter set.

## One example

For invented binary candidate A, probabilities are 0.75 and 0.25 and hypothetical gradient lengths are 2 and 6. Its expected length is 0.75×2+0.25×6=3. Candidate B has probabilities 0.5 and 0.5 and lengths 1 and 3, giving 2. This policy selects A although B has more balanced label uncertainty. The example assumes those lengths and does not infer them from class probabilities.

## Validation and boundaries

Compare random, entropy and model-change acquisition at matched total annotation and scoring cost. Backpropagating under many labels can be expensive; a restricted layer or label approximation changes the score and requires validation. Inspect outliers, feature scaling, label noise and representative held-out quality. A large update is a proposed mechanism, not the final success metric.

## Check your understanding

Can a label with low probability dominate the score? Yes, if its hypothetical update magnitude is sufficiently large.

## Prerequisites

- [[active-learning]]
- [[gradient-descent]]
- [[expectation]]
- [[euclidean-distance]]

## Sources

- <https://raw.githubusercontent.com/webis-de/small-text/main/small_text/integrations/pytorch/query_strategies/strategies.py>
- <https://burrsettles.com/pub/settles.activelearning.pdf>
