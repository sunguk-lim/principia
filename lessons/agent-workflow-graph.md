# Agent Workflow Graph

## Meaning

An agent workflow graph makes steps and transitions explicit: state moves through model calls, deterministic checks, tools, loops, and termination conditions.

## Mechanism

Each node reads part of task state and writes a result. An edge condition selects the next node. The [[agent-execution-harness]] still enforces permissions and executes effects; a graph drawing cannot authorize a tool or prove its outcome. Checkpoints preserve run progress through interruption. Conversation continuity in [[agent-session-state]] is a different lifecycle from this run's completed steps.

Use a graph when branching, retries, or recovery genuinely need inspection. A short linear task may be simpler as plain code. Test cycles with bounded retries, crashes after side effects, state conflicts, and false completion.

## One example

A document agent retrieves sources, assesses whether evidence is sufficient, loops only within a budget, then writes an answer. The graph records why it took each branch and which source IDs supported completion.

Every step also needs an input/output contract. Validate required fields, schema version and semantic acceptance conditions before downstream work. Static type annotations and successful parsing do not prove that a result is true, current or authorized. A numeric price without currency and billing interval is insufficient for a meaningful comparison.

Bind accepted outputs to their actual input revision and producing attempt. If evidence revision 4 produced extraction revision 7, a retrieval retry writing evidence revision 5 cannot silently relabel extraction 7 as derived from 5. Preserve the accepted pairing or rerun and validate extraction. A familiar file path is not a stable data revision. These checks belong to the graph's handoff contract, while the surrounding harness still enforces authority and effects.

## Check your understanding

**Question:** Does a completed graph node establish real-world success? **Answer:** No; the effect requires separate evidence.
