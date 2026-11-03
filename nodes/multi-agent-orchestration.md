---
id: multi-agent-orchestration
title: Multi-Agent Orchestration
summary: Multi-agent orchestration assigns bounded roles and communication paths to multiple model-driven workers while an explicit protocol coordinates state, tools, termination, and verification.
type: concept
tags: [ml/agents]
prereqs: [transformer-attention, structured-output, measurement]
sources: [https://www.anthropic.com/engineering/multi-agent-research-system, https://arxiv.org/abs/2308.08155]
status: explained
created: 2026-09-10
updated: 2026-11-04
---

# Multi-Agent Orchestration

## Summary

**Multi-agent orchestration** decomposes a task among several model-driven workers and defines how they exchange messages, invoke tools, share state, and decide that work is complete.

## Grounded explanation

An orchestrated system needs more than role labels. Specify each worker’s input and output contract, allowed tools, private and shared state, routing rules, stopping condition, retry budget, and authority. [[structured-output]] can make handoffs machine-checkable instead of relying on prose conventions.

Common topologies include a sequential pipeline, a central coordinator with specialists, a critic–solver loop, and a group conversation. Each changes failure propagation. Pipelines make provenance clearer but can compound early errors; open conversation allows flexible recovery but increases message cost and makes termination harder to reason about.

Multiple workers do not create independent evidence when they use the same model, prompt assumptions, or retrieved source. Agreement can be correlated. A critic can improve results only when it has a useful verification signal, different information, or executable checks—not merely another opportunity to generate plausible text.

Tool access requires least privilege and explicit data boundaries. Treat scraped or retrieved content as untrusted, validate every handoff, cap recursion, and ensure that one worker cannot delegate broader authority than it received. Record the worker, prompt or policy version, tool call, inputs, outputs, and parent task for traceability.

Compare orchestration with a single-worker baseline at equal model and tool budgets. [[measurement]] should include task success, independently verified correctness, tool failures, handoff loss, latency, token and external-service cost, retries, and safety violations. Keep multiple workers only when decomposition improves these outcomes enough to justify added state and coordination risk.

## Separating strategy from search

A coordinator can be restricted to planning and worker dispatch while research workers alone have search access. This changes the permitted action space: the coordinator must formulate a self-contained brief rather than satisfy every subquestion through its own browsing. Enforce the restriction in tool exposure and authorization, not merely in a role prompt. It is a hypothesis about better task decomposition, not a theorem that coordinators must never search.

For example, dispatch separate evidence questions about mechanism, limitations and competing explanations. Each worker returns source identifiers, claims and unresolved gaps. A deterministic assembly step can renumber identifiers and remove duplicate references, but it cannot verify that a source entails a claim. Preserve that claim-to-evidence association when merging. A shallow topology limits the number of summaries passed between workers; it does not prevent every distortion. Compare tool-separated and search-capable coordinators at equal research and model budgets, checking completeness, evidence support, handoff loss and latency rather than a vendor leaderboard.

## Communication cost follows the topology

Count communication edges and rounds rather than treating worker count as a complete cost model. One directed all-to-all round among n workers has n(n-1) messages if every distinct pair exchanges one message. With four workers that is 12 messages, whereas a coordinator collecting one result from each of four workers receives four worker-result messages, plus whatever dispatch and follow-up it actually sends. These are examples under explicit protocols, not unavoidable costs of all multi-agent systems.

Record message sizes, coordinator and aggregation calls, duplicate tool work, serialized dependencies and state contention. Parallel generation can increase total cost while reducing latency; lengthy discussion can do the opposite when workers repeatedly wait on one another. Compare topology and round count separately from team size. An early wrong draft can anchor later revisions, while independent proposals can diversify starts; neither independence of sampling nor different role names proves independent errors. Retain a serial baseline when successive steps genuinely depend on new evidence or executable feedback.

## Compression placement and late synthesis

A convergent hierarchy repeatedly compresses worker findings before the final decision. With bounded intermediate messages, a minority contradiction or evidence reference can disappear before reaching the final reviewer. A divergent structure moves from a shared proposal into branches and performs synthesis later. These alter both where information is compressed and which initial assumptions workers inherit; reversing arrows is not a universal quality improvement.

For an invented four-worker investigation, three workers find supporting evidence and one finds a counterexample. If an intermediate summary reports only the majority conclusion, a later manager cannot evaluate the discarded counterexample. Retaining the counterexample’s source ID, scope and uncertainty lets the final reviewer decide whether it actually invalidates the claim. Conversely, giving every branch the same flawed root proposal can correlate their searches even when their final reports are combined late.

Compare convergent, divergent and hybrid policies under equal task sets, total tokens, tools and agent counts. Track fact and disagreement survival at every handoff, evidence support, correlated errors, selector failures, critical-path latency and complete resource use. Include direct structured aggregation and a single-worker baseline. Provider multi-agent engineering reports motivate shallow, evidence-preserving handoffs; they do not prove that every bottom-up organization loses to every top-down tree.

## Prerequisites

- [[transformer-attention]]
- [[structured-output]]
- [[measurement]]

## Sources

- [Wu et al., “AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation”](https://arxiv.org/abs/2308.08155): presents customizable conversational workers combining language models, human input, tools, and programmable interaction patterns.

- <https://arxiv.org/abs/2308.08155>

- <https://www.anthropic.com/engineering/multi-agent-research-system>
