---
id: little-law
title: "Little's Law"
summary: "Little's law relates long-run mean occupancy to effective throughput and mean time inside the same system boundary."
type: concept
tags: [distributed-systems/performance]
prereqs: [queue, expectation, measurement]
sources: [https://web.mit.edu/urban_or_book/www/book/chapter4/4.4.html]
status: explained
created: 2026-11-07
updated: 2026-11-07
---

# Little's Law

## Meaning

Little's law is an accounting relation between how many items occupy a system and how long they stay. It applies to a waiting [[queue]], a complete service system or another explicitly bounded flow. It does not require Poisson arrivals or a particular order of service.

## Mechanism

Choose one boundary and one item population. Let L be the long-run time-average number inside, lambda the effective rate at which items enter that boundary, and W the mean time an entering item spends inside. When these averages exist with suitable flow balance and negligible long-window boundary contributions, L=lambda W. Use the same accepted population for rate and residence time; rejected arrivals that never enter do not count as throughput inside.

Why? Each item contributes one unit to occupancy throughout its residence interval. Adding those interval lengths gives the area under the occupancy-versus-time curve. Over a sufficiently long observation window, divide that area by window duration: occupancy equals completed/entered-item rate times mean residence time, after handling unfinished items at the edges. This is a sample-path accounting argument; a steady-state [[expectation]] version uses the corresponding expected quantities under appropriate assumptions.

## One example

An invented service accepts 40 jobs per second and mean end-to-end residence is .3 seconds. Mean occupancy is 40*.3=12 jobs, including waiting and execution. If the mean queue-only wait is .2 seconds, that boundary has mean occupancy 8, not 12. If 50 attempted jobs arrive each second but 10 are rejected before admission, using 50 with the accepted jobs' residence time would incorrectly predict 15. Boundary and population mismatch, not algebra, caused that error.

## Check your understanding

Does an average of 12 jobs mean the queue never exceeds 12? No. The law relates averages, not capacity, percentiles or a waiting-time distribution. [[measurement]] must use aligned windows and units and account for retries, drops, cancellations and work already present. Growing unbounded backlog or censored long jobs can invalidate a naive finite-window calculation. The relation can check instrument consistency and capacity estimates; it does not by itself determine waiting from only arrival and service rates.

## Prerequisites

- [[queue]]
- [[expectation]]
- [[measurement]]

## Sources

- <https://web.mit.edu/urban_or_book/www/book/chapter4/4.4.html>
