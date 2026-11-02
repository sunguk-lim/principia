# Binary Cross-Entropy

## Meaning

Binary cross-entropy evaluates a predicted probability for a yes/no outcome. It rewards assigning probability to the label that actually occurred, rather than merely choosing the correct side of a classification threshold.

## Mechanism

Write y for the observed label, either zero or one, and p for the predicted probability of label one. If y is one, loss is minus the natural logarithm of p. If y is zero, loss is minus the natural logarithm of one minus p. The combined expression is -[y ln p + (1-y) ln(1-p)]. It is the negative log-likelihood of that binary observation.

Average over examples when each should count equally. For a weighted dataset, specify the weights and whether the result is a sum or a weighted mean. Training penalties and reported values depend on this normalization.

The logarithm makes confidently wrong probabilities expensive. In an ideal population where the event occurs with probability r, expected binary log loss is minimized by predicting r. This population property motivates probability estimation but does not promise that a fitted model is calibrated on new traffic.

## One example

For labels [1,0] and positive-class probabilities [0.8,0.3], the probabilities assigned to observed labels are 0.8 and 0.7. Their losses are approximately 0.223 and 0.357; mean loss is 0.290. Predictions [0.6,0.4] have mean loss 0.511. Both systems classify both examples correctly at threshold 0.5, but their log losses differ.

## Check your understanding

Is a correct label enough to compute binary cross-entropy? **No.** You need the probability assigned to the observed label. Verify which label a returned probability represents, and evaluate calibration and decision costs separately. Class weighting, clipping and aggregation also affect interpretation; a lower training value is not proof of better deployed decisions.
