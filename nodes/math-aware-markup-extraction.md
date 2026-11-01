---
id: math-aware-markup-extraction
title: Math-Aware Markup Extraction
summary: Math-aware markup extraction preserves semantic equations from web representations before generic text cleanup and validates their survival through later corpus filters.
type: concept
tags: [ml/data]
prereqs: [web-text-extraction]
sources: [https://arxiv.org/html/2310.06786v1, https://katex.org/docs/options.html, https://docs.mathjax.org/en/v2.7/advanced/model.html]
status: explained
created: 2026-11-02
updated: 2026-11-02
---

# Math-Aware Markup Extraction

## Meaning

Math-aware extraction converts a web document into text without silently deleting its equations. Mathematics may be represented by TeX source, structured mathematical markup or equation-image descriptions rather than ordinary visible prose. Recovering those representations is a distinct objective from simply removing navigation and other boilerplate.

## Mechanism

[[web-text-extraction]] selects what survives into the corpus. Inspect equation-bearing elements before generic script, hidden-element and image cleanup. A supported extractor can recover source notation from math-specific script elements or TeX annotations, preserve structured mathematical content, and use equation-image alternative text when it is actually informative. Do not execute scripts or assume every image description is a faithful equation.

Choose one representation per equation, retain inline versus display boundaries and nearby prose, and avoid duplicating hidden source with its rendered copy. Preserve raw snapshots and extraction versions so disagreements can be inspected. OpenWebMath explicitly designs extraction to retain mathematical content before quality filtering and deduplication; it is evidence for a pipeline strategy, not a guarantee that every markup system is handled.

## Worked example

An archived page represents a fraction using the literal TeX string `\frac{a}{b}` in a math-specific element. A generic script-removal rule drops that element and emits “the ratio is .” A math-aware pass first records the fraction with an equation boundary, then removes the enclosing markup and emits “the ratio is [math: \frac{a}{b}].” A second hidden rendering of the same expression should not create a second training example.

Keeping the characters alone is not sufficient: flattening a superscript into an ordinary adjacent digit changes meaning even when both characters remain. Validate mathematical structure rather than only counting backslashes.

## Validation and boundaries

Build adjudicated fixtures for fractions, superscripts, matrices, mixed Unicode, plain-text notation and duplicate visual/source representations. Measure equation fidelity and document retention after extraction, filtering and deduplication separately. A downstream classifier cannot reliably recover equations already deleted. Equal model and token budgets do not establish extraction loss as the cause of a capability difference; compare matched preprocessing variants with controlled downstream training and evaluation. Avoid universal claims about particular historical filters without checking their exact implementation and version.

## Prerequisites

- [[web-text-extraction]]

## Sources

- <https://arxiv.org/html/2310.06786v1>

- <https://katex.org/docs/options.html>
- <https://docs.mathjax.org/en/v2.7/advanced/model.html>
