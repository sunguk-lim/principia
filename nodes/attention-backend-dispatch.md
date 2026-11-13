---
id: attention-backend-dispatch
title: Attention Backend Dispatch
summary: Attention backend dispatch selects an implementation of a declared attention operation subject to input compatibility while preserving explicit numerical and masking contracts.
type: concept
tags: [ml/llm/inference]
prereqs: [dropout, transformer-attention, flash-attention, masked-attention-numerics, gpu-kernel-benchmarking]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html]
status: explained
created: 2026-11-14
updated: 2026-11-14
---

# Attention Backend Dispatch

## Meaning

An attention API specifies an operation, not necessarily one kernel. Backend dispatch chooses an available implementation for the device and input. Calling a high-level function is therefore not evidence that a particular fused implementation ran.

## Mechanism

[[transformer-attention]] defines score scaling, masking, normalization and value aggregation. A backend such as [[flash-attention]] stages that operation differently to reduce memory traffic. Compatibility depends on the installed library, device, dtype, head dimensions, layout and mask support. A dispatcher may use another implementation when the preferred path is ineligible.

PyTorch's scaled-dot-product-attention interface can choose implementations automatically. Its `sdpa_kernel` context manager restricts the allowed choices; a forced fused implementation can report why an input is unsupported. Such a context is useful diagnostic control, not a promise that every workload supports that backend. Record the installed version and profile the operation actually executed.

Correctness remains separate from eligibility. Under the documented SDPA boolean mask convention, true means a key participates, unlike a padding-mask interface where true can mean excluded. Follow [[masked-attention-numerics]] for empty queries and finite gradients. Pass zero [[dropout]] probability explicitly during evaluation: changing the enclosing module's mode does not itself rewrite a functional call's probability argument. Different floating-point evaluation orders can differ within a justified tolerance without changing the intended operation.

## One example

Consider an evaluation request with one batch, eight heads, 128 positions and head width 64. First run a compatible mathematical reference with dropout zero. Next restrict dispatch to the desired fused backend for those same inputs. If a new mask makes it unsupported, record that result rather than quietly timing a fallback and labeling it fused. For supported cases, compare output errors and gradients where relevant, then use [[gpu-kernel-benchmarking]] for warmup and device-completed timings. A fast kernel with the wrong mask is not a valid speedup.

## Check your understanding

Does identical API code imply identical backend performance across devices? No. Compatibility and dispatch can change. Check the executed path, numerical contract and complete workload before interpreting latency.

## Prerequisites

- [[transformer-attention]]
- [[flash-attention]]
- [[masked-attention-numerics]]
- [[gpu-kernel-benchmarking]]

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html>
