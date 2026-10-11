---
id: synthetic-bug-training
title: Synthetic Bug Training for Coding Agents
summary: Synthetic repository bugs provide scalable, testable agent practice, but training must control generator shortcuts and evaluate on independent real issues.
type: concept
tags: [ml/training]
prereqs: [reward-hacking, temporal-data-leakage]
sources: [https://github.com/SWE-bench/SWE-smith, https://github.com/SWE-bench/SWE-bench]
status: explained
created: 2026-10-12
updated: 2026-10-12
---

# Synthetic Bug Training for Coding Agents

## Summary

A synthetic bug task starts with a working repository, changes it to introduce a failure, and asks a coding agent to repair the resulting behavior. A runnable environment and tests make feedback scalable. The central risk is that the agent learns **how the generator makes bugs** instead of how real defects are diagnosed.

## Grounded explanation

SWE-smith provides primary examples of repository environments, synthesized task instances, tests that detect introduced failures, and generated issue text. That pipeline creates verifiable training tasks, but its mutation operators, eligible test-covered code, and issue-writing process define a distribution. If a generated issue reveals the changed line, or all bugs are one-line operator flips, an agent can exploit those cues. This is a form of [[reward-hacking]]: synthetic reward rises while real issue resolution may not.

A real-issue benchmark such as SWE-bench supplies a distinct evaluation anchor. Separate repositories and time periods between training and evaluation to reduce [[temporal-data-leakage]] and near-duplicate exposure. Measure generator realism by bug category, files touched, localization distance, symptom wording, and available tests. No one synthetic-to-real mixing ratio is universally justified.

## Validation

Compare real-only, synthetic-only, and mixed training at matched model, compute, tool interface, and test budget. Hold out real issues; report resolution and failure types by repository and bug category. Require a candidate patch to turn designated failing tests green **and** preserve previously passing tests, while acknowledging that finite tests do not prove full correctness. Audit shortcuts by hiding or changing generator-specific cues and checking whether performance collapses. If synthetic reward improves without held-out real improvement, revise the generator or curriculum rather than claiming transfer.

## Prerequisites

- [[reward-hacking]]
- [[temporal-data-leakage]]

## Sources

- [SWE-smith project and paper](https://github.com/SWE-bench/SWE-smith)
- [SWE-bench project](https://github.com/SWE-bench/SWE-bench)
