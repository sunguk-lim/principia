---
id: cost-aware-active-learning
title: "Cost-Aware Active Learning"
summary: "Cost-aware active learning chooses label acquisitions under explicit annotation and selection costs rather than equating every requested label with equal expense."
type: concept
tags: [ml/training]
prereqs: [active-learning, expectation]
sources: [https://raw.githubusercontent.com/NUAA-AL/ALiPy/master/alipy/query_strategy/cost_sensitive.py, https://arxiv.org/html/1905.03677v1]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# Cost-Aware Active Learning

## Meaning

Cost-aware acquisition seeks useful model improvement within a real resource budget. Ordinary [[active-learning]] often compares label counts; this can be misleading when one example requires seconds and another requires expert review. Cost is part of selection, not only a number reported after the experiment.

## Mechanism

For candidate i, let g_i be an estimated benefit, c_i a positive estimated acquisition cost and B the remaining budget. A simple additive selection model chooses a subset S with sum of c_i over S no greater than B while maximizing sum of g_i over S. Benefit concerns an [[expectation]] under uncertain future labels and retraining, not a known outcome. Costs can include annotation, adjudication and candidate-specific compute; shared retraining overhead belongs in complete accounting rather than being silently charged repeatedly per item.

One heuristic sorts by g_i/c_i and accepts affordable candidates. This is not generally optimal for indivisible labels: a slightly better ratio can leave unused budget that prevents a better pair. Correlated examples also violate additive benefit. ALiPy provides cost-sensitive query strategies and a budgeted subset-selection implementation, demonstrating that explicit costs can enter the acquisition decision. Its hierarchical multilabel setting is not the definition of all cost-aware active learning.

## One example

Use a hypothetical budget of 10 units. Candidate A has value 9 and cost 6; B and C each have value 7 and cost 5. A's ratio is 1.5, above B and C at 1.4. Ratio-greedy takes A and has 4 units left, insufficient for either other item, yielding value 9. Taking B and C costs 10 and yields value 14 under the assumed additive model. The example disproves universal optimality of the ratio rule; it does not claim true learning gains are known or additive.

## Boundaries and validation

Record actual completion time and disagreement-resolution costs, not only planned prices. Expensive examples can also cover important rare cases; blindly minimizing cost can starve them. Compare policies at matched money, time and selection compute, using a representative held-out evaluation and critical-slice coverage. Refit cost estimates when annotators, task types or instructions change. Evaluate cost prediction error and budget overshoot separately from task quality.

**Check:** Is the policy with fewer acquired labels necessarily cheaper? No. Label difficulty and compute can reverse the total bill.

## Sources

- <https://raw.githubusercontent.com/NUAA-AL/ALiPy/master/alipy/query_strategy/cost_sensitive.py>
- <https://arxiv.org/html/1905.03677v1>
