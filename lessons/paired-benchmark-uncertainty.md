# Paired Benchmark Uncertainty

## Meaning

Paired benchmark uncertainty concerns the difference between systems evaluated on the same cases. The identities of changed answers matter, not only the two headline accuracies.

## Mechanism

For each item, subtract model A's zero/one correctness from model B's. A shared success or failure contributes zero; a new success contributes one, and a regression minus one. Average those differences to obtain the accuracy change. Their variability depends on the joint outcomes.

A paired bootstrap samples item indices and applies each sampled index to both systems. It preserves the pairing. If items share a source document, template or other dependency, choose an appropriate grouped sampling unit. Prompt variation is another dimension that should be measured explicitly.

## One example

A answers 60 of 100 items correctly and B answers 62. Ten cases improve and eight regress, yielding a two-point gain with 18 disagreements. Another comparison with three improvements and one regression has the same two-point gain but only four disagreements. The uncertainty of their paired differences is not the same.

For a single accuracy near 60% on 500 independent binary cases, sqrt(0.6 times 0.4 divided by 500) is about 0.0219. That describes a standalone score's approximate standard error under those assumptions, not the uncertainty of the paired difference.

## Check your understanding

Can two separate accuracy error bars replace paired analysis? **No.** Retain item-level results, dependencies and prompt conditions. Predeclare comparisons, report effect size and intervals, and account for multiple testing. A benchmark interval also does not repair contamination or an unrepresentative dataset.
