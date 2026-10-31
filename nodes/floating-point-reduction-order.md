---
id: floating-point-reduction-order
title: Floating-Point Reduction Order
summary: Floating-point reduction order fixes which rounded partial sums are combined, so mathematically equal sums can produce different machine values.
type: concept
tags: [parallel-computing]
prereqs: [numeric-precision-formats, reduction-operation]
sources: [https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Floating-Point Reduction Order

## Meaning

A reduction combines many input values into one. In exact arithmetic, addition can be regrouped without changing its result. In a finite [[numeric-precision-formats|numeric precision format]], intermediate rounding breaks that guarantee. The order includes both which values are grouped and the precision used at each intermediate step.

## Mechanism

The algebraic associativity described by [[reduction-operation]] permits a parallel tree for exact addition. Machine addition rounds each intermediate result onto a representable grid. Regrouping changes which small contributions are lost before larger values arrive. A parallel implementation can be completely repeatable for one shape while choosing a different, also repeatable tree for another shape. Therefore changed numerics do not by themselves prove a race or a random hardware operation.

A matrix kernel can partition its inner sum among workers and then combine their partial sums. Changing the number or boundaries of those partitions changes rounding. Accumulation precision matters separately from operand storage: half-precision inputs do not imply half-precision intermediate accumulation.

## Worked example

Assume binary16 rounding after every addition, round to nearest, and inputs represented near 1,024 and 0.4. Between 1,024 and 2,048 adjacent representable values are one unit apart. First compute 1,024+0.4: it rounds to 1,024. Adding another 0.4 again rounds to 1,024. Instead combine the small values first: their binary16 sum is approximately 0.7998; adding it to 1,024 rounds to 1,025. Both paths implement the same exact sum of the represented inputs; different intermediate rounding gives different final values. The example isolates binary16 arithmetic, not the accumulation behavior of every GPU matrix multiply.

## Boundaries and validation

Pin inputs, storage and accumulation formats, kernel version and reduction partition. Compare repeatability at fixed shape separately from sensitivity to changed shape. A wider accumulator often reduces error but does not prove all execution paths are bitwise identical. Numerical tolerance and bitwise identity are different contracts; neither alone establishes task quality. A fixed tree may sacrifice a faster shape-specific strategy, so measure the required accuracy together with runtime.

## Prerequisites

- [[numeric-precision-formats]]
- [[reduction-operation]]

## Sources

- <https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/>
