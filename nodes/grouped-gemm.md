---
id: grouped-gemm
title: "Grouped Matrix Multiplication"
summary: "Grouped matrix multiplication schedules several independently shaped matrix products in one grouped execution while preserving each product and its output identity."
type: concept
tags: [parallel-computing]
prereqs: [matrix-multiplication, cuda-thread-hierarchy]
sources: [https://docs.nvidia.com/cutlass/latest/media/docs/cpp/grouped_scheduler.html]
status: explained
created: 2026-11-08
updated: 2026-11-08
---

# Grouped Matrix Multiplication

## Meaning

A group of small matrix products may waste time in separate launches or leave insufficient tiles for the device. Grouped multiplication schedules work from several products together. Unlike a uniform batched product, members can have different row counts or other supported shapes; each still has its own operands and result.

## Mechanism

For product i, let A_i have m_i rows and k_i columns, and B_i have k_i rows and n_i columns. [[matrix-multiplication]] produces C_i with m_i rows and n_i columns. Provide shapes, operand locations and output identities to a grouped kernel. Work is divided into tiles and assigned to blocks in the [[cuda-thread-hierarchy]]. CUTLASS documents a persistent scheduler whose blocks repeatedly obtain another tile across the problem group rather than requiring one separate launch per product.

The scheduler must map each tile to the correct product and coordinates. Shared scheduling does not mix weights or numerically add unrelated outputs. It also does not make unequal-size products equal-cost: tile counts, reduction lengths, alignment and memory layout still matter. Group metadata and schedule calculation introduce their own overhead.

## One example

Two hypothetical experts have token-row counts three and one. Both multiply two input features by two output features. For the first, A_1=[[1,2],[2,1],[3,1]] and B_1=[[1,0],[0,2]], yielding C_1=[[1,4],[2,2],[3,2]]. For the second, A_2=[[2,3]] and B_2=[[2,1],[1,0]], yielding C_2=[[7,2]]. A grouped execution must preserve those separate products and the association back to their original rows. Padding both experts to three rows would schedule six row positions rather than four useful rows; a ragged grouped design can avoid some such waste, though hardware tiling may still pad internally.

## Check your understanding

Does grouping ensure a speedup? No. Tiny groups, scheduling overhead, skewed reductions or an already-efficient baseline can erase the benefit. Validate results against independent products with the required precision, then measure launch gaps, tile occupancy, metadata setup and full application latency. In an MoE path, grouped expert compute does not remove token dispatch or combine communication. Supported shapes, dtypes and layouts are implementation-specific; verify the chosen kernel rather than inferring support from the mathematical interface.

## Prerequisites

- [[matrix-multiplication]]
- [[cuda-thread-hierarchy]]

## Sources

- <https://docs.nvidia.com/cutlass/latest/media/docs/cpp/grouped_scheduler.html>
