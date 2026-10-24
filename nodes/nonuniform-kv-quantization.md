---
id: nonuniform-kv-quantization
title: Non-Uniform KV Quantization
summary: Non-uniform KV quantization maps cached values to unequally spaced reconstruction levels chosen to preserve a calibrated distribution or sensitivity objective.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-quantization]
sources: [https://arxiv.org/html/2401.18079v2]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Non-Uniform KV Quantization

## Meaning

Non-uniform KV quantization chooses reconstruction levels that are not evenly spaced. A stored low-bit code selects a level from a codebook, potentially followed by scale reconstruction. It changes the quantizer itself, not just how many values share a scale in [[kv-quantization]].

## Mechanism

Let C be a finite list of reconstruction values. For cached scalar x, select an index q according to a chosen error objective and reconstruct C[q]. An ordinary nearest-level rule minimizes squared reconstruction error for that scalar. Sensitivity weighting can instead allocate scarce levels to reduce important downstream errors. Calibration estimates the relevant distributions and importance; KVQuant studies per-layer sensitivity-weighted non-uniform formats. This is a method-specific design, not a guarantee that matching a histogram preserves attention outputs.

Codebooks, scales, layer distinctions and kernel lookup all consume resources. A codebook that fits calibration can fail after a domain or context-length shift. Outlier separation is another design choice; unequal spacing does not automatically provide sparse outlier storage.

## Worked example

Compare a two-bit uniform codebook [-3,-1,1,3] with an illustrative non-uniform codebook [-3,-0.25,0.25,3]. For values [-0.3,0.2,2.8], nearest-level uniform reconstruction is [-1,1,3], with squared error 0.49+0.64+0.04=1.17. The non-uniform reconstruction is [-0.25,0.25,3], with error 0.0025+0.0025+0.04=0.045. But for x=1.2, the uniform nearest level 1 has error 0.04 while the non-uniform nearest level 0.25 has error 0.9025. The advantage depends on the distribution and objective; the toy codebook is not KVQuant's learned datatype.

Compare codebook and uniform schemes at matched *total* bytes, including metadata and residual buffers. Measure key/value error, attention-output differences, held-out task quality, out-of-distribution robustness and kernel runtime. Publish calibration provenance and format version with the cache configuration.

## Check your understanding

Does the same bit width imply the same reconstruction grid? No. The code-to-value mapping can allocate precision differently.

## Prerequisites

- [[kv-quantization]]

## Sources

- <https://arxiv.org/html/2401.18079v2>
