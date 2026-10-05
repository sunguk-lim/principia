# Conformal Prediction Set

## Meaning

A **conformal prediction set** wraps a fixed predictive model with an uncertainty set. In split conformal prediction, a held-out calibration set determines how large that set must be to achieve a chosen *marginal* coverage target under exchangeability. A 90% coverage target describes repeated future examples from the same data-generating process; it does not mean that one patient's diagnosis has a 90% conditional probability of being inside the returned set.

## Mechanism

Train the base model without using the calibration examples. Define a nonconformity score that is small when the true outcome fits well. Score the calibration examples, sort those scores, and choose the finite-sample adjusted upper [[quantile]] for error level $\alpha$. For a new input, include candidate outcomes whose scores do not exceed that threshold. Exchangeability gives a rank argument: the new true-outcome score is no more likely than a calibration score to rank beyond the threshold. This is the source of the marginal coverage statement, independent of the model's accuracy.

For classification, the output may be a set of plausible labels. A weak classifier can still achieve coverage by returning large, unhelpful sets. Measure both empirical coverage and set size on held-out data; stratify by clinically relevant groups because marginal coverage can hide poor subgroup or individual conditional coverage. [[model-calibration]] of numeric probabilities is a different question: a conformal set can cover at its target rate without turning the model score into an individualized disease probability.

## One example

A classifier returns a set of diagnoses calibrated to cover the true label on roughly 90% of future exchangeable examples. Some individual cases may have much lower conditional coverage.

## Check your understanding

**Question:** Does a 90% coverage set mean this patient has a 90% disease probability?

**Answer:** No. The guarantee is marginal over future examples, not an individualized posterior.
