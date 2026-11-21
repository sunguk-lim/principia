# Clustering-Based Data Curation

## Meaning

Clustering can organize an unlabeled pool for training-data selection. Groups can limit redundant dominant modes or guide sampling near trusted reference examples. A cluster is a property of a chosen representation and algorithm, not an automatic semantic class or quality label.

## Mechanism

Compute an [[embedding]] for each eligible example, define normalization and distance, and group the pool using [[k-means-clustering]] or another declared rule. Choose a selection policy: fixed per-group quotas, proportional quotas, representative examples, or expansion from groups touched by curated references. Keep eligibility, deduplication, licenses and benchmark exclusions separate from similarity. Record selected IDs, encoder/codebook versions and sampling seeds.

DINOv2 supplies a primary example of image-pool deduplication and retrieval-based curation, including cluster-guided expansion for small curated datasets. That design motivates the mechanism; it does not establish that arbitrary embeddings or equal cluster quotas yield a balanced population. Groups can split one common class into many regions and merge several rare classes into one.

## One example

An invented pool has groups of 9,000, 900 and 100 examples. Sampling 100 from each changes their representation from 90:9:1 to equal group counts. That may improve coverage of small groups but can amplify noisy or irrelevant regions and remove useful variation from the largest group. If the smallest group contains duplicated artifacts, equal quotas increase their influence rather than improve diversity.

## Boundaries and check your understanding

Use a [[dataset-ablation-study]] to compare random, proportional and cluster-based selection at equal retained sample and training budgets. Keep a held-out task set independent of curation queries; near-duplicate reference or evaluation examples can leak into training. Measure per-group retention, duplicate rate, source/domain coverage and downstream quality, including rare and shifted slices. Inspect stability under another encoder or cluster count. Lower clustering distortion measures grouping fit, not better training-data selection.

**Check:** Do equal group counts establish equal representation of real-world classes? No. The grouping need not correspond one-to-one with those classes, and class balance may not be the intended deployment objective.
