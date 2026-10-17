# Selective Classification

## Meaning

**Goal:** distinguish error among accepted predictions from the amount of work a system agrees to handle.

A selective classifier may return a prediction or reject the input. Rejection can mean human review, a second model, or no automated decision. It is not automatically a correct answer. The predictor and rejection policy must be evaluated as a pair.

## Mechanism

Let $g(X)=1$ mean that input $X$ is accepted, and let $f(X)$ be the predicted label. Coverage is the fraction accepted. Selective risk is the fraction wrong *inside that accepted subset*. This is a [[conditional-probability]] statement, not the error rate across all inputs.

A threshold on a model score is one possible rejection rule. [[model-calibration]] helps assess score meaning, but average calibration does not choose a safe operating threshold or establish reliability for every class. Fit the rule on representative labeled selection data, then evaluate it on separate cases. Report accepted counts, risk, coverage, and uncertainty together.

## One example

On 1,000 labeled cases, the full classifier makes 100 errors. A selector accepts 600 cases, of which 12 are wrong. Coverage is 60%; selective risk is $12/600=2\%$. The remaining 400 cases have not disappeared: their review cost and final outcomes belong in the system evaluation. A selector accepting no cases has zero coverage and an undefined conditional error, not a demonstrated zero-risk service.

## Check your understanding

Does raising a score threshold guarantee lower measured selective risk?

**Answer:** no. Coverage cannot increase, but finite-sample error rates can fluctuate. Validate the actual operating point and recheck it after changes to classes, model, or traffic. Never transfer a measured risk guarantee without checking its assumptions.

Reference: [Selective Classification for Deep Neural Networks](https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html).
