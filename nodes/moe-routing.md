---
id: moe-routing
title: MoE Routing
summary: "MoE routing defines token-to-expert assignments, output weights and capacity handling; token-choice top-k is one routing family rather than a universal contract."
type: concept
tags: [ml/llm/architecture]
prereqs: [mixture-of-experts, softmax]
sources: [https://arxiv.org/html/1701.06538v1, https://arxiv.org/html/2202.09368v2, https://arxiv.org/html/2412.19437v2]
status: explained
created: 2026-06-23
updated: 2026-11-08
---

# MoE Routing

## Summary

Routing defines which expert transformations contribute to each token, with what weights and under what capacity rules. In [[mixture-of-experts]], learned token-choice top-k is a common family, not the definition of every router. Expert-choice, deterministic mappings and soft token mixtures use different selection contracts.

## Grounded explanation

### Token-choice scores and output weights

For a common token-choice gate, multiply a token's hidden vector by a learned matrix to obtain expert scores. [[softmax]] converts them to normalized preferences; retain the largest k. Selected weights may be renormalized, but that convention is model-specific. Selection scores and output-mixing weights need not even be identical: DeepSeek-V3 documents balancing biases used for selection while output weights derive from the original affinities. Fixed k bounds selected expert evaluations, not storage, total routing work or wall-clock latency.

For an original top-two example, preferences [.50,.30,.20] select experts one and two. Under selected-weight renormalization, their weights become .50/.80=.625 and .30/.80=.375. If their scalar outputs are 4 and 8, the combined output is .625*4+.375*8=5.5. Keeping the original masked weights instead gives .50*4+.30*8=4.4. Neither convention may be silently substituted for the checkpoint's trained computation.

### Capacity and overflow

Expert capacity counts token-expert assignments, not necessarily distinct tokens. Let T tokens each select k experts from E total experts. There are T*k assignments, with average T*k/E per expert. One common illustrative cap is the ceiling of c*T*k/E, where c is a capacity factor. Definitions, rounding and routing stages differ among implementations, so record the actual formula.

For T=6, k=2, E=4 and c=1, twelve assignments imply a cap of three each. If requested counts are [5,3,2,2], the first expert overflows by two even though total demand equals total capacity. A dropping policy removes those two branch contributions; a rerouting policy changes their destinations; a dropless implementation can allocate or schedule the uneven work. These are different computations and execution costs. A token losing one branch is not necessarily removed from the sequence or left wholly unchanged: other expert contributions and any residual path still matter.

A training-time balancing objective encourages a distribution, but does not guarantee every serving batch is balanced. Capacity constraints occur during training as well as serving; they are not inherently inference-only. Dropping is not universally required, and its quality cost is not guaranteed small. The DeepSeek-V3 report describes no token dropping in its training and inference design, not a guarantee for every sparse system.

### Validation

Declare training and inference selection separately, including grouping, causality, weights, ties, capacity and empty/overflow behavior. Inspect per-expert loads, per-token coverage, dropped assignments, task quality and complete dispatch/compute/combine latency. Equal token counts do not imply identical expert runtime, and a numerically balanced router is not proof of a faster application. Compare interventions against the same checkpoint and quality contract; changing routing after training can change the learned function.

## Prerequisites

- [[mixture-of-experts]]
- [[softmax]]

## Sources

- <https://arxiv.org/html/1701.06538v1> — sparse gating and load controls.
- <https://arxiv.org/html/2202.09368v2> — token-choice limitations and expert-choice alternative.
- <https://arxiv.org/html/2412.19437v2> — selection biases, original-affinity mixing and dropless design.
