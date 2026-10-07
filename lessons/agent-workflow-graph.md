# Agent Workflow Graph

## Meaning

An agent workflow graph makes steps and transitions explicit: state moves through model calls, deterministic checks, tools, loops, and termination conditions.

## Mechanism

Each node reads part of task state and writes a result. An edge condition selects the next node. The [[agent-execution-harness]] still enforces permissions and executes effects; a graph drawing cannot authorize a tool or prove its outcome. Checkpoints preserve run progress through interruption. Conversation continuity in [[agent-session-state]] is a different lifecycle from this run's completed steps.

Use a graph when branching, retries, or recovery genuinely need inspection. A short linear task may be simpler as plain code. Test cycles with bounded retries, crashes after side effects, state conflicts, and false completion.

## One example

A document agent retrieves sources, assesses whether evidence is sufficient, loops only within a budget, then writes an answer. The graph records why it took each branch and which source IDs supported completion.

## Check your understanding

**Question:** Does a completed graph node establish real-world success? **Answer:** No; the effect requires separate evidence.
