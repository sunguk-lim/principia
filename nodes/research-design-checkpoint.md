---
id: research-design-checkpoint
title: "Research Design Checkpoint"
summary: "A research design checkpoint reviews the question, hypotheses, data and analysis contract before execution can turn flawed assumptions into polished results."
type: concept
tags: [ml/agents]
prereqs: [agent-plan-artifact, hypothesis-testing, ml-task-specification]
sources: [https://www.cos.io/initiatives/prereg]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Research Design Checkpoint

## Meaning

A design checkpoint is a review boundary before expensive or consequential research execution. The agent proposes what will be learned and how; a reviewer or policy decides whether the plan is coherent enough to proceed. It is not approval of the future result and not a guarantee of a sound study.

## Mechanism

Use an [[agent-plan-artifact]] to record the question, target population, variables, comparison, admissible data, analysis, resource budget and failure criteria. [[ml-task-specification]] separates the operational objective from an easy proxy. [[hypothesis-testing]] makes clear why choosing a test after seeing a favorable result is different from assessing a prespecified claim.

Preregistration provides a public scientific example of fixing a plan before analysis and distinguishing planned from exploratory work. An internal checkpoint need not publish anything, and expert review and preregistration are not the same mechanism. Both can expose decisions before outcomes encourage rationalization. Permit justified revisions, record what changed and why, and identify which conclusions now need independent confirmation. Escalate unresolved methodology rather than using review as a ceremonial sign-off.

## One example

A fictional project proposes testing ten interventions and reporting whichever improves one of five outcomes. That creates fifty opportunities for a favorable result. Before execution, the reviewer asks for one primary contrast and outcome, a declared treatment of the other analyses and a confirmation dataset. If discovery is the actual goal, exploration remains legitimate, but its selected hypotheses are not retroactively labeled prespecified evidence. The checkpoint changes the evidential contract rather than forbidding useful exploration.

## Check your understanding

Should every cheap exploratory plot wait for an expert? No. Match the boundary to ambiguity and consequence, and distinguish exploration from confirmatory claims. Measure time spent reviewing, defects caught and downstream rework. A signed plan cannot compensate for invalid data or an untested identification assumption; inspect the completed work against the plan and preserve deviations transparently.

## Prerequisites

- [[agent-plan-artifact]]
- [[hypothesis-testing]]
- [[ml-task-specification]]

## Sources

- <https://www.cos.io/initiatives/prereg>
