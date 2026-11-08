---
id: research-agent-capability-evaluation
title: "Research-Agent Capability Evaluation"
summary: "Research-agent capability evaluation separates ideation, study design, implementation and realized outcomes while controlling how much expert guidance the agent receives."
type: concept
tags: [ml/evaluation]
prereqs: [task-underspecification, evaluation-oracle-availability, paired-benchmark-uncertainty]
sources: [https://arxiv.org/abs/2409.04109, https://www.anthropic.com/research/demystifying-evals-for-ai-agents]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Research-Agent Capability Evaluation

## Meaning

Executing an established analysis and designing a useful new study are different capabilities. Research-agent evaluation records which decisions were already supplied, which the agent made and which outcomes were actually checked. Proposal novelty and quality of completed research are separate axes, not interchangeable scores.

## Mechanism

Construct stage-specific tasks: reproduce a supplied method, choose an analysis under a broad goal, propose a study, and execute a selected proposal. Control tools, data, compute and human assistance. [[task-underspecification]] identifies open choices; [[evaluation-oracle-availability]] identifies how each choice and output can be assessed. Score methodological validity, reproducibility, feasibility and contribution separately. A detailed expert prompt is part of the tested system, not free evidence that the model generated the expert judgment.

Blind subjective reviews where possible and preserve per-task outcomes for [[paired-benchmark-uncertainty]]. Predefine idea-selection and execution budgets, include abandoned projects and distinguish missing outcomes from demonstrated failures. The primary research-idea study evaluates novelty and feasibility judgments and explicitly motivates an end-to-end execution study; proposal ratings alone do not establish realized scientific value.

## One example

Suppose agent A correctly reproduces 8 of 10 supplied analyses and agent B reproduces 6. On ten new design tasks, experts accept 3 of A's designs and 5 of B's. These invented counts reverse the ordering because the objectives differ. If A's three accepted proposals each receive two weeks of human repair while B's receive none, comparing final papers without that assistance ledger is also misleading. Track valid designs, implementation success and contribution with their own denominators.

## Check your understanding

Can a novel proposal certify an autonomous scientist? No. It can be infeasible, invalid or unhelpful after execution. Conversely, a replication is useful evidence about execution without proving ideation competence. Report the capability profile and intervention budget rather than extrapolating one benchmark score to every stage of research.

## Prerequisites

- [[task-underspecification]]
- [[evaluation-oracle-availability]]
- [[paired-benchmark-uncertainty]]

## Sources

- <https://arxiv.org/abs/2409.04109>
- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
