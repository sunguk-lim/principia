# Cross Entropy versus Accuracy

## Meaning

Cross entropy measures the probability a model assigns to the correct label. Accuracy measures whether that label wins the final top-choice decision. One is sensitive to probability changes; the other changes only when the selected label changes.

## Mechanism

For a hard target with probability p, cross entropy is -ln(p). A larger target probability produces a smaller loss. Top-choice accuracy discards all probabilities except the identity of the winner, then records one for correct or zero for incorrect.

This explains a common apparent conflict: a model can improve the target's probability without moving it above the leading wrong option. Conversely, an aggregate loss improvement can hide deterioration in an important slice. Neither metric automatically describes the service's error costs.

## One example

Suppose A is correct. One model assigns A=0.20, B=0.50 and C=0.30. Another assigns A=0.35, B=0.40 and C=0.25. Both choose B, so both are wrong. Their losses differ: -ln(0.20) is about 1.609, while -ln(0.35) is about 1.050. Target probability improved even though accuracy did not move.

The example does not prove that the second model is generally better. It shows why a single decision score has lower resolution than the full probability assignment.

## Check your understanding

Does lower validation loss certify better performance on every downstream benchmark? **No.** Compare matched inputs, targets, weights and scoring rules; inspect paired outcomes and relevant domains. Per-token language-model loss also depends on tokenization and valid-token accounting. Across incompatible tokenizers, raw token averages are not directly comparable evidence of capability.
