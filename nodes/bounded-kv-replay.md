---
id: bounded-kv-replay
title: Bounded KV Replay
summary: Bounded KV replay rebuilds a short recent attention state on demand instead of persisting all of its keys and values, exchanging recomputation for smaller long-lived storage.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, receptive-field, prefill-vs-decode]
sources: [https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md, https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash]
status: explained
created: 2026-10-08
updated: 2026-10-21
---

# Bounded KV Replay

## Summary

A serving system can save memory by *recomputing* a bounded recent window's attention state when it is needed rather than keeping every window key and value persistently. **Bounded KV replay** is this storage–compute exchange. It is distinct from compressing stored values or searching a sparse global index.

## Grounded explanation

A [[kv-cache]] normally stores past keys and values so autoregressive decode does not recompute them. If an attention component needs only the last $W$ positions, the system may retain enough inputs or intermediate state to replay those $W$ positions and rebuild its short-window KV. The replayed token count can be bounded by $W$ rather than the historical context length. Exact reconstruction additionally requires the original starting state and all causal dependencies; bounding the token suffix alone does not establish exactness. The design must specify exactly which states survive and when replay occurs; otherwise a supposed memory saving can become an unbounded latency cost.

DeepSeek's V4.1 Flash model card describes “SWA Bounded Replay” as rebuilding missing sliding-window-attention KV from recent tokens instead of persisting that KV to SSD. That is a primary implementation claim, not independent proof of the model card's reported memory ratio. Full persistence, compressed persistence, offloading, and smaller windows are alternatives with different latency, bandwidth, and quality consequences.

Measure persistent and peak device/host bytes, replay FLOPs, time to first token, inter-token latency, and frequency of replay under real prompt and generation patterns. Verify state equivalence after replay within numerical tolerance, including context truncation, batch admission/eviction, and recovery after interruption. Test long-context quality separately: a correct replay of a short window does not ensure that the model can retrieve distant information.

## Exact reconstruction versus truncated-window approximation

A stacked local-attention decoder can have a [[receptive-field]] extending beyond one layer's window. For a toy two-layer causal model with window size 3 including the current token, the last output can depend on five original token positions: each layer can reach two additional positions into the past. Replaying only the final three raw tokens without the missing boundary state generally cannot reproduce that output exactly. A supplied compatible intermediate boundary state can change the requirement.

DeepInfer's deployment Q&A explicitly describes its missing-state replay as approximate: replay beginning at position s restricts a query at i to keys from max(s, i-127) through i. It distinguishes encoder recovery from decoder bounded replay and says decoder replay results are used for decode rather than written into the prefix cache. Its README also requires retaining enough suffix for the attention window plus speculative backtracking. These are architecture- and version-specific contracts, not a general theorem that any final 128 tokens reconstruct all layers exactly.

Separate the replayed token bound from total FLOPs, layer count, quality and output equivalence. Compare exact reconstruction, truncated replay and full recomputation on sensitive long-range tasks and restart cases. Accepting an approximation is a model-quality decision as well as a storage policy. [[transformer-attention]] defines the causal dependencies; [[prefill-vs-decode]] determines where reconstruction cost is paid.

## Sources

- [DeepSeek V4.1 Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash): primary description of SWA Bounded Replay; reported savings are author claims.

- <https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md>
