---
id: access-based-memory-decay
title: "Access-Based Memory Decay"
summary: "Access-based memory decay lowers retrieval priority as time since last use grows, modeling reinforcement through retrieval rather than proving that frequently recalled information is current."
type: concept
tags: [ml/agents]
prereqs: [agent-memory, exponential-function]
sources: [https://arxiv.org/html/2304.03442v2#S4.SS1, https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/persona/cognitive_modules/retrieve.py]
status: explained
created: 2026-11-26
updated: 2026-11-26
---

# Access-Based Memory Decay

## Meaning

Access-based decay is a recency feature computed from the last retrieval of a memory. It favors records recently used, which can preserve continuity across related decisions. It is not the same as decay from the event's creation or last factual verification. [[agent-memory]] supplies those separately meaningful timestamps.

## Mechanism

Let a be elapsed intervals since last access and let d be a decay factor strictly between zero and one. Define the recency score R=d^a, using [[exponential-function]]. Each additional interval multiplies priority by d; an access resets a under the application's update rule. The Generative Agents paper defines exponential decay by sandbox hours since retrieval. Its repository contains a different rank-based recency implementation, so the paper's time rule and that code path must not be reported as identical.

Specify the clock, interval units, update policy and handling of future or missing timestamps. Updating only selected records differs from updating every candidate inspected. Refreshing access is a consequence of the retrieval policy itself: an initially favored memory can keep winning and thereby continually refresh itself. This feedback does not revalidate its content.

## One example

Choose a hypothetical d=0.8 per hour. A record last accessed two hours ago has score 0.8×0.8=0.64. Another last accessed five hours ago has score 0.32768. If the second record is selected now, its elapsed age resets to zero and its score becomes 1. The underlying event may still be years old; only its use became recent.

A policy changed yesterday can therefore conflict with an old rule recalled every hour. Enforce validity separately rather than expecting decay to remove the old rule.

## Validation and boundaries

Compare creation-time, verification-time and access-time decay on held-out sequences. Measure stale recall, recovery of infrequently needed facts, popularity feedback and task success across different decay rates. Keep authoritative constraints outside a ranking heuristic. A low score is not deletion, and a high score is not trust.

## Check your understanding

Does recalling an obsolete rule make it fresh evidence? No. Access time measures use, not correctness.

## Prerequisites

- [[agent-memory]]
- [[exponential-function]]

## Sources

- <https://arxiv.org/html/2304.03442v2#S4.SS1>

- <https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/persona/cognitive_modules/retrieve.py> — implementation differs from paper time decay.
