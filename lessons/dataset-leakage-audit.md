# Dataset Leakage Audit

## Meaning

A leakage audit tests the information boundary behind a generalization claim. Test examples should represent the conditions under which the system will be used, without giving model development information that the evaluation protocol forbids. Duplicate rows are one possible path across that boundary; preprocessing, repeated entities and repeated model selection are others.

## Mechanism

First state the unit that must be unseen: a row, document family, person, device, organization or future interval. Two rows from the same person can be legitimate when predicting more observations for known people, yet invalid evidence for performance on unseen people. Exact content hashes catch identical representations, not every related example. Preserve source and version information in [[dataset-lineage]], inspect near-duplicate candidates, and choose groups that reflect the intended independence boundary.

Assign each related group wholly to one side of a split when that claim requires it. GroupShuffleSplit provides within-split group separation for supplied group IDs; it does not discover hidden relatedness, and separate random splits can reuse test groups. A false group assignment therefore survives a correct splitting implementation. A chronological boundary addresses temporal data leakage but does not automatically remove copied examples across dates.

Trace learned transformations too. Scaling, feature selection, imputation and threshold selection must be fitted within the permitted training or development data. A training-only model can still leak if its selected features were chosen using the full dataset. Refit the entire pipeline inside each fold; applying a fixed transform to held-out inputs is different from learning that transform from them.

## One example

Suppose 120 records come from 40 people, with three records per person. A row split can place two records of person P in training and the third in test. A model might exploit a stable identifier-like pattern rather than generalize to a new person. A group split could train on 30 people, or 90 records, and test on the remaining 10 people, or 30 records. This enforces the known-person boundary for that split, not independence from all other hidden relations.

Measure overlap before and after grouping and compare performance on the same declared target population with [[measurement]]. If the stricter score falls, distinguish removed information access from changed test difficulty and sample size. Inspect exact duplicates, near-duplicate recall, group sizes, timing and fitted-transform provenance. Overlap is a threat to a claim; it is not by itself proof of memorization or a universal reason to discard a source.

## Check your understanding

**Question:** Is deduplicating exact rows enough? **Answer:** No. Related entities, transformed copies, future information and full-data preprocessing can still cross the evaluation boundary.
