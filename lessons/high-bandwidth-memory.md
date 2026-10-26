# High-Bandwidth Memory

## Meaning

HBM is a main-memory technology that stacks dynamic-memory dies and connects them through a wide interface near an accelerator. It is a physical way to provide substantial storage capacity and aggregate data movement, not a guarantee that every memory access becomes quick. It occupies a different tier from registers and on-chip caches in the [[memory-hierarchy]].

## Mechanism

Stacking increases storage density. Many connections provide transfer width. The bandwidth arithmetic is interface lanes multiplied by bits per second per lane, converted to bytes per second. Several stacks can contribute capacity and transfer paths, but the implemented memory controllers, packaging and workload determine what is usable.

Keep three quantities separate. Capacity is bytes that fit. Bandwidth is bytes transferred per second. Latency is the wait for a particular access. Independent streaming accesses can keep many paths busy; a dependent chain can wait on each access despite high aggregate bandwidth. A cache hit avoids the main-memory transfer and must not be confused with measured HBM traffic.

## One example

Assume four hypothetical stacks each hold 16 GB and sustain 0.5 TB/s. Capacity totals 64 GB and streaming bandwidth totals 2 TB/s. Reading 8 GB once takes at least 8/2000 seconds, or 4 ms, at that measured rate. That is a transfer floor, not an end-to-end latency prediction. A 70 GB working set still does not fit. A smaller working set can still perform poorly if accesses are serial, computation dominates or the service is queued.

## Check your understanding

Would doubling capacity necessarily double token throughput? No. First determine whether capacity, bandwidth, access dependencies or a non-memory stage limits this workload. Check the precise board variant and measure representative sustained traffic rather than borrowing a product headline.
