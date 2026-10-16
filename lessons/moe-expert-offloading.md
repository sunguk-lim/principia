# Moe Expert Offloading

## Meaning

Sparse expert activation saves per-token arithmetic but does not eliminate storage for the inactive experts. Offloading places some weights outside GPU memory.

## Mechanism

A router chooses experts; resident weights execute quickly, while cache misses require transfer from host memory. Quantization can shrink transfer bytes but introduces its own quality checks.

## Example

A model may fit across two GPUs only because many experts sit in CPU RAM. Single-request throughput and eight-request throughput can differ sharply when request diversity changes the expert cache hit rate.

## Boundaries and trade-offs

MoE sparsity means few experts run for one token, not that all weights fit in GPU memory. Offloading exploits reuse: popular experts stay resident while cold experts wait in host RAM. A placement algorithm predicts which weights will be needed; a miss exposes interconnect cost. Different prompts and concurrent users can activate different experts, so a favorable single-stream benchmark may not represent a service.

## Validation

Keep the same model and tasks when comparing all-GPU, offloaded, and quantized variants. Trace which experts are chosen, where they reside, transfer volume, GPU stalls, and cache eviction. Measure prefill separately from decode and include p95 at realistic concurrency. Test cold starts and long requests as well as warmed steady state. Report host RAM, GPU memory, power, and operating cost; reducing one memory term can introduce a latency or quality bill elsewhere.

## Understanding check

What measurements would show that host-to-device expert transfer, rather than GPU compute, is the serving bottleneck?
