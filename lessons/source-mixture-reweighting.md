# Source Mixture Reweighting

## Meaning

Appending datasets makes their sizes determine the unweighted training mixture. Source mixture reweighting deliberately changes that influence. A source is a provenance-defined group such as a collection process or annotation-policy version, not necessarily a class label. Weighting can express a target population or a robust training objective; those are different reasons and need different validation.

## Mechanism

Let s identify a source. Let p_s be its fraction of the observed training data and q_s its desired mixture share; both sets of nonnegative fractions sum to one. Assume p_s is positive wherever q_s is positive. Let L_s be the mean [[loss-function]] value within source s. The unweighted mean is the sum of p_s times L_s. To optimize the desired mixture, the corresponding sum is q_s times L_s. Giving each example from source s weight w_s = q_s/p_s changes its expected contribution from p_s L_s to q_s L_s.

This identity uses a [[probability-distribution]] over sources and assumes the within-source examples represent what the chosen objective means. It is not a general correction for changed label semantics or arbitrary within-source shift. A missing source cannot be created by weighting. Large ratios amplify noisy examples and unstable estimates; clipping changes the intended objective and must be reported.

Alternatively, sample sources with probabilities q_s, then sample examples within the chosen source. This targets the same mean data loss under the stated assumptions, but finite batches, replacement, update order and optimizer dynamics can differ. Combining resampling with q_s/p_s weights can double-adjust the mix. Frameworks also differ in whether they normalize weighted losses by example count or weight sum; record that convention and its interaction with regularization.

## One example

A has 100 examples and B has 900, so p_A=.1 and p_B=.9. To target q_A=.4 and q_B=.6, use w_A=4 and w_B=2/3. Total weighted contributions are 100×4=400 and 900×2/3=600, producing 40% and 60% of the weight rather than 10% and 90%. These numbers define an objective, not proof that 40/60 is the correct production mix.

Keep source identities and annotation policies in [[dataset-lineage]]. Compare original proportions, proposed weights and matched-budget resampling on untouched target data, reporting [[evaluation-slices]], calibration and weight concentration. DoReMi is a distinct learned approach: a small proxy uses group-robust optimization to choose domain proportions for larger-model training. Its experimental results do not justify treating the highest-loss source, largest source or newest source as universally best.

## Check your understanding

**Question:** Can reweighting reconcile two sources that assign different meanings to the same label? **Answer:** Not by itself. Reconcile the task and annotation policy or explicitly model the difference before interpreting a mixture objective.
