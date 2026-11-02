# Multi-Agent Scaling Evaluation

## Meaning

Multi-agent scaling evaluation asks whether extra workers improve verified outcomes enough to justify their complete cost. The answer is conditional on tasks, models, tools and communication policy, not a universal number of agents.

## Mechanism

Choose team sizes and a success rubric before running the comparison. Keep the task cohort, model and tool access fixed, record the topology and stopping rules, and repeat trials. Include a single-worker baseline and equal-total-resource alternatives: otherwise a larger team may win simply because it received more inference work. A parallel system can use more total tokens while finishing sooner, so report both total resource use and latency tails.

Account for coordinators, aggregation, tools, retries and failures, not just worker generation. Check quality on difficult slices and verify answers against evidence or executable tests. Agreement is not independent confirmation when workers share the same false assumption. Measure whether a selector keeps correct proposals and whether discussion adds information or merely propagates one draft.

Use development tasks to choose a configuration under explicit quality and cost limits, then validate it on unseen tasks. Uncertainty matters: two extra successes in a small cohort may be noise rather than a dependable improvement.

## One example

For 200 invented validation tasks, 1 worker resolves 140 for $20, 4 workers resolve 160 for $45, and 8 resolve 162 for $80. The first expansion costs $25 for 20 additional successes; the second costs $35 for two. A $50 budget excludes the largest team. The four-worker result still needs comparison with a stronger or longer-running single-worker system at the same total budget.

## Check your understanding

Does a flattening curve prove that agents cannot collaborate? **No.** It describes a particular task and policy. Poor diversity, selection or communication may be the bottleneck; diagnose them before generalizing.
