---
id: bounded-kv-replay
title: Bounded KV Replay
summary: Bounded KV replay rebuilds a short recent attention state on demand instead of persisting all of its keys and values, exchanging recomputation for smaller long-lived storage.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, transformer-attention, prefill-vs-decode]
sources: [https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Bounded KV Replay

## Summary

A serving system can save memory by *recomputing* a bounded recent window's attention state when it is needed rather than keeping every window key and value persistently. **Bounded KV replay** is this storage–compute exchange. It is distinct from compressing stored values or searching a sparse global index.

## Grounded explanation

A [[kv-cache]] normally stores past keys and values so autoregressive decode does not recompute them. If an attention component needs only the last $W$ positions, the system may retain enough inputs or intermediate state to replay those $W$ positions and rebuild its short-window KV. The replay cost is bounded by $W$, not by the entire historical context, provided the required starting state and causal dependencies are available. The design must specify exactly which states survive and when replay occurs; otherwise a supposed memory saving can become an unbounded latency cost.

DeepSeek's V4.1 Flash model card describes “SWA Bounded Replay” as rebuilding missing sliding-window-attention KV from recent tokens instead of persisting that KV to SSD. That is a primary implementation claim, not independent proof of the model card's reported memory ratio. Full persistence, compressed persistence, offloading, and smaller windows are alternatives with different latency, bandwidth, and quality consequences.

Measure persistent and peak device/host bytes, replay FLOPs, time to first token, inter-token latency, and frequency of replay under real prompt and generation patterns. Verify state equivalence after replay within numerical tolerance, including context truncation, batch admission/eviction, and recovery after interruption. Test long-context quality separately: a correct replay of a short window does not ensure that the model can retrieve distant information.

## Sources

- [DeepSeek V4.1 Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash): primary description of SWA Bounded Replay; reported savings are author claims.
