# Selection Rate versus Evaluator Validity

## Meaning

An acceptance rate is the fraction of submitted items a judge admits. It measures selectivity under the submitted population and threshold. It does not establish that accepted items are correct, useful or scientifically valid. An arbitrary selector can be highly selective.

## Mechanism

Choose the target property and obtain labels or checks independent of the selection loop. Build a [[confusion-matrix]] of admitted/rejected items against valid/invalid outcomes. With valid work as positive, [[precision-recall]] distinguishes accepted-item validity from retention of valid work. Also report false acceptance among invalid submissions, uncertainty and the population used to calculate each rate.

A lower acceptance threshold in the numerical-score sense may admit more items; a stricter rule may admit fewer. Either can still rely on the wrong signal. Reviewing only accepted items cannot measure missed valid work. Review a representative sample of rejected items too, preserving selection probabilities when estimating population rates. Shared model-generated references can undermine independence even if reviewers carry different names.

## One example

In an invented batch of 100 submissions, 20 are valid. A judge admits 20 items: 5 valid and 15 invalid. Acceptance is 20/100=20%, but accepted-item validity is 5/20=25% and valid-item recall is 5/20=25%. A second judge admits 40 items including 18 valid ones: it is less selective yet has higher accepted-item validity, 18/40=45%, and recall, 18/20=90%. Neither result proves generalization beyond this labeled batch.

## Boundaries and check

Human agreement is evidence about agreement, not proof that the humans know the truth. Combine expert adjudication with executable or physical checks where applicable. Revalidate when submissions adapt to the judge. A conference-like acceptance rate is not a substitute for validating the actual evaluator.


## Check your understanding

Does admitting only one in five items establish high accepted-item quality? No; the judge can select the wrong fifth.
