---
id: error-prediction-acquisition
title: "Error-Prediction Acquisition"
summary: "Error-prediction acquisition learns a proxy for target-model mistakes or loss and uses its fallible difficulty ranking to request labels."
type: concept
tags: [ml/training]
prereqs: [active-learning]
sources: [https://arxiv.org/html/1905.03677v1]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# Error-Prediction Acquisition

## Meaning

Error-prediction acquisition selects unlabeled examples using a learned proxy for target-model difficulty rather than directly using class entropy. A predictor may target whether a task output is wrong or the magnitude of its loss; those targets are not interchangeable. It is an [[active-learning]] acquisition mechanism: a secondary predictor estimates where the target model is likely to struggle, then human labels are requested for selected inputs. The loss estimate is a fallible ranking signal, not an observed error label.

## Mechanism

For a binary error predictor, the training target can be the observed wrong/right outcome under a fixed task rubric. For a loss predictor, it is the numerical task loss. Specify which quantity the score estimates: high loss is not automatically high error probability, and neither is guaranteed annotation benefit. The following primary-paper instance uses predicted loss.

For an already labeled input x with label y, the target model produces a prediction and an actual per-example loss l(x,y). An auxiliary model reads permitted features of x, including target-network features when designed that way, and predicts a score l_hat(x) without needing y at selection time. Train the predictor using labeled examples and the corresponding observed target losses. Rank unlabeled candidates by their predicted score, acquire a bounded batch, update the target and refresh the predictor as the target changes.

Yoo and Kweon's Learning Loss method attaches a small module to several target-network layers and jointly learns it to rank losses. An arbitrary cheap standalone model is a broader engineering alternative, not exactly their architecture. Features extracted by an expensive target still cost a forward pass; a small head alone does not remove that expense.

## One example

Suppose four unseen candidates A–D receive predicted losses .8, .7, .2 and .1. A two-label budget chooses A and B. After annotation their actual losses are .05 and .9: the ranker misjudged A and B's order. The new labels still help assess and update it, but the acquisition scores were never observed truth. If A and B are near-duplicates, selecting both may waste coverage despite their high scores.

The actual target loss can change after retraining. A predictor trained only on the initial model's mistakes can become stale even when the input distribution stays fixed.

## Boundaries and validation

Distinguish high predicted loss, true error and expected benefit from acquiring a label. Ambiguous or corrupted examples can stay difficult without being useful to learn. Evaluate ranking against newly observed losses and compare downstream learning curves with random, uncertainty and diversity-aware acquisition at equal full cost. Preserve an independent representative evaluation set; the actively chosen labels are not an unbiased quality sample. Include feature extraction, predictor training and selection in resource accounting. Primary experiments on vision tasks do not establish the same gains for frontier language models.

**Check:** Does a tiny loss head imply cheap pool scoring? No, not if obtaining its input still requires an expensive target-model pass.

## Sources

- <https://arxiv.org/html/1905.03677v1>
