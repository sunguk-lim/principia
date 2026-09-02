---
id: post-training-quantization
title: Post-Training Quantization
summary: Post-training quantization converts a trained neural network to lower-bit weights, activations, or both without updating learned parameters, then accepts the conversion only if measured task quality stays within a declared tolerance.
type: concept
tags: [ml/llm/inference]
prereqs: [quantization, neural-network, loss-function, tensor]
sources: [https://developer.nvidia.com/blog/model-quantization-post-training-quantization-using-nvidia-model-optimizer/, arxiv:1712.05877]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Post-Training Quantization

## Summary

Post-training quantization (PTQ) converts an already trained [[neural-network]] to lower-bit weights, activations, or both without updating its learned parameters. It applies [[quantization]] after training, then accepts the conversion only if the measured task quality remains within an explicit tolerance under the original [[loss-function]] or another task metric.

## Grounded explanation

### The problem PTQ solves

A trained [[neural-network]] stores many parameter values and repeatedly moves them into arithmetic units during inference. Wide values consume memory and transfer bandwidth. Re-training the network in a low-bit representation may recover quality, but it requires training data, compute, and another optimization run. PTQ asks a narrower question:

> Can the fixed trained parameters be mapped to a smaller set of representable values, with no parameter-learning step, while keeping the deployed model's error within a declared budget?

The phrase **post-training** fixes the boundary. Training has already produced the parameters. The conversion may inspect those parameters and may run representative inputs to observe activation ranges, but it does not use [[loss-function]] gradients to update the parameters. If gradients update them to adapt to the low-bit representation, the procedure is no longer PTQ.

### The conversion

PTQ is an application of [[quantization]] to selected [[tensor]]s in the trained network. For one group of real values $x$, choose a scale $s$, map each value to an integer code,

$$q = \operatorname{round}(x/s),$$

and recover the value used by arithmetic as

$$\hat{x} = q s.$$

The scale may be shared by a whole tensor, a channel, or a smaller group. A coarse group stores fewer scales and is simpler to execute, but one large outlier can enlarge $s$ for every value in the group. That spreads the available codes too thinly around the many smaller values. Finer groups isolate outliers and usually reduce error, but store more scale metadata and may have less efficient hardware support.

PTQ therefore makes three coupled choices:

1. **Scope:** quantize weights only, or weights and intermediate activations. Weight-only conversion is simpler because the fixed weights reveal their ranges directly. Activation conversion can reduce more memory traffic, but activation ranges depend on inputs.
2. **Bit width and grouping:** fewer bits save more storage and bandwidth but increase rounding error; finer groups reduce that error but add metadata and execution complexity.
3. **Range selection:** make the scale wide enough to preserve rare extreme values, or deliberately clip extremes so the common values receive finer spacing. Preserving every outlier avoids clipping error but can increase rounding error for most values.

These choices are not interchangeable with the mathematical act of [[quantization]] itself. Quantization defines the mapping. PTQ is the deployment procedure that chooses where and how to apply that mapping to a completed model, then measures whether the converted model is still acceptable.

### Worked instance

Suppose one trained layer contains the weights

$$x = [-1.0,\ -0.6,\ 0.2,\ 0.9].$$

Use signed 3-bit symmetric codes $q \in [-3,3]$. The largest magnitude is $1.0$, so a scale that covers the full range is

$$s = 1.0/3 \approx 0.333.$$

The stored codes are

$$q = \operatorname{round}(x/s) = [-3,\ -2,\ 1,\ 3],$$

and dequantization gives

$$\hat{x} = [-1.000,\ -0.667,\ 0.333,\ 1.000].$$

The layer has not learned new parameters; the four original values were projected onto a seven-level grid. Their absolute errors are $[0, 0.067, 0.133, 0.100]$. Those local errors do not by themselves decide whether the model is usable: a small perturbation in a sensitive layer can matter more than a larger perturbation elsewhere. PTQ must therefore validate the complete converted network, not merely report average weight error.

### Diagnostics and alternatives

When quality falls, isolate the mechanism before changing the entire recipe:

- compare weight-only conversion with weight-plus-activation conversion;
- restore one layer at a time to the original representation to locate sensitive layers;
- compare per-tensor with finer grouping to test whether outliers are wasting the code range;
- compare clipping and non-clipping ranges to separate clipping error from rounding error;
- inspect several input slices, because activation ranges and model errors can differ by domain.

A mixed representation is a valid outcome: leave sensitive layers wide and quantize the rest. If PTQ still misses the quality target, alternatives are a wider bit width or training that explicitly adapts parameters to simulated quantization. The latter can recover accuracy but gives up PTQ's main advantage—no training pass—and adds data, compute, and optimization risk.

### Validation contract

Choose the acceptance contract before conversion. Keep the original network as the baseline, evaluate both versions on the same representative examples, and compare the original [[loss-function]] plus the deployment metric that users actually experience. Record model size, peak memory, latency, throughput, and any hardware-specific conversion overhead alongside quality. Warm up execution, hold batching and input shapes fixed, and report multiple workload slices rather than one aggregate.

PTQ succeeds only when the lower-bit model meets both sides of the contract: a measured resource improvement and a quality change inside the declared tolerance. A smaller file without faster supported kernels is not an inference win, and a speedup whose quality cost was never measured is not a validated conversion.

## Prerequisites

- [[quantization]]
- [[neural-network]]
- [[loss-function]]
- [[tensor]]

## Sources

- NVIDIA Technical Blog, “Model Quantization: Post-Training Quantization Using NVIDIA Model Optimizer” — deployment workflow and PTQ configuration choices. The saved Raindrop snapshot supplied metadata only; source-specific claims were not relied on beyond this topic boundary.
- Jacob et al., “Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference” (2018), arXiv:1712.05877 — scale and integer-mapping foundation.
