---
id: multi-agent-scaling-evaluation
title: Multi-Agent Scaling Evaluation
summary: Multi-agent scaling evaluation measures how team size changes verified task outcomes and total resources before selecting a budget-feasible collaboration policy.
type: concept
tags: [ml/agents]
prereqs: [multi-agent-orchestration, quality-cost-model-selection, agent-task-cost]
sources: [https://www.anthropic.com/engineering/multi-agent-research-system, https://arxiv.org/abs/2408.03314, https://arxiv.org/abs/2406.04692]
status: explained
created: 2026-11-03
updated: 2026-11-08
---

# Multi-Agent Scaling Evaluation

## Meaning

Adding workers changes both available exploration and coordination cost. A scaling evaluation estimates that trade-off for a declared task population. It does not assume that quality must increase, follow an S-curve, or saturate at a universal team size. More independent attempts, more discussion and a stronger single model are different interventions.

## Mechanism

Pin the model, task set, tools, stopping policy and communication topology defined by [[multi-agent-orchestration]]. Vary team size over a small declared grid and repeat trials. First measure the system as configured; then compare equal-total-budget alternatives to distinguish the value of collaboration from simply spending more resources. Report independently verified success, failures and important task slices, not merely judge preference or agent agreement.

Apply [[agent-task-cost]] to every worker, coordinator, selector, tool and failed attempt. Parallel work can shorten the critical path while increasing total tokens. Measure latency tails separately. Use [[quality-cost-model-selection]] to reject configurations that violate the quality or resource contract; select on development data and reserve an untouched acceptance set. The incremental benefit is the measured outcome change between two configurations, not a promise about the next doubling.

## Worked example

On an invented 200-task validation set, teams of 1, 4 and 8 workers resolve 140, 160 and 162 tasks, costing $20, $45 and $80 respectively. Moving 1 to 4 buys 20 additional successes for $25; moving 4 to 8 buys only 2 for $35. Those ratios are $1.25 and $17.50 per additional validation success. They describe this cohort, not the cost of an individual task or a causal effect for every deployment.

If the budget is $50, the eight-worker configuration is infeasible regardless of its point estimate. The four-worker configuration is a candidate, but its true advantage still needs uncertainty estimates and held-out confirmation. An equal-$45 single-worker alternative may do better; without that baseline, the experiment cannot attribute the gain to team structure.

## Boundaries and validation

Shared models and evidence can create correlated errors. A weak selector may discard the one correct candidate; communication can duplicate research or spread an early false premise. Inspect disagreement, evidence coverage, message paths and selector errors. Ablate worker count, communication rounds and proposal diversity separately. Provider engineering reports motivate these mechanisms but their benchmark gains do not establish a universal scaling law. Never infer that a longer serial chain is always worse than every parallel topology.

## Separate selection error from synthesis gain

Hold the candidate pool fixed when evaluating an aggregator. Compare a deployable selector, direct synthesis and a diagnostic oracle that selects the best candidate using unavailable ground truth. The oracle is a ceiling for selection from that pool, not a production baseline or a ceiling for newly constructed answers. Attribute lost quality separately to absence of a good candidate, failure to select one, and damage introduced during synthesis.

For an invented 100-task pool, at least one correct candidate exists on 80 tasks. A real selector succeeds on 65; a synthesizer succeeds on 72. Its measured gain over that selector is seven percentage points, while it remains eight points below the pool's oracle-selection result. It may nevertheless solve some tasks with no individually correct candidate by combining compatible partial work. Preserve paired per-task outcomes: aggregate subtraction alone cannot tell whether synthesis fixed ten tasks and broke three or fixed thirty and broke twenty-three.

Use fixed candidate sets to isolate aggregation, then compare the complete generation-plus-selection/synthesis policies at equal total budgets. Track constraint violations, discarded counterevidence, unsupported new claims and cost. Claim-to-source tracing diagnoses loss, but lexical novelty is not the objective: copying a verified correct candidate can be optimal. The Mixture-of-Agents primary paper motivates response-conditioned synthesis without proving universal gains.

## Prerequisites

- [[multi-agent-orchestration]]
- [[quality-cost-model-selection]]
- [[agent-task-cost]]

## Sources

- <https://www.anthropic.com/engineering/multi-agent-research-system>
- <https://arxiv.org/abs/2408.03314>

- <https://arxiv.org/abs/2406.04692>
