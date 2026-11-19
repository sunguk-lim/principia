---
id: kernel-fusion
title: "Kernel Fusion"
summary: "Kernel fusion executes compatible operations in one device program to reduce intermediate materialization and launch work while preserving a stated numerical contract."
type: concept
tags: [gpu]
prereqs: [cuda-kernel, memory-hierarchy, occupancy]
sources: [https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html]
status: explained
created: 2026-11-20
updated: 2026-11-20
---

# Kernel Fusion

## Meaning

Kernel fusion combines compatible operations into one device program rather than launching a separate [[cuda-kernel]] for each. The objective is to remove avoidable data movement or submission overhead, not to change the mathematical operation. A fused kernel can still contain many instructions and memory accesses.

## Mechanism

Consider row-wise normalization: find a maximum, subtract it, exponentiate, sum and divide. Separate kernels may write and reread large intermediate arrays. A fused program can retain a row or tile in registers or local shared storage, perform the sequence and write the final result. The [[memory-hierarchy]] determines which transfers were actually avoided. A global-memory operation may hit cache, so an API boundary alone does not establish a complete device-memory round trip.

Fusion has boundaries. A producer's output must fit within an executable schedule that respects dependencies and synchronization. Keeping more live values consumes registers or shared storage; spills can restore the traffic that fusion meant to remove. Lower [[occupancy]], redundant computation, oversized tiles or a slower algorithm may outweigh saved launches. An algebraic rewrite, such as combining two compatible projections into one matrix product, is a narrower case; fusion can also cross elementwise and reduction operations without eliminating their dependencies.

The primary Triton softmax tutorial demonstrates one such implementation, including padding, masked loads and resource-dependent program counts. Its favorable matrix sizes and measurements do not prove every softmax implementation or model should use that kernel.

## One example

For a hypothetical vector of N four-byte elements, two elementwise stages each reading and writing an N-element array move about 16N useful bytes. A fused stage that reads the original and writes only the final array moves about 8N, ignoring scalar inputs and cache effects. This is a byte-count reduction, not a promised twofold runtime improvement: arithmetic, launches, alignment and resource limits still contribute.

## Check your understanding

Does fewer kernels prove lower latency? No. Compare equivalent outputs and gradients across shapes, masks and precisions; measure launches, memory traffic, register/shared-storage use, spills, occupancy and end-to-end latency. A capture-and-replay mechanism can reduce host submission work while retaining separate kernels and intermediates; that is not the same transformation as fusion.

## Prerequisites

- [[cuda-kernel]]
- [[memory-hierarchy]]
- [[occupancy]]

## Sources

- <https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html>
