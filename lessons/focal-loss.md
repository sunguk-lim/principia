# Focal Loss

## Meaning

Focal loss reduces the weight of examples the classifier already predicts confidently. It was proposed to address many easy background examples in dense object detection, not as a guarantee for every imbalanced dataset.

## Mechanism

Let $p_t$ be the probability assigned to the correct class. Ordinary cross-entropy contributes $-\log p_t$. Focal loss multiplies this by $(1-p_t)^\gamma$ and optionally a class factor $\alpha_t$. A confident correct prediction has $p_t$ near one and receives little weight; a mistaken prediction remains influential. The class factor is separate from the confidence factor. Unlike plain [[class-weighted-loss]], this changes weight from example to example within a class.

This can concentrate learning on hard examples, but some hard examples are mislabeled or intrinsically ambiguous. It can also affect calibration. Compare with class weighting and hard-negative sampling at matched compute.

## One example

For a true class predicted with $p_t=0.9$ and $\gamma=2$, the focal factor is $0.01$. For $p_t=0.2$, it is $0.64$. The second example gets more relative emphasis, but that arithmetic alone does not show whether the model improves on the target task.

## Check your understanding

**Question:** Does focal loss automatically fix a rare-class alert flood? **Answer:** No. It changes training emphasis; deployed thresholds, base rates, calibration, and label quality still matter.
