# CPU vs GPU

## Meaning

CPU and GPU designs make different latency and throughput trade-offs. A CPU emphasizes flexible independent instruction streams. A GPU emphasizes regular work with enough parallelism to keep many arithmetic resources busy. Both depend on the [[memory-hierarchy]]; neither is universally faster.

## Mechanism

A GPU scheduler can choose ready work while other work waits, but only when independent work and execution resources are available. It cannot hide every dependency. GPUs also use caches, and CPUs also use vector operations and many threads, so avoid the false split of a purely sequential CPU versus a GPU that never avoids memory traffic.

Separate logical work from physical execution. A launch can describe a million logical threads while only a bounded subset is resident. The rest run as resources become free. A logical thread is not one permanently assigned arithmetic lane. Advertised GPU-core counts also cannot be converted into CPU-core performance using a fixed multiplier.

## One example

Adding two one-million-element arrays into a third, with four bytes per element, requires 12 MB of useful streaming reads and writes. Assume one path sustains 120 GB/s: the transfer floor is 100 microseconds. At an assumed 1.2 TB/s it is 10 microseconds. These are arithmetic floors, not hardware benchmark results. Extra traffic, launch costs, synchronization and host/device copies can change the complete result. A small operation may favor remaining where its data already lives.

## Check your understanding

Does a million-thread launch mean a million simultaneously resident threads? No. Residency is bounded by execution resources and storage. Compare matched complete paths with stated data location and output quality, rather than inferring speed from thread or core count.
