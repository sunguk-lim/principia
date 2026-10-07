---
id: training-memory-budget
title: Training Memory Budget
summary: A training memory budget accounts for parameters, gradients, optimizer state, retained activations, temporary workspace, and allocator overhead at the workload's peak.
type: concept
tags: [ml/llm/training]
prereqs: [neural-network, gradient-descent, activation-checkpointing]
sources: [https://docs.pytorch.org/docs/stable/notes/cuda.html#memory-management, https://www.deepspeed.ai/tutorials/zero/]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Training Memory Budget

## Summary

A checkpoint's weight bytes are only one part of training memory. A useful **training memory budget** separates parameter copies, gradients, optimizer state, retained forward activations, temporary workspaces, and runtime/allocator reservations. Plan for the peak *coexisting* allocations, not a sum of every tensor ever created.

## Grounded explanation

For $P$ parameters, 16-bit weights occupy about $2P$ bytes before metadata. A particular mixed-precision Adam setup may also keep an FP32 master copy ($4P$), gradients (often $2P$ or $4P$), and two FP32 moment arrays ($8P$). That can suggest roughly $16P$–$18P$ bytes for model-and-optimizer state, but it is not a universal constant: optimizer, framework, precision policy, sharding, and gradient representation change the terms. Confirm the actual live allocations rather than copying a newsletter's formula.

Forward activations retained for [[gradient-descent|backpropagation]] depend on layer shapes, microbatch, sequence length, attention implementation, and what is recomputed. [[activation-checkpointing]] stores fewer intermediates and recomputes selected forward work during backward, trading extra compute for memory. Data parallel replicas multiply per-device state unless gradients or optimizer tensors are sharded; ZeRO documents those partitioning stages. Temporary kernels, communication buffers, graph capture, and allocator fragmentation add peaks that a parameter count cannot predict. PyTorch distinguishes memory occupied by live tensors from memory reserved by its caching allocator.

Profile after warm-up on the actual model, hardware, optimizer, precision, sequence length, and microbatch. Record peak allocated and reserved bytes, optimizer/gradient/activation contributions, failed allocation size, step time, and numerical quality. Sweep sequence length and microbatch separately. Compare checkpointing, smaller microbatches with accumulation, sharding, lower precision, and optimizer changes at equal effective batch and training objective. A model that loads for inference may still be impossible to train under the same device limit.

## Sources

- [PyTorch CUDA memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html#memory-management): allocated and reserved memory diagnostics.
- [DeepSpeed ZeRO tutorial](https://www.deepspeed.ai/tutorials/zero/): optimizer, gradient, and parameter state partitioning.
