---
id: python-profiling
title: Python Profiling
summary: Python profiling measures where a representative program spends execution time or allocations so optimization targets observed bottlenecks rather than guesses.
type: concept
tags: [languages/python]
prereqs: [interpreter, measurement]
sources: [https://docs.python.org/3/library/profile.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Profiling

## Summary

**Python profiling** is a runtime [[measurement]] that records execution statistics such as call counts, self time, and cumulative time to locate bottlenecks before changing code.

## Grounded explanation

Python's deterministic profilers observe function calls and returns. In `cProfile` output, `tottime` is time in a function excluding callees, while `cumtime` includes subcalls. A function with small self time but large cumulative time delegates expensive work; a function with high self time is expensive directly.

The standard documentation recommends `cProfile` for most users because its C implementation has reasonable overhead. The pure-Python `profile` module is easier to extend but adds more overhead. Both perturb execution, and their overhead does not affect Python and C-level work equally.

Profiling and benchmarking answer different questions. A profile attributes one workload's cost; a benchmark estimates comparative elapsed performance under controlled repeated conditions. Use the standard `timeit` facility or an equivalent benchmark for before-and-after speed claims rather than treating profiler totals as precise benchmark results.

Start with a representative end-to-end workload and a user-visible target such as latency or throughput. Sort by cumulative and self time, inspect callers and callees, then change one demonstrated bottleneck. Check semantic equivalence with tests and remeasure the same workload. Improvements can shift cost to memory, startup, I/O, serialization, or another process, so retain end-to-end measurements and resource limits.

Avoid folklore such as replacing every loop or local variable pattern. Algorithm, data shape, library boundary, interpreter version, warm-up, and input distribution often dominate micro-syntax. Report environment, dataset, repetitions, variance, and both absolute and relative changes.

## Prerequisites

- [[interpreter]]
- [[measurement]]

## Sources

- [Python documentation, “The Python Profilers”](https://docs.python.org/3/library/profile.html): defines deterministic profiling, `cProfile`, `profile`, `pstats`, self and cumulative time, and the distinction from benchmarking.
