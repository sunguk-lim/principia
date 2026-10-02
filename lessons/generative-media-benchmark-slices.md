# Generative-Media Benchmark Slices

## Meaning

An image or video model can look impressive in one prompt family and fail at counting, spatial relations, text rendering, editing, or temporal continuity. **Benchmark slices** make those separate capabilities visible before any overall ranking is computed.

## Mechanism

Construct prompts with controlled attributes and observable success criteria. GenEval's object-focused image evaluation illustrates compositional slices such as object count and relation; VBench separates dimensions of video quality. These are tests of defined properties, not a complete measure of human preference. [[image-preference-modeling]] captures a different question: which output people favor under a prompt. Keep adherence, aesthetics, artifacts, diversity, and safety as separate measurements when they matter.

For video, include temporal consistency and motion behavior in addition to frame appearance. Hold seed, sampling budget, resolution, aspect ratio, and postprocessing fixed across models; otherwise a quality comparison may be a compute comparison. Record failures and censored generations rather than displaying only selected successes. Measure generation time and billable cost alongside output quality through [[measurement]].

## Worked example

Two image generators tie on an overall score. One fails counting prompts; the other makes attractive images but misses spatial relations. The tie hides different application risks. Video adds motion and temporal continuity, so a frame-only image score cannot substitute for a video evaluation.

**Understanding check:** Which benchmark controls would prevent a larger sampling budget from masquerading as a better model?
