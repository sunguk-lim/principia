---
id: w4a16-weight-only-kernel
title: W4A16 Weight-Only Kernel
summary: A W4A16 weight-only kernel consumes packed four-bit weights and sixteen-bit activations while jointly arranging unpacking, scaling, data movement and matrix execution.
type: concept
tags: [ml/llm/inference]
prereqs: [quantization, cuda-kernel, tensor-core, roofline-model]
sources: [https://github.com/IST-DASLab/marlin, https://arxiv.org/abs/2408.11743]
status: explained
created: 2026-10-27
updated: 2026-10-27
---

# W4A16 Weight-Only Kernel

## Meaning

W4A16 names an operand contract: weights are stored with four-bit codes and activations use a sixteen-bit format. It does not by itself specify the codebook, group scales, packing order, accumulation format or machine instructions. A weight-only kernel makes this representation executable efficiently; it is a different objective from choosing accurate [[quantization]] parameters.

## Mechanism

A [[cuda-kernel]] reads packed codes and their metadata, reconstructs the weight values needed for a small matrix region, and combines them with activation values. One implementation can convert those weights into a format accepted by a [[tensor-core]] and accumulate partial results. Four-bit storage therefore does not imply that every multiplication is a native four-bit operation. The exact supported operand and accumulator formats are a device-and-kernel contract.

Unpacking near the consuming arithmetic avoids first expanding the entire matrix into a large temporary in main memory. The kernel must still pay for bit extraction, scale loads, conversion, synchronization and output reduction. A useful layout arranges both codes and scales for the intended access pattern; offline repacking costs must also be accounted for. Marlin is a primary example of co-designing this layout with asynchronous weight loads, activation reuse and instruction ordering. Its reported speedups are not universal W4A16 guarantees.

## Worked example

Take two quantized weight rows with integer codes [-2, 6] and [4, -4], each using scale 0.5. Their reconstructed rows are [-1, 3] and [2, -2]. For an activation vector [1, 2], the outputs are -1*1 + 3*2 = 5 and 2*1 - 2*2 = -2. Packing changes how the codes arrive, not this intended multiplication. Compare the kernel first against multiplication with these reconstructed weights, then separately compare model quality against the original unquantized weights.

Storage savings are smaller than a bare four-to-one claim. For a hypothetical group of 128 weights, four-bit codes require 512 bits. One sixteen-bit scale adds 16, giving 528 bits, or 4.125 bits per weight. Original sixteen-bit weights need 2048 bits, so the ratio is 2048/528, about 3.88, before alignment, zero points or other metadata. That ratio concerns this weight storage only, not activations, cache or wall time.

## Validation and alternatives

Use the [[roofline-model]] to ask whether lower weight traffic can matter at the actual batch shape. More activation reuse can shift the limit toward arithmetic or unpacking; tiny or skewed expert batches have different utilization. Test supported shapes, tails, strides, scale grouping, repeated launches and numerical tolerance against reconstructed-weight reference outputs. Then evaluate task quality and full-service latency with the exact checkpoint and kernel. Compare a wider supported kernel, another packing layout and materialized reconstruction as correctness/performance baselines. Reject a format mismatch rather than interpreting arbitrary packed bytes as a valid matrix.

## Check your understanding

Does W4A16 promise four times faster serving? No. Metadata, conversion, shape utilization and the rest of the serving path remain.

## Prerequisites

- [[quantization]]
- [[cuda-kernel]]
- [[tensor-core]]
- [[roofline-model]]

## Sources

- [Marlin implementation and design](https://github.com/IST-DASLab/marlin): FP16-by-INT4 kernel, packing, metadata, data reuse and documented hardware scope.
- [Frantar et al., MARLIN](https://arxiv.org/abs/2408.11743): mixed-precision autoregressive kernel design.
