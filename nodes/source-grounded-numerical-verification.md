---
id: source-grounded-numerical-verification
title: Source-Grounded Numerical Verification
summary: "Source-grounded numerical verification checks a reported number against an identified source location, semantic context and explicit transformation rather than relying on repeated agreement."
type: concept
tags: [ml/agents]
prereqs: [agent-verification-loop, citation-support-validation, dataset-lineage, arithmetic]
sources: [https://arxiv.org/abs/2309.11495, https://openlineage.io/docs/spec/object-model/]
status: explained
created: 2026-11-05
updated: 2026-11-05
---

# Source-Grounded Numerical Verification

## Meaning

A reported number is a claim about a quantity, not just a sequence of digits. Verification must bind the value to its entity, period, unit and source location, then check the operation that produced the reported result. A plausible number copied from the wrong row can pass arithmetic and range checks while remaining false.

## Mechanism

[[citation-support-validation]] checks that a claim follows from its cited span. The additional objective here is to reconstruct a typed quantity and its computation, not only assess textual support. Preserve a compact evidence record: source version, page or cell location, row and column labels, unit, time period, extracted value and any transformation. [[dataset-lineage]] grounds the distinction between an input version and the run that processed it. The record must point to retrievable evidence; a citation string alone is not verification.

Within an [[agent-verification-loop]], separate three tests. Check that the source actually states the extracted quantity. Check that its meaning matches the question, including period and units. Then recompute the transformation with [[arithmetic]] outside the model where practical. A second extractor should consult the identified source without being shown the proposed number when that would anchor its answer. Shared parsers, stale snapshots and a common mistaken label can still cause common errors.

Chain-of-Verification studies independently answered verification questions before final synthesis. It motivates separating checking from the draft; it does not certify this particular numeric-record design or make a model critic an oracle. The evidence record and example here are independent engineering constructions.

## One example

An invented table reports service A revenue of 125 and 140 thousand dollars for two successive quarters, and service B revenue of 150 and 160. The question asks for service A's second-quarter revenue in dollars. An agent returns 160,000. Multiplying 160 by 1,000 is correct and the value is in range, but the row is wrong. A source-location check obtains A's second-quarter cell, 140; the unit conversion gives 140×1,000=140,000. Comparing the two evidence records localizes a row-selection error, not an arithmetic error.

## Check your understanding

Would two agents returning 160,000 settle the claim? No: both may have selected B. Test wrong rows, swapped columns, stale periods, unit changes, missing evidence and incorrect conversions separately. Measure detected errors and false alarms against known source truth. If the source is unavailable or ambiguous, preserve that uncertainty and withhold unsupported numerical certainty rather than manufacturing agreement.

## Prerequisites

- [[agent-verification-loop]]
- [[citation-support-validation]]
- [[dataset-lineage]]
- [[arithmetic]]

## Sources

- <https://arxiv.org/abs/2309.11495>
- <https://openlineage.io/docs/spec/object-model/>
