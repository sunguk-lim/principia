---
id: kernel-autotuning
title: Kernel Autotuning
summary: Kernel autotuning benchmarks valid implementation configurations for a keyed workload and retains a measured choice while accounting for search cost and correctness.
type: concept
tags: [gpu/programming-models]
prereqs: [cuda-kernel, measurement, memory-hierarchy]
sources: [https://triton-lang.org/main/python-api/generated/triton.autotune.html]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Kernel Autotuning

## Meaning

Kernel autotuning chooses among implementations of the same operation using measured performance on the intended workload. It searches configuration, not model quality: tile sizes, worker counts and staging choices are examples. A faster configuration is eligible only when it still computes the required function.

## Mechanism

A [[cuda-kernel]] configuration determines how work and data movement are organized on the device. The [[memory-hierarchy]] explains why changing reuse and resource occupancy can alter speed. Define a search space, exclude invalid configurations, warm up candidates, time them with device-completion-aware [[measurement]], then retain a winner for a declared key such as shape, dtype and device family. Versions and layout constraints can also invalidate a cached choice.

Tuning executes candidate kernels repeatedly. A kernel that increments output will corrupt its benchmark state unless the tuner resets or restores affected inputs between trials. Triton's autotune API explicitly exposes reset and restore controls. Those controls do not replace correctness tests for every eligible candidate.

## Worked example

For one shape, configuration A takes 20 microseconds per call and B takes 14. A tuning search costs 30 milliseconds more than using the default. Each later B call saves six microseconds, so 30,000/6=5,000 calls amortize the search in this simplified accounting. If the workload runs only 200 times, the six-microsecond improvement saves 1.2 milliseconds and does not recover the search cost. Another shape may favor A.

## Boundaries and validation

Measure cold compile/search time separately from cached steady-state execution. Validate every candidate's output against a reference over representative values and numerical tolerances; test side effects, strides, edge tiles and resource limits. Report variation rather than selecting a winner from one noisy timing. A prebuilt runtime may already dispatch among specialized kernels; local tuning is not automatically better. Results for one chip or shape do not establish a universal engine ranking.

## Prerequisites

- [[cuda-kernel]]
- [[measurement]]
- [[memory-hierarchy]]

## Sources

- <https://triton-lang.org/main/python-api/generated/triton.autotune.html>
