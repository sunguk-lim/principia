# Bayesian Optimization

## Meaning

Bayesian optimization chooses which expensive experiment to run next. It is helpful when a score such as validation accuracy takes substantial time to measure and only a limited trial budget is available.

## Mechanism

After several completed trials, a probabilistic surrogate estimates scores for untested settings and uncertainty about those estimates. An acquisition rule uses both to select a candidate. The real experiment is then run, the observation is added, and the surrogate is updated. The estimated distribution is conditional on the observed data, an application of [[conditional-probability]].

This is not magic extrapolation. It searches only the declared domain, and a poor surrogate can steer trials badly. It can handle discrete choices with an appropriate model; it is not restricted to continuous parameters.

## One example

Training one model takes four hours. Instead of trying a full grid of learning rates and regularization values, run a small initial set, fit a surrogate, and choose the next pair based on likely improvement and uncertainty. Compare the best validation score after the same 40-hour budget with random search across multiple seeds.

## Check your understanding

**Question:** What is the role of the acquisition rule? **Answer:** It ranks possible next experiments using the surrogate's predicted value and uncertainty.
