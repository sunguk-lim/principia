---
id: evaluation-oracle-availability
title: "Evaluation Oracle Availability"
summary: "Evaluation oracle availability describes which independent signals can distinguish acceptable outcomes from plausible but incorrect ones, with explicit coverage and cost limits."
type: concept
tags: [ml/evaluation]
prereqs: [execution-benchmark-validity, agent-verification-loop]
sources: [https://www.anthropic.com/research/demystifying-evals-for-ai-agents, https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Evaluation Oracle Availability

## Meaning

An evaluation oracle is a source of evidence used to decide whether an outcome satisfies a contract. A reference answer, executable assertion, physical measurement and expert rubric are different oracles. Availability concerns what can actually be checked at the decision point, not whether a task has one uniquely worded answer.

## Mechanism

For each criterion, identify its evidence, independence from the candidate, failure coverage, cost and uncertainty. [[execution-benchmark-validity]] explains why a test harness can be an unreliable instrument even when it returns a crisp Boolean. An [[agent-verification-loop]] uses such evidence to accept, repair, escalate or stop; it cannot make missing evidence appear by asking the same model to be confident.

Combine complementary signals when no complete oracle is cheap. Invariants check necessary properties; controlled cases with known answers test parts of a method; expert assessment can judge an open-ended design. Multiple checks derived from the same mistaken reference are correlated evidence, not independent confirmation. Original research lacks a known final discovery, but still admits tests of analysis, assumptions and reproducibility.

## One example

A fictional agent migrates 200 records. A row-count check passes, but every price is doubled. A sum invariant detects that error, yet would miss swapping two customers' values. A per-ID comparison detects the swap. All three signals have different coverage: passing the count is not equivalent to checking the migration. If expected per-ID values are unavailable, report that limit and validate sampled records independently rather than inventing an exact correctness score.

## Check your understanding

Is another language model automatically an independent oracle? No. Shared training, prompts or reasoning shortcuts can reproduce the same mistake. Calibrate rubrics against reviewed cases and separate grader uncertainty from candidate quality. A missing reference should change the evaluation design, not license the assertion that correctness is either established or impossible to investigate.

## Prerequisites

- [[execution-benchmark-validity]]
- [[agent-verification-loop]]

## Sources

- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
- <https://www.swebench.com/SWE-bench/guides/evaluation/>
