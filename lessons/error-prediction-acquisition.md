# Error-Prediction Acquisition

## Meaning

Error-prediction acquisition asks a secondary model which unlabeled examples are likely to be difficult for the target. A binary wrong/right predictor and a numerical loss predictor have different targets; the concrete Learning Loss instance predicts loss. It uses that prediction to choose labels, instead of treating output entropy as the only acquisition signal. Predicted loss is not the unknown label and is not guaranteed future learning benefit.

## Mechanism

On labeled examples, compute the target prediction and its observed per-example loss. Train an auxiliary predictor to estimate or rank those losses from input features. At acquisition time, it scores unseen candidates without access to their labels. Select a bounded batch, request labels, update the target and refresh the predictor as the target changes.

The original Learning Loss method attaches a small jointly trained module to intermediate target-network features. This is more specific than using an arbitrary standalone cheap model. A small scoring head can still need an expensive target forward pass to obtain its features; count that work.

## One example

Four candidates A–D have predicted losses .8, .7, .2 and .1. With budget for two labels, the policy selects A and B. Their newly observed losses turn out to be .05 and .9. The predicted ordering was wrong. Those labeled examples provide corrective evidence, but the earlier scores should not be reported as measured errors.

If A and B are nearly identical, selecting both may also add little coverage. After retraining, yesterday's loss ranking can become stale because the target's mistakes have changed.

## Check your understanding

Is a hard example always useful to label? No. It may be ambiguous, corrupted or redundant. Compare random, uncertainty and learned-loss acquisition using downstream quality on an independent test set at equal annotation and compute cost. Separately measure loss-ranking quality and total feature-extraction cost. Vision-task results in the primary paper are evidence for its evaluated settings, not proof that a small proxy will replace all expensive language-model scoring.
