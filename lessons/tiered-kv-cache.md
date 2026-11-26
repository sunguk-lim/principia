# Tiered KV Cache

## Meaning

A tiered KV cache retains reusable attention state in larger, slower memory when GPU space is scarce. A later compatible request can restore it instead of recomputing its prefix. The useful trade is capacity and reuse against movement cost, not simply a higher hit rate.

## Mechanism

GPU memory holds active state; host RAM or storage can retain colder blocks. On reuse, the system verifies compatibility and ownership, locates the state and transfers it before consumption. A cache index can be stale, and concurrent traffic shares transfer paths. Layerwise prefetch helps only when state arrives before its read and staging buffers remain valid.

Tiering does not require racing every backend. Concurrent lookup may shorten a slow miss path but can add redundant traffic and cancellation work. LMCache documents an L1 reservation followed by L2 handling of remaining keys; check the actual implementation before attributing an all-tier race to it.

## One example

For a hypothetical 2 GiB prefix and an effective 8 GiB/s path, transfer alone takes 250 ms. Adding 30 ms of setup and queueing gives 280 ms. If recomputation costs 180 ms, restoring that hit loses. At 32 GiB/s, transfer takes 62.5 ms and total restoration 92.5 ms, which can win under the same assumptions.

Four independent storage paths do not evade a shared bottleneck. Four 128 MiB blocks total 512 MiB; a common 4 GiB/s link needs at least 125 ms, even when each device can read its own block faster. Measure complete restoration rather than summing device peaks.

## Check your understanding

Can every cached block be evicted without affecting correctness? No. An unreferenced reusable prefix can be recomputed later, but an active request still needs its required state before the next read. Preserve pin/release ownership and test cancellation, eviction and worker loss. Report token reuse, transfer latency, memory pressure and task quality separately. A hit is an opportunity to avoid work, not proof of lower tail latency.
