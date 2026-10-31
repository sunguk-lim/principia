---
id: attention-head-pruning
title: Attention Head Pruning
summary: Attention head pruning removes selected learned attention contributions and evaluates whether retained quality and actual execution cost justify the structural change.
type: concept
tags: [ml/llm/architecture]
prereqs: [multi-head-attention, measurement]
sources: [https://arxiv.org/html/1905.10650v3]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Attention Head Pruning

## Meaning

Attention head pruning removes selected contributions from a trained multi-head layer. It tests redundancy for a particular model and task; it does not establish that every additional head is redundant or that a narrower-headed model would train equally well from scratch.

## Mechanism

[[multi-head-attention]] combines several head outputs through an output projection. A head mask can multiply one contribution by zero, enabling ablations before structural editing. Rank candidates by an importance estimate or direct validation loss, remove a bounded set, re-evaluate, and optionally adapt remaining weights. Importance can change after other heads are removed; individually harmless removals need not be harmless together.

A masked head may still execute all its matrix operations. Real speedup requires an implementation that eliminates work and preserves legal tensor layouts. Smaller shapes can be less efficient, so theoretical savings do not directly predict wall time. [[measurement]] must distinguish mask-only ablation, physically pruned execution and any retraining cost.

## Worked example

A four-head layer scores 90% on a held-out task. Removing H1 alone yields 89.8%, and removing H2 alone yields 89.9%. Removing both yields 84%. The first two measurements do not license their joint removal: the heads can be substitutes when only one is absent. A greedy process would remove one and remeasure the remaining candidates, using an independent evaluation split for final reporting. If the masked implementation takes the same 10 ms as the original, quality-tolerable removal has not yet produced an inference speedup.

## Boundaries

Michel and colleagues report model- and layer-dependent pruning behavior, including different sensitivity across attention components. These are empirical findings, not a theorem that head count has no expressive effect. Compare task slices, sequence lengths, calibration and long-context behavior. Keep recovery or rollback possible and report retained quality alongside latency, throughput and memory. Pruning a trained checkpoint and designing a new fixed-width head count answer different experimental questions.

## Prerequisites

- [[multi-head-attention]]
- [[measurement]]

## Sources

- <https://arxiv.org/html/1905.10650v3>
