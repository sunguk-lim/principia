# Memory-Level Parallelism

## Meaning

Memory-level parallelism is the amount of independent memory work that can be outstanding together. It connects access latency with achieved throughput: a memory interface can have high bandwidth yet remain underused when a program exposes too few independent requests. This is a distinct property from storing fewer bytes or using a faster cache.

## Mechanism

[[memory-hierarchy]] separates where accesses are served and their latency, traffic and bandwidth. Suppose an idealized request transfers b bytes, occupies a request slot for L seconds, and at most N independent requests can overlap. Sustaining completion of those N requests every L seconds would provide N×b/L bytes per second. If the interface bandwidth ceiling is B, an idealized throughput envelope is min(B, N×b/L).

This is a counting model with stated assumptions, not a prediction of a particular device. Requests can merge, split into transactions, hit different cache levels or contend for queues. Their latencies need not be equal. A dependent chain that computes each next address from the preceding result may expose only one request at a time even with a large dataset. Independent streams of work can expose several.

On a GPU, resident warps provide potential work, but only ready instructions can issue and only independent loads can increase outstanding requests. A warp stalled on a result does not become ready because another resident warp exists. Nsight distinguishes active, eligible and issued warps; inspect actual issue and memory traffic instead of treating occupancy as achieved memory parallelism.

## One example

Assume fictional 64-byte requests, 200-nanosecond slot occupancy and a 32-GB/s interface ceiling, using decimal units. One independent request yields at most 64/(200×10^-9)=0.32 GB/s in this model. Sixteen provide at most 5.12 GB/s; one hundred reach the 32-GB/s ceiling. Doubling overlap from one hundred to two hundred cannot double that fixed ceiling, and additional queueing can increase individual latency.

These are synthetic values. They explain why doubling stored KV groups can have little timing effect in one regime and a larger effect in another: fewer transferred bytes, number of independent requests, reuse and kernel scheduling all change the result. They do not prove that any particular group count is optimal or that one attention design preserves quality.

## Check your understanding

Can a device advertise high bandwidth while one dependent load chain runs slowly? Yes. Available aggregate capacity does not remove each dependency's access latency.
