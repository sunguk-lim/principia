---
id: hash-expert-routing
title: "Hash-Based Expert Routing"
summary: "Hash-based expert routing deterministically maps a declared token feature to experts without learning a context-dependent routing gate."
type: concept
tags: [ml/llm/architecture]
prereqs: [mixture-of-experts, hash-map]
sources: [https://arxiv.org/html/2106.04426v3]
status: explained
created: 2026-11-08
updated: 2026-11-08
---

# Hash-Based Expert Routing

## Meaning

A hash router chooses expert identity from a fixed mapping rather than learning the gate from each contextual token representation. This removes the learned selection parameters, not the expert networks or their dependence on contextual input.

## Mechanism

Choose an input feature, a fixed [[hash-map|hash mapping]] or lookup mapping, and an expert-count rule. For token-ID routing, the same vocabulary ID maps to the same expert in every occurrence at that layer. The selected [[mixture-of-experts]] transformation still receives the current hidden representation, so two occurrences of one word can produce different outputs even though they visit the same expert. Layers can have different mappings; the rule and its lifecycle belong in the model contract.

The Hash Layers paper studies token hashing in Transformer feed-forward layers. It compares several mappings and input features; it does not establish that any arbitrary hash produces equal traffic or universal quality. A uniform distribution over possible hash outputs does not make the actual token-frequency distribution uniform.

## One example

Use a toy rule expert_id = token_id modulo three. Token IDs [4,4,4,5,6] map to experts [1,1,1,2,0]. Counts in expert order [0,1,2] are [1,3,1], despite the three available destinations. Repeating token 4 in a different context still selects expert 1; the representation passed to that expert can change. Changing the mapping after training may send those representations to a transformation trained for different traffic.

## Check your understanding

Does removing the learned gate eliminate load imbalance? No. Frequent tokens, feature choice and shifted traffic still matter. Measure per-expert assignment counts, skew, quality by token/domain, overflow and complete execution time. Separate routing-computation savings from memory and communication costs. Compare fixed mappings and learned selection with matched expert architecture and active work. If using frequency-aware mapping or multiple hash destinations, state that additional mechanism rather than attributing it to hashing alone. Deterministic routing also does not guarantee bit-identical full-model outputs across kernels or batches.

## Prerequisites

- [[mixture-of-experts]]
- [[hash-map]]

## Sources

- <https://arxiv.org/html/2106.04426v3>
