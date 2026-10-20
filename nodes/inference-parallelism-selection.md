---
id: inference-parallelism-selection
title: Inference Parallelism Selection
summary: Inference parallelism selection maps a measured serving bottleneck to replica, weight, stage, context, or expert partitioning under the actual device topology.
type: concept
tags: [ml/llm/inference]
prereqs: [data-parallelism, tensor-parallelism, pipeline-parallelism, inference-context-parallelism, expert-parallelism, llm-serving-metric-triangulation]
sources: [https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md, https://docs.vllm.ai/en/stable/serving/parallelism_scaling/, https://docs.vllm.ai/en/stable/serving/context_parallel_deployment/, https://docs.vllm.ai/en/stable/serving/data_parallel_deployment/]
status: explained
created: 2026-10-14
updated: 2026-10-21
---

# Inference Parallelism Selection

## Summary

A deployment rarely needs every parallelism technique. **Inference parallelism selection** starts with the limiting resource—weight capacity, prefill work, KV capacity, decode latency, expert placement, or queueing—and chooses the smallest partition that addresses it without making communication or coordination dominant.

## Grounded explanation

If one replica meets latency objectives but requests queue, [[data-parallelism]] adds independent replicas. If model weights do not fit, [[tensor-parallelism]] splits operations or [[pipeline-parallelism]] assigns layer stages; the former communicates repeatedly within layers, while the latter needs enough concurrent microbatches to fill its pipeline. Long prompts or KV pressure can justify [[inference-context-parallelism]], which itself separates prefill compute from decode cache sharding. [[expert-parallelism]] places mixture-of-experts weights but adds token routing and load imbalance. These axes can combine, but each new axis adds a cost and a failure mode.

Placement follows topology: frequent tensor collectives generally need faster links than infrequent stage transfers. A single model may use one layout within a node and another across nodes. Do not assume aggregate VRAM is one shared address space, or that a larger GPU count always improves time to first token or inter-token latency. [[llm-serving-metric-triangulation]] measures the actual user-visible bottleneck and guards against optimizing throughput while worsening tail latency.

Sweep representative prompt/output lengths, concurrency, and mixture-of-experts routing skew. Record peak memory, queue delay, TTFT, inter-token latency, throughput, link utilization, idle stages, and cost at equal model quality. Compare each added dimension against the simpler layout it replaces. An advertised speedup under another workload is not a placement rule.

## Phase-specific layouts need phase-specific demand

A model can use attention data parallelism with expert-parallel feedforward work and still choose different group widths for prefill and decode. DeepInfer documents small prefill groups and wide decode groups for one large-scale MoE deployment. Prefill, decode and storage are provisioned separately; its suggested production sizes are not a universal minimum model deployment.

Wider decode groups can raise expert batches only when enough live requests supply tokens. At low offered load, idle devices and collective overhead can make a narrower or tensor-parallel layout preferable. Compare service demand in uncached prompt tokens and active decode requests, not an assumed 1:1 device ratio. Topology, route skew, cache compatibility and KV-transfer costs constrain the feasible configurations. Validate the actual release: an offline engine exposing distributed primitives does not automatically include routing, persistent cache storage or the complete disaggregated service.

## Prerequisites

- [[data-parallelism]]
- [[tensor-parallelism]]
- [[pipeline-parallelism]]
- [[inference-context-parallelism]]
- [[expert-parallelism]]
- [[llm-serving-metric-triangulation]]

## Sources

- [vLLM Parallelism and Scaling](https://docs.vllm.ai/en/stable/serving/parallelism_scaling/): distributed inference layout guidance.
- [vLLM Context Parallel Deployment](https://docs.vllm.ai/en/stable/serving/context_parallel_deployment/): separate prefill and decode objectives.
- [vLLM Data Parallel Deployment](https://docs.vllm.ai/en/stable/serving/data_parallel_deployment/): replica and expert-partition combinations.

- <https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md>
