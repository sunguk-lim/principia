---
id: feasibility-aware-triage
title: "Feasibility-Aware Triage"
summary: "Feasibility-aware triage orders corrective actions by achievable risk reduction under explicit time, resource and dependency constraints without suppressing mandatory blockers."
type: concept
tags: [ml/agents]
prereqs: [diagnosis-prescription-separation, agent-plan-artifact]
sources: [https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/]
status: explained
created: 2026-11-13
updated: 2026-11-13
---

# Feasibility-Aware Triage

## Meaning

Triage chooses which corrective actions to perform under limited resources. It is not a new definition of whether a finding is true. Feasibility includes elapsed time, available expertise, permissions and dependencies, not just how encouraging a suggestion sounds.

## Mechanism

Start with the findings preserved by [[diagnosis-prescription-separation]]. For each proposed action, record required inputs, estimated effort, uncertainty, expected benefit and completion evidence. Use an [[agent-plan-artifact]] to expose dependencies. Exclude infeasible actions from the immediate plan, but retain the underlying defects and follow-up work. A mandatory release blocker is a constraint, not a low-priority task that can be compensated for by many cosmetic fixes.

A severity-times-fixability product is only a heuristic: ordinal severity labels are not calibrated numerical utilities. If quantitative benefit estimates exist, compare feasible portfolios rather than sorting each action independently. Shared setup and prerequisites can make two individually cheap actions jointly expensive, or one large action enable several later repairs.

## One example

Suppose an invented team has sixty minutes. Action A takes forty minutes and removes a high-risk claim; B takes thirty minutes and corrects a figure; C takes fifteen minutes and fixes a misleading unit label. A and B do not fit together. A and C take fifty-five minutes, leaving five for verification. If A is a mandatory blocker, the plan cannot replace it with B plus C merely because two completed tickets look better. If A's estimate grows to ninety minutes, withhold the claim instead of hiding the defect.

## Boundaries and check

Estimates are uncertain; reserve verification time and replan when evidence changes. Test deadlines, missing authority, prerequisite failures and underestimated effort. Measure useful verified risk reduction and missed blockers, not ticket count. Domain owners must define what is mandatory and how costs or harms are compared.

## Prerequisites

- [[diagnosis-prescription-separation]]
- [[agent-plan-artifact]]

## Sources

- <https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/>
