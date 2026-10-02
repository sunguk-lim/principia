---
id: code-generation-quality-reward
title: Code-Generation Quality Reward
summary: A code-generation quality reward evaluates functional correctness separately from measured non-functional properties and fallible human or learned judgments.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [reward-hacking, execution-benchmark-validity, measurement]
sources: [https://arxiv.org/abs/2203.02155, https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Code-Generation Quality Reward

## Summary

A generated program can pass tests and still be slow, insecure, wasteful, or hard to maintain. A **code-generation quality reward** makes these outcomes separate measurements rather than assuming that test pass rate is a complete proxy for useful code.

## Grounded explanation

A task's executable tests supply evidence about behavior on tested inputs, subject to [[execution-benchmark-validity]]. They do not certify runtime, memory, security, maintainability, or correctness on untested inputs. Record these dimensions separately before combining them. For example, a policy may receive a resource-use bonus only after it passes a pinned functional test suite. This correctness gate prevents a large style score from directly compensating for failing tests, but it cannot repair weak tests or capture every valid implementation.

Measure properties where possible: benchmark latency under fixed hardware and inputs, cap memory, and run targeted static and dynamic security checks. Use blinded expert ratings for subjective readability, with a rubric and agreement analysis. A learned judge may approximate those ratings, but optimization can exploit its blind spots; [[reward-hacking]] predicts that the judge's score may rise while human quality falls. Comments are neither automatically good nor bad: penalizing comment volume may suppress useful explanations, while rewarding it can produce filler.

Compare a functional-only baseline, separate constrained optimization, and a gated composite reward on held-out tasks. Report pass rate, per-property distributions, trade-off frontiers, human judgments, and regressions by task type. Audit failures and refresh the judge independently of the policy. The relative weights and any claimed improvement are empirical choices, not consequences of the reward formula.

## Prerequisites

- [[reward-hacking]]
- [[execution-benchmark-validity]]
- [[measurement]]

## Sources

- [InstructGPT paper](https://arxiv.org/abs/2203.02155): reward-model optimization and held-out human evaluation.
- [SWE-bench evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/): executable coding evaluation and its harness boundary.
