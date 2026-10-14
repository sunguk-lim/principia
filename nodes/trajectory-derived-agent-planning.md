---
id: trajectory-derived-agent-planning
title: Trajectory-Derived Agent Planning
summary: Trajectory-derived agent planning trains a planner from recorded actions by labeling only the information available at each planning decision, including later replanning decisions rather than hindsight outcomes.
type: concept
tags: [ml/agents]
prereqs: [agent-plan-artifact, temporal-data-leakage, agent-workflow-graph]
sources: [https://scikit-learn.org/stable/common_pitfalls.html#data-leakage, https://docs.langchain.com/oss/python/langgraph/graph-api]
status: explained
created: 2026-10-15
updated: 2026-10-15
---

# Trajectory-Derived Agent Planning

## Summary

A completed agent trace contains actions, observations, and eventual outcomes, but not necessarily a plan that existed before the work began. A training pipeline may *derive* plan labels from that trace. The label is valid only if it could have been written from information available at the corresponding decision point; otherwise it teaches a planner to anticipate discoveries it has not made.

## Grounded explanation

Represent each trace as ordered tuples of state, action, and resulting observation. At time $t$, construct a training input from the original task and observations through $t$, then ask for an [[agent-plan-artifact]] describing intended next steps. The labeler must not see later observations or final results when it writes that plan. This is the same availability-time constraint as [[temporal-data-leakage]], applied to action labels rather than ordinary prediction features. A plan can specify “check compatible suppliers,” but cannot name a supplier discovered only after that check.

Keep planning and execution supervision distinct. A planner learns `available state → proposed steps`; an executor learns `current state + approved step → bounded action`. One successful trace can yield several examples when a failed action or new observation requires a revised plan. Record the triggering observation, previous plan, revised plan, and whether the revision was actually executable. If a dataset retains only successes, it may discard the recovery cases needed for long tasks. Conversely, keeping every failed trace without labeling failure can teach unproductive behavior; stratify and evaluate both.

An [[agent-workflow-graph]] can expose these decision boundaries during data collection. Compare a causal-label planner with direct execution and a hindsight-labeled planner on held-out tasks. Measure unavailable-fact leakage, plan feasibility, executor success, replanning after changed evidence, and cost. Re-executing a generated plan is a useful check, but it can select for the specific executor and environment used in that test. Use independent tasks and repeated runs; do not infer deployment success from polished offline labels.

## Prerequisites

- [[agent-plan-artifact]]
- [[temporal-data-leakage]]
- [[agent-workflow-graph]]

## Sources

- [scikit-learn, data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage): the general rule that unavailable information must not influence training or evaluation inputs.
- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api): explicit state, node updates, and conditional transitions that can expose planning and replanning boundaries.
