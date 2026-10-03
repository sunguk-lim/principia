---
id: naive-bayes-likelihood-estimation
title: Naive Bayes Likelihood Estimation
summary: Naive Bayes estimates class priors and feature likelihoods under conditional independence, then applies Bayes' rule to classify new observations.
type: concept
tags: [ml/evaluation]
prereqs: [bayes-theorem, conditional-probability]
sources: [https://scikit-learn.org/stable/modules/naive_bayes.html]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Naive Bayes Likelihood Estimation

## Summary

**Naive Bayes** is a generative classifier that models a class prior and the conditional likelihood of each feature given the class. “Naive” names its assumption that features are conditionally independent within each class.

## Grounded explanation

The model combines estimated terms using [[bayes-theorem]]: a class score is proportional to its prior times the product of its feature likelihoods. In practice, log scores avoid numerical underflow. Multinomial, Bernoulli, and Gaussian variants use different feature likelihood models; smoothing prevents zero counts from eliminating a class solely because a feature value was unseen.

This approach does have an estimation criterion even if it is not trained by minimizing a discriminative loss such as cross-entropy over a neural network. Its independence assumption can yield useful classification despite imperfect probabilities, so evaluate predictive quality and calibration separately. Compare against a majority-class baseline and a discriminative model on held-out data. Check feature leakage, class imbalance, and whether the assumed [[conditional-probability]] form matches the data type.

## Prerequisites

- [[bayes-theorem]]
- [[conditional-probability]]

## Sources

- [scikit-learn Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html): conditional-independence formulation and model families.
