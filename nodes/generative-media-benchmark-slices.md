---
id: generative-media-benchmark-slices
title: Generative-Media Benchmark Slices
summary: Generative-media benchmark slices separate prompt adherence, visual quality, temporal consistency, latency, and cost so one aggregate score cannot hide distinct failure modes.
type: concept
tags: [ml/evaluation]
prereqs: [image-preference-modeling, measurement]
sources: [https://arxiv.org/abs/2310.11513, https://arxiv.org/abs/2311.17982]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Generative-Media Benchmark Slices

## Summary

An image or video model can look impressive in one prompt family and fail at counting, spatial relations, text rendering, editing, or temporal continuity. **Benchmark slices** make those separate capabilities visible before any overall ranking is computed.

## Grounded explanation

Construct prompts with controlled attributes and observable success criteria. GenEval's object-focused image evaluation illustrates compositional slices such as object count and relation; VBench separates dimensions of video quality. These are tests of defined properties, not a complete measure of human preference. [[image-preference-modeling]] captures a different question: which output people favor under a prompt. Keep adherence, aesthetics, artifacts, diversity, and safety as separate measurements when they matter.

For video, include temporal consistency and motion behavior in addition to frame appearance. Hold seed, sampling budget, resolution, aspect ratio, and postprocessing fixed across models; otherwise a quality comparison may be a compute comparison. Record failures and censored generations rather than displaying only selected successes. Measure generation time and billable cost alongside output quality through [[measurement]].

Use blinded raters for subjective dimensions, deterministic checks where possible, and uncertainty intervals for small slices. Audit whether automated judges overreward familiar styles or miss rare errors. A public benchmark board may be useful discovery evidence, but without its exact prompts, sampling, judge, and filtering rules it cannot establish a general model ranking.

## Prerequisites

- [[image-preference-modeling]]
- [[measurement]]

## Sources

- [GenEval](https://arxiv.org/abs/2310.11513): object-focused text-to-image alignment evaluation.
- [VBench](https://arxiv.org/abs/2311.17982): multidimensional video-generation benchmark design.
