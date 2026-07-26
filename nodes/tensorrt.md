---
id: tensorrt
title: TensorRT
summary: An inference compiler + runtime that turns a trained neural network into a GPU-specific "engine" — fusing layers into fewer CUDA kernels, lowering numeric precision, and auto-tuning each kernel to the target GPU, all ahead of time.
type: concept
tags: [gpu]
prereqs: [jit-vs-aot-compilation, cuda-kernel, roofline-model, quantization, neural-network]
sources: ["NVIDIA TensorRT — developer.nvidia.com/tensorrt"]
status: explained
created: 2026-07-06
updated: 2026-07-06
---

# TensorRT

## Summary

**TensorRT** is NVIDIA's **inference optimizer and runtime**: it takes a *trained*
[[neural-network]] and compiles it, **ahead of time** (per [[jit-vs-aot-compilation]]), into a
GPU-specific **"engine"** that runs the same forward pass much faster. It is not a training
framework and adds no new math — it *re-expresses* the existing computation to fit the hardware,
through three optimizations applied at build time: **layer fusion** (merge a chain of layers into a
single [[cuda-kernel]], so intermediate results never round-trip to GPU memory — the memory-bound win
the [[roofline-model]] predicts), **precision reduction** (store weights/activations in FP16 or INT8
via [[quantization]], moving far fewer bytes), and **kernel auto-tuning** (benchmark many candidate
[[cuda-kernel]] implementations for each layer and keep the fastest for *this* GPU and *these* tensor
shapes). The output is a serialized engine specialized to one GPU architecture — fast and warm-up-free
to run, but, like any [[jit-vs-aot-compilation|AOT]] artifact, rigid: rebuild it for a different GPU.

## Grounded explanation

### What TensorRT *is* — a compiler for inference, not a framework

A training framework runs a [[neural-network]] **generically**: it walks the model layer by
layer, launching a separate, general-purpose [[cuda-kernel]] for each operation (a convolution, a bias
add, an activation, a normalization), because during training the network keeps changing and gradients
must flow back through every intermediate. That generality is wasted at **inference** time, where the
weights are frozen and only the forward pass runs, the same shape over and over. TensorRT is the tool
that exploits that: it consumes the trained network **once**, at *build time*, and emits a specialized
**engine** — a fixed, optimized execution plan for one target GPU. The concept to hold onto is
**compiler**: input a portable model, output hardware-specific optimized code, with the optimization
work paid once up front. Everything below is *which* optimizations it applies and *why* each one wins.

### The problem: a naive forward pass is memory-bound and launch-heavy

Run the trained model op-by-op and two costs dominate, both structural rather than arithmetic. First,
**many layers are memory-bound.** By the [[roofline-model]], an operation's speed ceiling is set by
its *arithmetic intensity* — FLOPs performed per byte dragged from GPU memory. A bias add or a ReLU
does about one cheap operation per element while reading that element and writing it back: intensity
far *left* of the ridge, so the GPU idles waiting on memory traffic, nowhere near its compute ceiling.
Second, **each op is its own [[cuda-kernel]] launch**, and every launch carries fixed overhead plus a
mandatory round-trip: the layer reads its input tensor from GPU memory and writes its output tensor
back, so the next layer can read it again. A ten-layer chain writes and re-reads nine intermediate
tensors it never needed to materialize. On top of both, **FP32 weights move 2–4× more bytes** than a
lower-precision copy would. TensorRT's three optimizations attack exactly these: fusion kills the
round-trips, precision cuts the bytes, auto-tuning picks the fastest kernel for what remains.

### Optimization 1 — layer/tensor fusion (fewer kernels, no round-trips)

TensorRT scans the network for chains of layers that can be computed **together** and fuses them into a
**single** [[cuda-kernel]]. The canonical case is *convolution → bias → activation*: instead of three
kernels each reading and writing the full feature-map tensor, one fused kernel computes the
convolution and, **while each output element is still in registers**, adds the bias and applies the
activation *before* the single write-back to GPU memory.

Why this wins is precisely the [[roofline-model]] lesson about fusion: the bias and activation are
memory-bound on their own, but fused they add arithmetic to a byte that has *already been loaded* and
would have been written anyway — one load and one store now carry three layers' worth of work. The
per-element arithmetic intensity rises, sliding the operation **rightward toward the ridge**, and the
eliminated intermediate tensors are pure removed traffic. Fewer kernels also means fewer launches, so
the fixed per-launch overhead shrinks. Fusion changes *when and where* values live (registers vs. GPU
memory), never *what* is computed — the result is bit-for-bit the same forward pass.

### Optimization 2 — precision reduction and INT8 calibration ([[quantization]])

TensorRT can store and compute the network in **FP16** or **INT8** instead of FP32. This is
[[quantization]]: an INT8 value is a small integer code times a shared **scale** `s`, with recovered
value `code × s` and a bounded rounding error `≤ s/2`. The payoff is bytes moved — an INT8 weight is
**a quarter** the size of FP32 — which directly relieves the memory-bound layers above (fewer bytes
per element ⇒ higher intensity on the same [[roofline-model]] slope), and low-precision matrix math
also runs faster on the GPU's dedicated units.

The danger is accuracy. INT8's grid is coarse, and (from [[quantization]]) the error grows as the
scale `s` grows, so a badly chosen `s` — one set by a rare outlier activation — coarsens every normal
value. TensorRT's fix is **calibration**: it runs the FP32 model over a small *representative* sample
of real inputs, records the actual range of each layer's activations, and chooses each `s` to
**minimize the mismatch** between the FP32 and INT8 value distributions (it compares the two
distributions with a statistical distance and picks the scale that makes the INT8 histogram best match
the FP32 one). Because the scales are fit to observed data rather than worst-case bounds, INT8
inference keeps almost all the accuracy **without retraining** — calibration is a measurement pass,
not a training pass.

### Optimization 3 — kernel auto-tuning (empirical, hardware-specific)

For a single layer there is no one "best" [[cuda-kernel]] — there are *many* valid implementations
(different tile sizes, memory layouts, algorithms), and which is fastest depends on the exact tensor
shapes **and** the specific GPU (its number of compute units, its memory bandwidth, its
supported precisions). TensorRT does not guess. At build time it **benchmarks the candidate kernels
for each layer on the actual target GPU** and keeps the fastest — NVIDIA calls each candidate a
*tactic*. The engine therefore contains, per layer, an empirically-chosen kernel tailored to this
hardware and these shapes. This is why the build is **hardware-specific and slow**: it is running real
timing experiments, not just translating code.

### The engine build is ahead-of-time — with AOT's tradeoff

All three optimizations happen **once**, at build time, and are frozen into a serialized **engine**
file. This is textbook [[jit-vs-aot-compilation|AOT compilation]]: the expensive work (fusion
decisions, calibration, kernel benchmarking) is paid before deployment, so at run time there is *no*
compile pause and *no* per-call optimization — the engine just executes, warm from the first inference
to the millionth. And it inherits AOT's rigidity exactly as that node describes: the engine is
specialized to one GPU architecture and a fixed range of input shapes, so it is **not portable** — a
different GPU generation, or shapes outside what it was built for, requires **rebuilding** the engine.
TensorRT trades build-time cost and flexibility for warm-up-free, hardware-matched inference speed.

### Worked instance — a conv → bias → ReLU block, fused and quantized

Take one feature-map tensor of **M = 1,000,000** elements flowing through *conv → bias → ReLU*, on a
chip whose [[roofline-model]] ridge sits near 33 FLOP/byte.

**Unfused, FP32 (4 bytes/element).** The bias and ReLU are separate memory-bound kernels:

- Bias: read M elements (4 MB) + write M (4 MB) = **8 MB** moved, doing ~M cheap adds.
- ReLU: read 4 MB + write 4 MB = **8 MB** moved, doing ~M max operations.

That is **16 MB** of memory traffic for ~2M FLOPs — intensity `≈ 2×10⁶ / 16×10⁶ = 0.125` FLOP/byte,
deep on the memory-bound slope: the ceiling is `bandwidth × 0.125`, well under 1% of peak compute. The
convolution's output tensor was written to GPU memory only to be read straight back twice.

**Fused, FP32.** Fold bias and ReLU into the convolution's epilogue: each conv output element, already
in a register, gets the bias added and the ReLU applied *before* its single write-back. The two extra
kernels — and their **16 MB** of round-trip traffic — **disappear entirely**; the bias/ReLU arithmetic
now costs zero additional bytes. Same numerical result, the memory-bound tail eliminated.

**Fused + INT8 (1 byte/element).** Now quantize. Every byte moved by the surviving loads/stores and by
the convolution's own weights shrinks **4×** (4 bytes → 1), so the convolution — the compute-heavy part
— both moves a quarter of the bytes and runs its matrix math in fast low precision, while calibration
keeps the output within the `≤ s/2` error bound so accuracy holds. Stacking the two effects: fusion
removed the memory-bound round-trips, and INT8 quartered the bytes of what remained — the same block
that idled the GPU now runs near its compute ceiling. That compounding — restructure to raise
intensity, then shrink the bytes — is what turns a trained model into a fast TensorRT engine, with no
change to what the network computes.

## Prerequisites

- [[jit-vs-aot-compilation]]
- [[cuda-kernel]]
- [[roofline-model]]
- [[quantization]]
- [[neural-network]]

## Sources

- NVIDIA TensorRT — developer.nvidia.com/tensorrt (inference optimizer + runtime: layer/tensor
  fusion, FP16/INT8 precision calibration, kernel auto-tuning / tactic selection, and the serialized
  hardware-specific engine build).
