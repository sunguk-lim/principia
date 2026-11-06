# Single-Server Queue Stability

## Meaning

A server can be busy without having a stable backlog. Stability asks whether waiting work admits a stationary regime under the model, rather than growing indefinitely. It is a capacity condition, not a latency guarantee or the observation that one short test drained its [[queue]].

## Mechanism

Consider one continuously available worker, an unbounded waiting room, no dropped work, and a work-conserving discipline: the worker does not idle while work waits. Let lambda be the long-run arrival rate in jobs per second. Let S be a job's required service time in seconds, with finite mean m=E[S] supplied by [[expectation]]. Offered work per second is rho=lambda m. One worker supplies one second of service per second.

For the usual stationary independent Poisson-arrival, independent identically distributed service model, rho<1 is the stability condition. Above one, average required work exceeds capacity. At one, there is no positive slack; the ordinary stochastic M/G/1 queue does not have the stable finite-mean waiting regime used by its waiting-time formula. Do not extend that statement to every deterministic, correlated, finite-buffer or time-varying system without its assumptions.

## One example

An invented worker receives six jobs per second, each requiring .12 seconds on average. Offered work is .72 service-seconds per second. At nine arrivals per second it becomes 1.08: on average .08 seconds of unfinished work is added each wall-clock second when the worker is busy. Adding buffer capacity postpones overflow but does not repair the excess workload. Reducing work per job, shedding arrivals or adding suitable service capacity changes the comparison.

## Check your understanding

Does rho=.95 establish an acceptable response time? No. Stable systems can still have long waits and infinite mean waiting under heavy-tailed service distributions. Near-capacity operation leaves little room to absorb bursts. [[measurement]] must distinguish arrivals, actual service demand, worker availability, waiting and dropped jobs. GPU utilization percentages are not automatically this rho: concurrent kernels, batching, memory stalls and shared hardware change what one effective server means. Compare a capacity model with the actual schedule instead of treating one counter as proof of stability.
