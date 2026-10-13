# Stateful Coding-Agent Evaluation

## Meaning

Stateful coding-agent evaluation chains repository tasks so each task begins with the agent’s earlier committed changes, exposing cumulative regressions and maintenance costs.

## Mechanism

An isolated issue test asks whether a patch solves one problem from a prepared repository state. **Stateful coding-agent evaluation** asks whether a sequence of patches leaves a usable repository for the next task. Task $n+1$ starts from the accepted state after task $n$, including the agent's helpers, tests, and architectural choices. This tests a different property from one-task pass rate.

## One example

An agent changes a repository in task one; task two starts from that exact changed tree and tests whether old behavior still works.

## Check your understanding

**Question:** Why is isolated issue pass rate insufficient? **Answer:** It cannot measure the effect of accumulated agent edits on future tasks or repository health.
