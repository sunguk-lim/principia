# Evaluation Slices

## Meaning

An evaluation slice is a documented subset of examples selected by a property relevant to service behavior. Slices can expose an important weakness even when the overall score improves. They do not create new ground truth, and their membership rule must not change between compared systems.

## Mechanism

Define a membership rule before comparing predictions: for instance human-annotated negation scope, language, input length or customer environment. Use the same labeled examples and metric within each slice. A [[confusion-matrix]] separates false alarms from missed cases; [[conditional-probability]] expresses error given membership. Slices may overlap and need not partition the dataset, so their counts cannot always be summed. Report denominator and label mix beside each score. Choosing slices after looking at failures is useful discovery, but requires confirmation on fresh held-out examples rather than treating a selected surprise as an unbiased test.

## One example

Suppose 100 of 1,000 labeled cases contain negation. A baseline makes 30 errors on those 100 and 45 on the other 900: total error is 75/1,000=7.5%. A replacement makes 40 and 20 respectively: total error improves to 6%, while negation error worsens from 30% to 40%. The aggregate is not wrong; it answers a different population question. If negation examples were artificially oversampled in a test suite, use the real traffic proportions for a deployment aggregate and still show slice results. Include uncertainty, paired per-example changes and important intersections. A broad slice can hide a rarer subgroup; tiny slices cannot support precise conclusions. Decide fixes by error cost and prevalence, not merely the largest percentage.

## Loss slices

Slicing also applies to probability-based loss. With 80% code and 20% reasoning tokens, losses 1.0 and 2.0 average to 1.2. New losses 0.8 and 2.4 average to 1.12: aggregate loss improves while reasoning gets worse. Hold the mix, valid-token accounting and tokenizer-compatible units fixed. Report domain counts and task outcomes; lower aggregate loss alone does not certify domain capability.

## Check your understanding

Can improving aggregate accuracy certify improvement on every slice? No. A weighted aggregate can improve while an operationally important subset deteriorates.
