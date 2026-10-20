---
id: logarithm
title: Logarithm
summary: A real logarithm inverts a positive-base exponential, turning multiplicative ratios into additive differences.
type: concept
tags: [math/calculus]
prereqs: [exponential-function]
sources: [https://dlmf.nist.gov/4.2]
status: explained
created: 2026-10-21
updated: 2026-10-21
---

# Logarithm

## Meaning

For a positive base b other than 1, log_b(x) is the exponent y satisfying b^y=x. The real logarithm therefore takes a positive input and returns an exponent. The natural logarithm, written ln(x), uses the base e of the [[exponential-function]].

## Mechanism

Because the exponential is positive and strictly increasing for base e, every positive x corresponds to one real y with e^y=x. Thus ln(e^y)=y and e^(ln(x))=x. In particular, ln(1)=0, ln(x)>0 for x>1, and ln(x)<0 for 0<x<1. Zero has no finite real logarithm, and negative inputs have no real value under this contract; complex logarithms are outside this lesson.

The exponential identity e^(u+v)=e^u e^v explains the product rule. Let x=e^u and z=e^v for positive x,z. Then xz=e^(u+v), so ln(xz)=u+v=ln(x)+ln(z). Similarly ln(x/z)=ln(x)-ln(z). There is no corresponding identity ln(x+z)=ln(x)+ln(z).

Changing base rescales the result: log_b(x)=ln(x)/ln(b). For b>1 it preserves ordering; a base between zero and one reverses ordering. State the base whenever numerical values or units depend on it.

## Worked example

In base 2, log_2(8)=3 because 2^3=8, and log_2(4)=2 because 2^2=4. Multiplying inputs gives 8×4=32=2^5, so log_2(32)=5=3+2. Dividing gives 8/4=2, so log_2(2)=1=3-2. In contrast, 8+4=12 is not 32, so the sum rule cannot use 3+2.

Logarithms compress large multiplicative ranges without treating all ratios as equal. A doubling adds the same log_2 increment of one at any positive scale. This makes log ratios useful for weights and comparisons, while a zero count needs an explicitly defined smoothing or domain policy.

## Check your understanding

**Question:** What is ln(0)? **Answer:** It has no finite real value. Replacing zero by a positive smoothed value changes the quantity and must be specified.

## Prerequisites

- [[exponential-function]]

## Sources

- <https://dlmf.nist.gov/4.2>
