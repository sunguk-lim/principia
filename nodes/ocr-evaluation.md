---
id: ocr-evaluation
title: OCR Evaluation
summary: OCR evaluation compares recognized text and document structure against task-matched reference material while separating extraction accuracy from layout, language, and speed claims.
type: concept
tags: [ml/evaluation]
prereqs: [measurement, confusion-matrix]
sources: [https://github.com/datalab-to/surya, https://huggingface.co/datasets/allenai/olmOCR-bench]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# OCR Evaluation

## Summary

**Optical character recognition (OCR) evaluation** asks whether a system recovers the text and structure a downstream task needs. A single benchmark score is not portable across languages, page layouts, handwriting, tables, and mathematical notation. The comparison must define both the reference and the error cost.

## Grounded explanation

An OCR pipeline may detect text regions, order them, transcribe characters, and preserve tables or formulas. Evaluate these stages separately when possible. Character or word error rates compare normalized strings, but their normalization rules matter: punctuation, whitespace, Unicode, and reading order can change the result. Formula transcription needs semantic or render-based checks in addition to raw-string matching. For tables, test cell structure and associations, not only all characters concatenated into one line.

Build held-out slices for the actual deployment distribution: language, script, scan quality, rotation, handwriting, diagrams, tables, and page length. Use adjudicated references and inspect disagreement. A [[confusion-matrix]] or targeted error taxonomy can show symbol substitutions and missed regions hidden by an average score. Measure pages per second and peak memory on specified hardware, batch size, image resolution, and precision; include preprocessing and postprocessing if they are part of the user-facing service.

The Surya project's own repository reports model size, benchmark and throughput results; the olmOCR benchmark publishes a dataset for comparison. Those are useful primary descriptions, not independent verification of a newsletter's ranking or a guarantee on a different corpus. Compare against a simple baseline and at least one competing OCR system under the same data and hardware. Prefer task-level extraction quality over a headline average when the application depends on rare symbols or structured fields.

## Sources

- [Surya repository](https://github.com/datalab-to/surya): primary model description and self-reported evaluation details.
- [olmOCR-bench dataset](https://huggingface.co/datasets/allenai/olmOCR-bench): benchmark task material; suitability depends on the target distribution.
