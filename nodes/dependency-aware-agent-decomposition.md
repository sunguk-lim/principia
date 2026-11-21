---
id: dependency-aware-agent-decomposition
title: "Dependency-Aware Agent Decomposition"
summary: "Dependency-aware agent decomposition chooses parallel work from separable inputs and effects while retaining an explicit owner for state-dependent transitions."
type: concept
tags: [ml/agents]
prereqs: [multi-agent-orchestration, agent-workflow-graph, graph]
sources: ["https://www.anthropic.com/engineering/multi-agent-research-system", "https://docs.langchain.com/oss/python/langgraph/workflows-agents"]
status: explained
created: 2026-11-22
updated: 2026-11-22
---

# Dependency-Aware Agent Decomposition

## Meaning

More workers help only when useful work can actually be separated. Dependency-aware decomposition identifies which subproblems can proceed from an agreed input snapshot and which require another step's accepted result. A domain label such as “research” or “planning” is not enough to choose a topology.

## Mechanism

Represent task dependencies as a directed [[graph]], then specify their state transitions using an [[agent-workflow-graph]]. An edge from A to B means B needs A's result or resulting state. For each proposed parallel branch, specify its read set, permitted effects, output contract and aggregation rule. Independent read-only branches can investigate different evidence. Two branches that modify the same resource or require each other's latest result need coordination; simply giving each a context window does not remove that dependency.

Choose among the protocols in [[multi-agent-orchestration]] after this analysis. A central state owner can retain the authoritative plan and accept bounded advisory results. Parallel workers can search alternatives while one executor serializes committed actions. A decentralized design may be appropriate when conflict resolution and termination are explicit, but it is not inherently more capable. Shared instructions or source material can correlate errors, so majority agreement does not replace evidence checks.

## One example

Suppose three independent documents each take two minutes to inspect, followed by a one-minute evidence check. With three workers and no overhead, inspection takes two minutes and the check one: three minutes rather than seven. These are invented task durations. If B instead requires a resource created by A and C requires B's committed output, the three two-minute stages still have a six-minute dependency path, even with three workers. Parallel speculation can produce guesses, not valid completed stages.

## Boundaries and check

Real workers add dispatch, repeated context, aggregation and recovery costs. Measure the complete policy against a single-worker and a coordinator-led baseline at matched models, tools and total budgets. Test stale snapshots, delayed results, duplicated effects, partial workers and mistaken aggregation. A benchmark improvement on separable tasks is not proof of improvement on stateful execution.

**Check:** Can two read-only analyses always run independently? No. One may need the other's interpretation or exact evidence selection. Declare that dependency rather than assuming read-only implies separable.

## Prerequisites

- [[multi-agent-orchestration]]
- [[agent-workflow-graph]]
- [[graph]]

## Sources

- <https://www.anthropic.com/engineering/multi-agent-research-system>
- <https://docs.langchain.com/oss/python/langgraph/workflows-agents>
