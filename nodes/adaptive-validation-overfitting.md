---
id: adaptive-validation-overfitting
title: "Adaptive Validation Overfitting"
summary: "Adaptive validation overfitting occurs when repeated selection decisions exploit noise in a reused validation set, making its score optimistic for the chosen procedure."
type: concept
tags: [ml/evaluation]
prereqs: [cross-validation, variance]
sources: [https://www.jmlr.org/papers/v11/cawley10a.html, https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Adaptive Validation Overfitting

## Meaning

A validation set can influence a model even when its examples never enter gradient updates. Selecting architectures, prompts or training changes from its scores transmits information into the next choice. The resulting score measures both useful learning and adaptation to that particular measurement sample.

## Mechanism

Separate fitting parameters from selecting a procedure and estimating its final performance. [[cross-validation]] provides an inner selection loop and, when nested, an outer evaluation loop that assesses the complete selection procedure. An untouched final test is another option when selection can genuinely stop before its results are seen. Once its feedback drives another edit, it has joined the selection process.

Log every candidate, query and decision through [[measurement]]. Restricting queries or using new data can reduce exposure, but a fixed count of trials does not determine the amount of bias: candidate dependence, data size and score [[variance]] matter. Cawley and Talbot analyze overfitting of model-selection criteria, including criteria that are individually unbiased. Repeating more seeds on the same exposed validation examples does not remove this data-level dependence.

## One example

Three invented configurations have true population accuracy .80. On one finite validation set their observed accuracies are .78, .81 and .84. Selecting the third and reporting .84 estimates the selected maximum, not an independently measured .84-capability model. An independent test might return .80. If that .80 result triggers new tuning and repeated testing, calling the same set untouched becomes false. The example illustrates selection, not a promise that every selected score will fall on retesting.

## Check your understanding

Does nested evaluation prove deployment reliability? No. It estimates a procedure under its split and population assumptions; leakage, shift or an inappropriate metric can remain. Keep preprocessing and all selection inside the appropriate training boundary, preserve the final evaluation protocol and disclose how many rounds used its feedback. A smooth validation curve does not establish that this boundary was respected.

## Prerequisites

- [[cross-validation]]
- [[variance]]

## Sources

- <https://www.jmlr.org/papers/v11/cawley10a.html>
- <https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html>
