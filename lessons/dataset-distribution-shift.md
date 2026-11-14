# Dataset Distribution Shift

## Meaning

Distribution shift means reference and target populations differ in their probabilities of inputs and targets. Their schemas can remain identical. Shift can occur between sources or between training and serving, not only across time. A detected difference is not by itself proof of reduced task quality.

## Mechanism

Let X denote inputs and Y their target. A [[probability-distribution]] assigns their joint probabilities. Factoring that joint into input frequency and the [[conditional-probability]] of Y given X separates a changed input mix from a changed target relationship. Special assumptions, such as a fixed relationship despite changed inputs, need evidence.

Unlabeled feature checks can reveal input differences but cannot generally establish an unchanged target relationship. Annotation-policy changes and instrumentation faults need separate diagnosis. Schema validation checks a different contract: matching types and allowed values do not imply matching distributions. Passing individual feature comparisons also does not prove equality of the full joint distribution.

## One example

A reference population contains 80% short requests and 20% long requests. The target contains 40% short and 60% long. A fixed classifier errs on 5% of short and 20% of long requests in both populations. Reference error is .8×.05+.2×.20=.08. Target error is .4×.05+.6×.20=.14. The mixture alone raises aggregate error from 8% to 14%, without changed within-group behavior.

Use [[evaluation-slices]] to report both error and population proportions. If the correct label for the same request changed because the instructions changed, reweighting the old groups alone cannot repair that semantic mismatch. Check independent target labels, provenance, missingness and uncertainty before choosing retraining, recollection, recalibration or weighting.

## Check your understanding

Does an unchanged schema establish that appended training data represents the same task population? No. Format, probability mix and target semantics are distinct. Diagnose the changed quantity and validate the proposed remedy on the intended target population.
