# Agent-Memory Read Projections

## Meaning

A stored history can be read in different forms: current facts, entity briefings, exact episodes, session outcomes, recurring observations, or initial user context. The question determines the useful view.

## Mechanism

Keep source events, validity times, and provenance. Derive bounded summaries and views from them, but do not replace exact evidence with a summary. A current fact filters by valid time; an episode preserves wording; an observation synthesizes several episodes with uncertainty. Update or invalidate derived views when their underlying evidence changes, and enforce access controls before placing any view into an agent's context.

## One example

After an outage, a thread outcome says “service restored; root cause unknown.” A later question about recurring outages needs several episodes and an evidence-backed observation. It must not transform “unknown” into a confident cause.

## Check your understanding

**Question:** Why not retrieve an entity summary when exact wording is requested? **Answer:** A summary can omit or paraphrase the crucial text; the source episode is needed for fidelity.
