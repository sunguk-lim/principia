# Cache-Aware Model-Hardware Co-Design

## Meaning

A model is executed repeatedly by a serving system, so attention-state design changes what hardware and scheduling can do efficiently. Co-design chooses these components together rather than ranking models only by parameter count or devices only by peak arithmetic.

## Mechanism

[[grouped-query-attention]] shares KV heads; [[multi-head-latent-attention]] stores a smaller latent with architecture-specific reconstruction. They change representation and may require training or adaptation, unlike simply moving unchanged state to another tier. [[tiered-kv-cache]] changes residency and restore cost, while a [[roofline-model]] helps identify whether traffic or arithmetic is limiting. Compression may free capacity yet add decoding work or unsupported kernels. More concurrent requests may amortize weights but increase active cache memory and latency. Reuse probability and context length determine whether cheaper storage is useful. Joint optimization therefore has quality, capacity, bandwidth, kernel availability and tail-latency constraints, not one universal best cache format.

## One example

Consider a hypothetical serving target with 8 GiB available for active cache after fixed allocations. Architecture A needs 1 GiB per request; B needs 0.5 GiB but adds 2 ms of decode work per iteration. Capacity-only arithmetic permits eight versus sixteen resident requests. It does not prove B is faster: its extra work, batch shape and quality may make it miss a latency target. Now suppose cold prefixes are restored over a path sustaining 4 GiB/s. A single restore has a 0.25-second transfer floor for A versus 0.125 seconds for B, before coordination and contention. Compare these full paths on the same traffic trace, quality bar and hardware, including warm/cold starts, long-context retrieval, actual transfer volume and p95 latency. If B lacks an efficient kernel, changing hardware or retaining A may be the correct choice.

## Check your understanding

Does halving cache bytes imply twice the token rate? No. The bottleneck can move to arithmetic, transfers, scheduling or quality constraints; measure the complete design.
