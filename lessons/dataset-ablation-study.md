# Dataset Ablation Study

## Meaning

A dataset ablation changes part of the training data and observes what changes in the resulting model. Removing a source, restoring it, or varying its share can reveal whether a reported gain depends on that component. The answer is conditional on the model, data mix, training procedure and evaluation, not an intrinsic quality score for a dataset.

## Mechanism

Declare the question before choosing the intervention. To ask whether adding source B helps an existing source A, compare A-only, B-only and A-plus-B using immutable versions from [[dataset-lineage]]. Keep the model family, initialization policy, optimizer configuration and evaluation protocol fixed. Fit each trial's learned preprocessing only on its training partition. Use a development set for choices and an independent final test set for the resulting claim.

Training exposure is a separate control. With fixed epochs, a larger mixture gets more example presentations and often more updates. With fixed updates, examples in the larger mixture may be seen less often. State which resource is matched: update count, tokens, unique examples or elapsed compute. No one control holds all the others fixed. A source-removal result can reflect changed volume, class mix, ordering, duplicates or label semantics; add matched-size subsamples and mixture sweeps when those alternatives matter.

Keep evaluation examples and scoring fixed across paired trials, use several declared training seeds, and report the spread of paired differences with [[measurement]]. Evaluate [[evaluation-slices]] so a large easy group cannot hide harm elsewhere. Do not repeatedly choose a mixture using the final holdout and then describe that same score as independent evidence.

## One example

A target test set has 200 short and 100 long requests. A-only makes 10 and 20 errors: 30/300 = 10%. A-plus-B makes 8 and 30: 38/300, about 12.7%. Short-request error improves from 5% to 4%, while long-request error worsens from 20% to 30%. An aggregate regression is real for this target mix, but it does not prove that every B example is mislabeled.

Now compare a matched-size A-plus-B sample with A-only under the same update budget, and repeat across seeds. If the effect disappears, changed exposure or sample composition is a lead. If it persists, inspect source provenance and disagreement cases before prescribing cleaning or reweighting. The counts here illustrate the diagnostic protocol, not a measured experiment.

## Check your understanding

**Question:** Does a lower combined-data score identify label noise as the cause? **Answer:** No. The ablation localizes dependence on a data intervention; controls and follow-up audits must distinguish competing mechanisms.
