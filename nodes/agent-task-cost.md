---
id: agent-task-cost
title: Agent Task Cost
summary: Agent task cost sums all trial resources over a declared task cohort and normalizes by attempted or successfully completed tasks rather than prompt length.
type: concept
tags: [ml/agents]
prereqs: [multi-turn-token-accounting, execution-benchmark-validity]
sources: [https://www.anthropic.com/research/demystifying-evals-for-ai-agents, https://platform.claude.com/docs/en/build-with-claude/prefix-caching]
status: explained
created: 2026-11-02
updated: 2026-11-02
---

# Agent Task Cost

## Meaning

Agent task cost measures the resources consumed in reaching a task outcome. A shorter model input is one local change, not evidence that a complete task became cheaper. State the cohort, what counts as an attempt, and the success criterion before computing the denominator.

## Mechanism

Use [[multi-turn-token-accounting]] for each model call, including summary generation, repairs and billed failures. Keep cache-read, cache-write, uncached-input and output categories disjoint and apply the actual model's rates. Add tool and execution charges in the same currency; avoid charging a shared resource twice. If a resource has no monetary conversion, report its unit separately rather than adding milliseconds to dollars.

Let C be total cost across all included trials, N the number of attempts and S the number of successful attempts under [[execution-benchmark-validity]]. Cost per attempt is C/N; cost per success is C/S when S is positive. The latter includes the cost of failures. With no successes, it is undefined, not zero. If a task has several retries, specify whether the unit is each trial or the task's entire bounded retry policy. Changing that policy changes the measured system.

## Worked example

On the same 100 tasks, system A spends $0.08 per attempt and resolves 80. Its total is $8, cost per attempt $0.08 and cost per success $8/80=$0.10. System B spends $0.05 per attempt plus $0.03 for summarization and extra recovery calls; it resolves 64. Its total is also $8, but cost per success is $8/64=$0.125. The cheaper visible main call did not improve task economics.

These are invented accounting values, not measured product performance. If B instead completed more tasks or required fewer later calls, the result could reverse.

## Boundaries and validation

Report success rate, attempt cost and success-normalized cost together, with latency and resource tails. Compare the same task mix and budgets; changed difficulty or success grading can move the ratio without improving execution. Reconcile per-call traces to billing and preserve which trial incurred each fee. Cache invalidation, longer trajectories and extra verification are hypotheses to test, not guaranteed consequences of compression. A longer successful run may be preferable to a cheap incorrect one.

## Prerequisites

- [[multi-turn-token-accounting]]
- [[execution-benchmark-validity]]

## Sources

- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
- <https://platform.claude.com/docs/en/build-with-claude/prefix-caching>
