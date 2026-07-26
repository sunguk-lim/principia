---
id: latency-percentile
title: Latency Percentiles (Tail Latency)
summary: "Latency percentiles (p50/p95/p99) summarize a service's response-time distribution by reading its empirical CDF in reverse: pN is the time under which N% of requests completed — reporting the tail (p95 and up) instead of the average, because the mean hides the slow requests users actually feel."
type: concept
tags: [networking/performance]
prereqs: [cumulative-distribution-function]
sources: ["Dean & Barroso, 'The Tail at Scale', CACM 2013", "G. Tene, 'How NOT to Measure Latency'"]
status: explained
created: 2026-07-14
updated: 2026-07-14
---

# Latency Percentiles (Tail Latency)

## Summary

Measure the response time of every request a service handles and you get not one number but a
**distribution**. A **latency percentile** summarizes it: **pN** (the *N*-th percentile) is the
time under which *N*% of requests completed — p50 = 20 ms means half the requests finished within
20 ms; p99 = 800 ms means 1 in 100 took longer than 800 ms. Formally, pN is the
[[cumulative-distribution-function]] read *in reverse* — the quantile $F^{-1}(N/100)$. The
practical discipline built on this: judge a service by its **tail** (p95, p99, p99.9 — the slowest
few percent), not its average, because latency distributions are lopsided — a long right tail of
slow stragglers that the mean smooths over and the median never sees, yet real users hit constantly.

## Grounded explanation

### What it is — the empirical CDF of response times, read backwards

Symbols first:

| symbol | type | meaning |
|---|---|---|
| $X$ | 🟦 scalar random quantity | the latency of one request |
| $F(x)$ | 🟦 scalar in $[0,1]$ | the [[cumulative-distribution-function]]: fraction of requests with latency $\le x$ |
| $q$ | 🟦 scalar in $[0,1]$ | a cumulative-probability level (0.50, 0.95, 0.99) |
| $p_{100q}$ | 🟦 scalar (a time) | the $q$-quantile: the smallest $x$ with $F(x) \ge q$ |

The [[cumulative-distribution-function]] answers "*given a time $x$, what fraction finished by
then?*". A percentile asks the **reverse**: "*given a fraction $q$, by what time had that fraction
finished?*"

$$ p_{100q} = F^{-1}(q) = \min\{\, x : F(x) \ge q \,\} $$

In practice $F$ is *empirical*: sort the $n$ measured latencies ascending, and pN is the value
$\lceil n \cdot N/100 \rceil$ positions in. No model is assumed — the data is the distribution.

### Why the tail, not the mean

Latency distributions are **skewed right**: most requests are fast and tightly clustered, but a
small fraction — a cache miss, a stall in the server, a retransmit — take 10–100× longer. Two
consequences:

- **The mean lies toward the fast side's crowd but is dragged by the stragglers** — it lands on a
  value that describes *neither* group, and a single 10-second outlier moves it while leaving every
  percentile below p99 untouched (percentiles are robust; the mean is not).
- **The median (p50) is honest about the typical request but silent about the worst.** "p50 =
  20 ms" is compatible with a p99 of 25 ms (a tight service) or 4 s (a disaster). Users experience
  the difference vividly; the median cannot express it.

So service-level targets are stated as tail percentiles — "p99 < 300 ms" — which pin down exactly
the region the mean and median ignore.

**Tail amplification under fan-out.** The tail matters *more* the bigger the system. If one page
load fans out to 100 backend calls and each is slow (worse than its own p99) with probability just
0.01, the page is only fast when *all 100* are fast: $0.99^{100} \approx 0.366$. Almost **two-thirds
of page loads** now experience at least one p99-tail backend call — a 1-in-100 event per call has
become the *common case* per page. This is why large systems obsess over p99 and p99.9: user-facing
latency is governed by the slowest of many parallel parts.

### Worked instance — ten requests, by hand

Ten measured latencies (ms), already sorted:

```
12  14  15  15  16  18  21  25  90  600
```

- **p50**: position $\lceil 10 \times 0.50 \rceil = 5$ → **16 ms**. Half the requests finished
  within 16 ms.
- **p90**: position $\lceil 10 \times 0.90 \rceil = 9$ → **90 ms**.
- **p99**: position $\lceil 10 \times 0.99 \rceil = 10$ → **600 ms** (with only 10 samples, the
  maximum — tail percentiles need many samples to be trustworthy).
- **mean**: $826 / 10 = $ **82.6 ms** — *five times* the median, describing no actual request: nine
  were far faster, one far slower. The two tail requests (90, 600) are exactly what p50 hides and
  the mean smears.

Read the same numbers as the empirical [[cumulative-distribution-function]]: $F(16) = 0.5$,
$F(90) = 0.9$, $F(600) = 1.0$ — each percentile is one point on that staircase, picked out at a
chosen height $q$. (One measurement honesty rule follows from the definition: percentiles are over
*all* requests, so if the measuring client stalls and *sends fewer requests while the server is
slow*, the slow period is under-sampled and the tail reads deceptively fast — the "coordinated
omission" pitfall; a correct measurement keeps issuing requests on schedule and counts the delayed
ones at their full latency.)

## Prerequisites

- [[cumulative-distribution-function]] — a percentile is its inverse: the value at which the
  running total of probability first reaches the chosen level $q$

## Sources

- Jeffrey Dean & Luiz André Barroso, "The Tail at Scale," CACM 56(2), 2013
- G. Tene, "How NOT to Measure Latency" (coordinated omission)
