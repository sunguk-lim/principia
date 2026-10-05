# Tabular Model Comparison

## Meaning

“Boosting beats neural networks on structured data” is not a portable result. **Tabular model comparison** is the controlled procedure for deciding which model family works for a particular dataset and deployment budget. The objective, data split, feature types, tuning budget, and metric must be matched before an observed gap means anything.

## Mechanism

Begin with a simple linear or tree baseline, a boosted-tree model, and a relevant neural baseline. [[gradient-boosting-objective]] explains one family but not the comparison itself. Use the same training, validation, and test populations, with [[cross-validation]] or a temporal split appropriate to the data-generating process. Keep test data out of preprocessing and hyperparameter selection. Allocate a documented search budget per family and report both the best quality and the resources required to reach it.

Tabular data often mixes numerical and categorical fields, missingness, skewed targets, and small sample sizes. Preprocessing choices can advantage one model: a tree may handle threshold-like patterns naturally, while a neural model may benefit from scale, embeddings, or multimodal covariates. Dataset properties, not a model label, govern the result. Grinsztajn and colleagues benchmarked many medium-sized datasets and found strong tree-based baselines in their setting; that finding motivates a baseline, not a universal winner.

## One example

Compare a boosted tree and a neural model on the same time-based holdout and search budget. Report quality, calibration, latency, and tuning cost.

## Check your understanding

**Question:** Why is an unmatched leaderboard comparison weak evidence?

**Answer:** Differences in splits, preprocessing, tuning, or metric can explain the apparent model gap.
