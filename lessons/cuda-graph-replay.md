# Cuda Graph Replay

## Meaning

CUDA graph replay reduces repeated CPU work submitting a compatible GPU operation sequence. It does not make the operations themselves faster.

## Mechanism

Capture a warmed, stable execution path, then replay it with stable buffers and compatible shapes. Multiple graph buckets improve coverage but require memory and startup work; eager fallback handles incompatible shapes.

## Example

A decode step with many tiny kernels has visible GPU idle gaps between CPU launches. Replaying a captured graph can reduce those gaps, while a long compute-bound prefill may barely change.

## Boundaries and trade-offs

A graph is an execution packaging mechanism. The CPU can submit a captured operation sequence more cheaply, but the GPU still executes kernels and moves data. This means its benefit is conditional on the fraction of time spent waiting for launches. Capture can fail or produce incorrect assumptions if buffers change address, operations allocate unexpectedly, or control flow depends on live data. Warm-up and replay correctness checks are part of deployment.

## Validation

Profile a representative arrival trace, not a single ideal batch. Label host enqueue periods, GPU idle gaps, kernel execution, queueing, and synchronization. Then compare eager and replay under equal shapes, precision, and quality. Count which requests use a captured bucket, which are padded, and which fall back. Extra buckets improve coverage but reserve memory; padding can waste compute. If p95 latency improves only on a benchmark shape, the production claim is not established.

## Understanding check

Which profiler evidence distinguishes launch-bound decode from kernel-bound decode, and what costs grow when you capture more batch shapes?
