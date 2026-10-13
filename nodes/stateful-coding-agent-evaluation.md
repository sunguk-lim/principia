---
id: stateful-coding-agent-evaluation
title: Stateful Coding-Agent Evaluation
summary: Stateful coding-agent evaluation chains repository tasks so each task begins with the agent’s earlier committed changes, exposing cumulative regressions and maintenance costs.
type: concept
tags: [ml/agents]
prereqs: [execution-benchmark-validity, measurement]
sources: [https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Stateful Coding-Agent Evaluation

## Summary

Stateful coding-agent evaluation chains repository tasks so each task begins with the agent’s earlier committed changes, exposing cumulative regressions and maintenance costs.

## Grounded explanation

An isolated issue test asks whether a patch solves one problem from a prepared repository state. **Stateful coding-agent evaluation** asks whether a sequence of patches leaves a usable repository for the next task. Task $n+1$ starts from the accepted state after task $n$, including the agent's helpers, tests, and architectural choices. This tests a different property from one-task pass rate.

[[execution-benchmark-validity]] still applies: pin dependencies, task order, timeout, review policy, and test oracle. Record both task-local pass/fail and pass-to-pass regression results. Inspect changed tests so an agent cannot improve apparent pass rate by deleting or weakening assertions. Mutation testing can probe test strength, but equivalent mutants and changed coverage make a single score inconclusive. Track duplication, complexity, dependency growth, review effort, reverts, and later repair cost as trends rather than treating lines added as a quality score.

Compare multiple task sequences and a clean-start or human-maintained control with the same budget. Task difficulty, changing dependencies, and flaky tests can produce a declining curve without agent-caused degradation. Use [[measurement]] to report paired outcomes and uncertainty, then inspect concrete regressions before promoting or stopping an agent. SWE-bench documents a reproducible isolated-task evaluation; chaining tasks is a separate evaluation design, not a claim about its published scores.

## Prerequisites

- [[execution-benchmark-validity]]
- [[measurement]]

## Sources

- [https://www.swebench.com/SWE-bench/guides/evaluation/](https://www.swebench.com/SWE-bench/guides/evaluation/)
