# Inference Accelerator Comparison

## Meaning

There is no workload-free fastest inference chip. A device and its compiler/runtime form one system, and the winner depends on the model, precision, context lengths, concurrency, and latency target.

## Mechanism

Use the [[roofline-model]] to ask whether the workload is bandwidth- or compute-limited. A batch-one decode can be limited by streaming weights, while a full service batch can reuse them across requests. Check model and kernel coverage, memory for weights and cache, interconnect, and scheduling. A specialized accelerator may win a fixed supported workload but impose compilation or feature constraints.

## One example

Compare the same checkpoint at the same quality target under short and long prompts, batch one and high concurrency. Record first-token and per-token latency, sustained output tokens per second, peak memory, energy, and cost. If one system must change precision or model architecture, disclose that instead of calling it a hardware-only speedup.

## Check your understanding

**Question:** Why does a 10× token-rate demo not rank two accelerators? **Answer:** It may use a different workload, batch, precision, model quality, or measurement boundary.
