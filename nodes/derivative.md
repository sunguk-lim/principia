---
id: derivative
title: Derivative
summary: The derivative measures the instantaneous rate of change of a function — how fast its output moves as its input nudges.
type: concept
tags: [math/calculus]
prereqs: [arithmetic]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Derivative

## Summary

The **derivative** measures the instantaneous rate of change of a function — how
fast its output moves as its input nudges.

## Grounded explanation

The slope of $f$ at $x$ is the ratio of a tiny output change to the input change
that caused it (a difference divided by a difference — [[arithmetic]]):

$$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$$

We take the *limit* (the input change shrinking to zero) as the calculus floor and
stop there. A positive derivative means $f$ is rising; zero means flat — which is
how optimization knows where a minimum is.

## Prerequisites

- [[arithmetic]]

## Sources

_none_
