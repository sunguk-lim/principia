---
id: gated-delta-network
title: Gated Delta Network
summary: A Gated Delta Network updates a fixed-size key–value state with selective forgetting and an error-correcting delta rule instead of storing every past token separately.
type: concept
tags: [ml/llm/architecture]
prereqs: [linear-transformer-attention]
sources: [https://arxiv.org/abs/2412.06464]
status: explained
created: 2026-10-12
updated: 2026-10-12
---

# Gated Delta Network

## Summary

A **Gated Delta Network** is a sequence layer whose memory is a fixed-size matrix, not a list of token positions. At each token, a gate can diminish old state and a delta update corrects what the state predicts for the new key. The design combines selective forgetting with targeted writing; it does not guarantee exact recall of every earlier token.

## Grounded explanation

[[linear-transformer-attention]] replaces an explicit attention matrix with a running state that summarizes prior key–value interactions. A basic additive update can overwrite useful associations or accumulate stale ones. A gated delta rule makes two decisions: how much of the old state to retain, and how strongly to correct the state for the current key. In a simplified notation, if the current state predicts $S_{t-1}k_t$, the correction is proportional to $(v_t-S_{t-1}k_t)k_t^\top$; a learned gate controls retention. The published method supplies a parallel training algorithm as well as a recurrent decoding form.

The state shape is independent of sequence length, so per-token recurrent-state storage does not grow with context. That is a **memory bound**, not a proof of unbounded recall: different histories can map to similar states, and exact retrieval may be harder than with token-addressable full attention. Quality and runtime depend on state dimensions, kernels, hardware, and the task.

## When to use it

Consider this layer when long-context decode memory or bandwidth limits a model and the task tolerates compressed history. Compare it with full attention and other recurrent layers at matched model size and training budget. Measure exact retrieval, evolving-state tasks, state bytes, and decode latency across context lengths; ablate the gate and delta correction to attribute any gains.

## Prerequisites

- [[linear-transformer-attention]]

## Sources

- [Yang et al., *Gated Delta Networks: Improving Mamba2 with Delta Rule*](https://arxiv.org/abs/2412.06464)
