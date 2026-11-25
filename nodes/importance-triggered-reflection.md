---
id: importance-triggered-reflection
title: "Importance-Triggered Reflection"
summary: "Importance-triggered reflection schedules memory synthesis when accumulated event salience reaches a budgeted threshold rather than invoking reflection after every interaction."
type: concept
tags: [ml/agents]
prereqs: [reflective-memory-consolidation, memory-importance-estimation]
sources: [https://arxiv.org/html/2304.03442v2#S4.SS2, https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/persona/cognitive_modules/reflect.py]
status: explained
created: 2026-11-26
updated: 2026-11-26
---

# Importance-Triggered Reflection

## Meaning

An importance trigger determines *when* to consolidate memory, independently of what the consolidation infers. It accumulates the estimated significance of new events and starts synthesis after enough evidence has arrived. [[reflective-memory-consolidation]] defines the synthesis; [[memory-importance-estimation]] supplies fallible weights rather than an objectively measured amount of learning.

## Mechanism

Maintain an accumulator A and threshold T. For each newly admitted event with importance i, add i to A. When A reaches the declared boundary, schedule one bounded reflection over a defined evidence interval. After successful completion, mark the interval consumed and reset or subtract the processed amount according to the policy. The Generative Agents paper describes a threshold of 150 for its simulation; this is not an optimal default for other systems. Its public reflection module checks a countdown and resets counters after reflection.

Operational implementation needs an explicit contract for duplicate events, failures and events arriving during synthesis. Consuming a failed interval can lose learning opportunities; retrying a successful interval without a durable completion record can duplicate memories. These are application-design consequences, not reliability guarantees of the prototype. Limit call count, token use and maximum wait separately from the threshold.

## One example

In an invented system with T=12, successive new-event scores 3, 5 and 6 raise A to 3, 8 and 14. The third event crosses the threshold. A reset-to-zero policy discards the excess 2 for scheduling purposes; a subtract-12 policy retains it. Both need documentation. If another event arrives during reflection, keep its score outside the completed interval so it is not accidentally cleared.

## Validation and boundaries

Compare threshold-triggered, periodic, per-turn and on-demand reflection at matched task volume. Measure useful promotions, stale or missed updates, cost, scheduling delay and duplicate synthesis after recovery. Gradual low-salience changes can fail to trigger, while one manipulated high score can force expensive work. A maximum-age fallback and a hard compute budget address different failure modes.

## Check your understanding

Can raising the threshold guarantee better memories? No. It changes cadence and accumulated evidence, not the validity of an inference.

## Prerequisites

- [[reflective-memory-consolidation]]
- [[memory-importance-estimation]]

## Sources

- <https://arxiv.org/html/2304.03442v2#S4.SS2>
- <https://raw.githubusercontent.com/joonspk-research/generative_agents/main/reverie/backend_server/persona/cognitive_modules/reflect.py>
