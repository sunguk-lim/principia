---
id: cpu-vs-gpu
title: CPU vs GPU
summary: CPU and GPU execution designs make different latency, throughput and concurrency trade-offs; logical work count, resident state and physical arithmetic lanes must not be conflated.
type: concept
tags: [gpu]
prereqs: [memory-hierarchy]
sources: [https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html, https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html]
status: explained
created: 2026-06-23
updated: 2026-10-27
---

# CPU vs GPU

## Meaning

CPUs and GPUs execute programs but distribute hardware resources differently. CPUs emphasize low latency for a small number of flexible instruction streams; GPUs emphasize aggregate throughput across many regular, parallel work items. Both depend on the [[memory-hierarchy]], and neither is universally faster. These are design tendencies, not absolute rules about every processor or program.

## Mechanism

A CPU core can run an independent instruction stream and uses mechanisms such as caches, branch prediction and out-of-order execution to reduce stalls. CPUs can also execute vector instructions and run many threads; calling them simply sequential loses an important part of the comparison.

A GPU devotes substantial resources to arithmetic and to keeping many execution contexts available. When one context waits, the scheduler can choose another ready context. This hides some latency only if enough independent work and resident resources are available. Dependencies, unavailable data, synchronization or exhausted storage can leave no useful work ready. GPUs also have caches: tolerating memory latency and avoiding traffic are complementary, not exclusive strategies.

An advertised CUDA-core count is not a count of CPU-like independent processors. Physical arithmetic lanes, thread scheduling resources and software execution contexts are different objects. Their counts have no universal performance conversion such as one lane being a fixed number of times weaker than one CPU core. Instructions, precision, clock, utilization and data movement determine the comparison.

The key distinction is **launched versus resident work**. An application can describe a million logical thread executions without all million being simultaneously loaded onto the chip. Only a bounded subset is resident at a time; registers, shared storage and device limits constrain that subset. Remaining work executes as resources become available. A logical thread is not a permanently assigned physical lane.

## Worked example

Add two arrays with one million elements each, storing a third array of results. If each element uses four bytes, the useful streaming traffic is two reads and one write: 1,000,000 * (4+4+4) = 12,000,000 bytes, or 12 MB in decimal units. This excludes extra traffic, caching effects and allocation.

For a hypothetical path sustaining 120 GB/s, moving those 12 MB has a floor of 12,000,000 / 120,000,000,000 seconds = 100 microseconds. At a hypothetical 1.2 TB/s it is 10 microseconds. These are transfer floors using assumed achieved bandwidths, not CPU/GPU benchmark promises. Launch overhead, host-to-device copies and synchronization can reverse the apparent advantage for a small job. Keeping inputs and outputs on the device can change that balance.

A CPU implementation can divide elements among workers and vectorize each worker's loop. A GPU implementation can describe one logical thread per element and execute those threads in resident subsets. Both expose the same independence; their execution resources and movement costs differ. Contrast a single dependent parsing stream, where each next action requires the previous result: more arithmetic lanes alone do not create parallel work. A batch of independent parsing streams would be a different workload.

## Validation and alternatives

Compare the complete path at the same output contract. State input sizes, numeric format, data residency, concurrency and transfer inclusion. Measure rather than infer a speed from core count. Separate warm steady state from setup, and inspect memory traffic and available independent work. Choose CPU, GPU or a split design based on those observations. Offloading every operation can be worse than keeping small control-dependent work on the CPU while larger regular regions execute on the GPU.

## Check your understanding

If a launch describes one million threads, are one million threads resident? No. Logical work, resident execution state and physical lanes are distinct; device resource limits govern residency.

## Prerequisites

- [[memory-hierarchy]]

## Sources

- [NVIDIA CUDA programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html): host/device roles, physical execution resources and scheduling a large grid on bounded hardware.
- [NVIDIA CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html): measured bandwidth, parallel work, transfers and application-level profiling.
