# Multi-Model Inference Residency

## Meaning

[[multi-model-inference-residency]] decides which models remain loaded on a finite GPU while requests for different models arrive. Routing names a model; residency determines whether its weights and active-request memory are available now. The distinction explains cold starts and eviction.

## Mechanism

Each loaded model consumes weight memory, runtime allocations, and potentially request-specific KV cache and workspace. Start with the [[llm-inference-memory-budget]] for each traffic slice, then ask which allocations can peak together. A shared server may avoid some duplicated process overhead, but it must schedule competing requests and decide whether to load a missing model. Evicting a resident model frees memory but imposes a future reload cost.

A simple least-recently-used rule can thrash if traffic alternates among models whose combined footprint exceeds the device. Pinning high-priority models or reserving capacity can protect latency but leave less room for other requests. Separate instances provide clearer isolation but may waste memory or require a [[load-balancing]] layer. There is no universal winner.

## One example

Models A and B are used every minute; C is used once an hour. Keeping A and B resident while loading C on demand may work if C's occasional cold start is acceptable. If C arrives in bursts that evict A repeatedly, both suffer. Measure the bursty case, not just a warm sequential demo.

## Check your understanding

**Question:** Why is “four requests finished faster” insufficient evidence for a shared server? **Answer:** The paths may differ in model-loading state, concurrency, hardware, or queue time. Compare cold and warm latency, throughput, memory, evictions, failures, and cost under matched conditions.
