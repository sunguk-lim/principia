# Hard-Negative Mining

## Meaning

Hard-negative mining selects negative examples that the current model misclassifies or assigns high loss, so training spends more effort on its confusing cases.

## Mechanism

A fraud model may see thousands of easy legitimate transactions and a handful that resemble fraud. After scoring a candidate pool, the trainer keeps some high-loss legitimate cases alongside positive cases. Unlike [[class-weighted-loss]], this changes the sampled examples; unlike [[focal-loss]], it need not modify the mathematical loss for every example.

## One example

Train three fraud models with identical compute: random negatives, fixed class weighting, and a capped hard-negative pool. Compare precision at the investigator's review capacity and audit whether the mined pool contains mislabeled transactions.

## Check your understanding

**Question:** Why not train only on the hardest negatives? **Answer:** The hardest cases can include label mistakes or atypical noise; exclusive selection may distort the data distribution and hurt calibration or generalization.
