---
id: load-testing
title: Load Testing
summary: "Load testing drives a service with controlled synthetic traffic (e.g. concurrent HTTP clients) while measuring throughput and latency percentiles, to find how performance degrades as load rises — where the saturation knee is, and whether the service meets its tail-latency targets at the load it must survive."
type: concept
tags: [networking/performance]
prereqs: [http, latency-percentile]
sources: ["https://grafana.com/docs/k6/latest/testing-guides/test-types/", "Schroeder et al., 'Open Versus Closed: A Cautionary Tale', NSDI 2006"]
status: explained
created: 2026-07-14
updated: 2026-07-14
---

# Load Testing

## Summary

**Load testing** is measuring a service's performance *under controlled synthetic demand*: instead
of waiting for real users, a test program plays the part of many concurrent clients — issuing
[[http]] requests against the real system — while recording two curves as the load rises:
**throughput** (requests completed per second) and **latency** (summarized as
[[latency-percentile]]s, p95/p99). The point is to answer, *before production does*, the questions
a single functional test cannot: how many requests per second can this service sustain? at what
load does latency blow up? does it meet "p99 < 300 ms" at peak traffic? does it recover after a
spike? A load test passes or fails on explicit **thresholds** over those measurements — it is a
performance experiment with pass/fail criteria, not a benchmark bragging number.

## Grounded explanation

### What it is — a dial for demand, two curves for the answer

A load test has three parts:

1. **A workload** — what one simulated client does: typically a small script of [[http]] requests
   ("log in, fetch the dashboard, post an item"), realistic enough that the server does real work
   (cache hits *and* misses, writes as well as reads).
2. **A load model** — how much demand, applied how: the number of concurrent clients or the request
   arrival rate, shaped over time (constant, ramping, spiking).
3. **Measurements and thresholds** — for every request: did it succeed (the [[http]] status code —
   `2xx` vs `5xx` — is the ground truth), and how long did it take. Aggregated into throughput,
   error rate, and [[latency-percentile]]s, and judged against explicit criteria:
   "error rate < 1% **and** p95 < 500 ms".

Raising the demand dial and re-measuring traces out the service's **load–response curve**, and it
always has the same shape: throughput climbs roughly linearly with offered load while the service
has spare capacity, latency staying flat; then throughput flattens at the service's capacity — the
**saturation knee** — and beyond it *latency* absorbs all further demand, growing without bound as
unserved requests pile up in an ever-growing backlog while completions per second stay pinned at capacity. The knee
is the single most valuable number a load test produces: capacity is the throughput plateau, and
the safe operating region is the load range where the tail percentiles still meet their targets —
**the tail degrades first**, long before the average moves, which is why the measurements are
percentiles ([[latency-percentile]]) and never means.

### Two load models — closed vs open (and why the difference bites)

*How* the load is generated changes what you measure:

- **Closed model** — a fixed pool of $N$ virtual users, each looping: send a request, wait for the
  response, think, repeat. Natural and safe, **but self-throttling**: when the server slows down,
  every user is stuck waiting, so the offered rate *drops* exactly when the server is struggling —
  the test involuntarily backs off, and the measured tail is kinder than reality. This is the
  load-generation form of the coordinated-omission pitfall noted in [[latency-percentile]].
- **Open model** — requests *arrive* at a set rate (e.g. 100/s) regardless of whether earlier ones
  have finished, the way independent real-world users actually behave (a new visitor doesn't know
  the server is slow). Under an open model a saturated server faces an ever-growing backlog — which
  is precisely the brutal honesty you want when the question is "what happens at 2× peak?".

Rule of thumb: closed for interactive-session realism, open for capacity and tail-latency
questions; a good test tool must offer both.

### The standard test shapes

One workload, different load-over-time profiles, different questions:

| shape | profile | question it answers |
|---|---|---|
| **smoke** | minimal load, briefly | does the script and system work at all? |
| **load (average)** | ramp to expected traffic, hold | thresholds met at normal load? |
| **stress** | ramp well past expected | where is the knee? what breaks first, and how? |
| **spike** | jump to extreme, drop back | does it survive — and *recover*? |
| **soak** | moderate load, hours | slow leaks: memory growth, connection exhaustion, drift |

### Worked instance — finding a knee

An [[http]] API is load-tested with an open model at increasing arrival rates, 5 minutes each:

| offered load | throughput | p50 | p99 | errors |
|---|---|---|---|---|
| 100 req/s | 100 req/s | 18 ms | 60 ms | 0% |
| 400 req/s | 400 req/s | 19 ms | 85 ms | 0% |
| 800 req/s | 795 req/s | 24 ms | **480 ms** | 0.1% |
| 1200 req/s | **810 req/s** | 310 ms | 4.1 s | 6% |

Reading it: up to 400 req/s the service is comfortable — throughput tracks offered load and the
tail is flat. At 800 req/s throughput still *looks* fine (795 ≈ 800) but the **p99 has jumped 5×**
— the tail is the early-warning signal; p50 has barely moved. At 1200 req/s the knee is behind us:
completions are pinned at ~810/s (the capacity), the unserved 390/s pile up, waiting time dominates
(p50 itself is now 310 ms), and timeouts surface as `5xx` errors. Against a threshold of
"p99 < 300 ms, errors < 1%" this service passes at 400, fails at 800 — so its safe capacity is
somewhere between, found by exactly this bisection. A closed-model test of the same server would
have reported a gentler 1200-req/s row — its stuck users would simply have offered less load.

## Prerequisites

- [[http]] — the protocol of the synthetic traffic, and the status codes that define success/failure
  per request
- [[latency-percentile]] — the measurement vocabulary: thresholds are stated on the tail, which
  degrades first as load approaches capacity

## Sources

- Grafana k6 docs, "Load test types" — https://grafana.com/docs/k6/latest/testing-guides/test-types/
- Schroeder, Wierman & Harchol-Balter, "Open Versus Closed: A Cautionary Tale," NSDI 2006
