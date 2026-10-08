---
id: inference-accelerator-comparison
title: Inference Accelerator Comparison
summary: "Compare GPU, TPU, and specialized dataflow inference devices at a fixed model, quality target, workload, and system boundary."
type: concept
tags: [ml/llm/inference]
prereqs: [roofline-model, gpu-data-flow, llm-inference-memory-budget]
sources: [https://arxiv.org/abs/1704.04760, https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/best-practices.html]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Inference Accelerator Comparison

## Summary

An accelerator comparison asks whether a GPU, TPU, or other specialized inference device better serves a *specified* model and traffic pattern. Peak arithmetic, one vendor's token-rate demo, and hardware price alone are insufficient. The runtime, compiler, memory system, interconnect, scheduling policy, and supported model operations form the measured system.

## Grounded explanation

The [[roofline-model]] separates compute ceilings from memory-transfer limits. Autoregressive decode at low batch may repeatedly stream weights, while high-batch serving can amortize weight reads and shift the bottleneck toward compute or memory capacity. A device with a large matrix engine may excel at one regime yet underperform on small, irregular, stateful, or unsupported operations. [[gpu-data-flow]] explains one flexible programmable path; specialized devices may expose different memory placement, static scheduling, or compiler constraints. A production inference stack also needs kernels for attention variants, quantization formats, cache management, collective communication, and failure recovery. Porting overhead and model coverage can outweigh a single microbenchmark gain.

First specify checkpoint and numerical format, context and output length distributions, quality tolerance, batch/concurrency, service-level latency target, and deployment constraints. Estimate the full [[llm-inference-memory-budget]] including weights, KV or recurrent state, workspaces, and replicas. Then compare sustained throughput, time to first token, inter-token and tail latency, energy, memory use, utilization, compiler coverage, operational reliability, and total cost at the *same* quality and load. Use a held-out mix of realistic prompts and warm/cold runs. Report unavailable operations or forced model changes explicitly rather than counting them as speedups.

A vendor-reported “10× faster” result is not portable without its baseline, workload, precision, batch, and measurement boundary. Treat an architecture claim as a hypothesis for a controlled benchmark, not a ranking of device families.

## Prerequisites

- [[roofline-model]]
- [[gpu-data-flow]]
- [[llm-inference-memory-budget]]

## Sources

- [Jouppi et al., In-Datacenter Performance Analysis of a Tensor Processing Unit](https://arxiv.org/abs/1704.04760): primary example of workload-specific accelerator analysis.
- [NVIDIA TensorRT performance best practices](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/best-practices.html): runtime, batch, and profiling considerations.
