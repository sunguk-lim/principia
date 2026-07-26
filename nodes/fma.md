---
id: fma
title: Fused Multiply-Add
summary: "A fused multiply-add (FMA) is a single hardware operation that computes d = a × b + c: it multiplies two numbers and adds a third, all at once."
type: concept
tags: [gpu]
prereqs: [arithmetic]
sources: [linux-internals-complete.html §15]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Fused Multiply-Add

## Summary

A fused multiply-add (FMA) is a single hardware operation that computes `d = a × b + c`: it multiplies two numbers and adds a third, all at once. The word *fused* means the multiply and the add happen as one indivisible step with a single rounding at the very end, rather than as two separate operations that each round their result. This buys two things. First, accuracy: rounding once loses less precision than rounding twice. Second, speed: FMA is the basic arithmetic instruction a graphics processor (GPU) executes, so nearly all heavy numeric work — dot products, matrix multiplication, convolutions — is built as long chains of FMAs, and a GPU's headline speed is literally counted in them.

## Grounded explanation

Recall from [[arithmetic]] that multiplication (`×`) and addition (`+`) are two of the four primitive operations on numbers. An FMA simply combines one of each into a fixed pattern: given three numbers `a`, `b`, and `c`, it produces `d = a × b + c`. The result `d` is the product of `a` and `b`, added to `c`. So far this is nothing new — you could get the same answer by first computing `a × b` and then adding `c` as two ordinary [[arithmetic]] steps. The whole idea of FMA is *how* it does this, not *what* it computes.

The key word is **fused**. A computer cannot store most numbers exactly: it keeps only a fixed number of digits, so after almost every operation it must **round** the true answer to the nearest representable value, throwing away the leftover digits. If you compute `a × b + c` as two separate operations, you round twice: once on the product `a × b` (discarding digits before you have even added `c`), and once again on the final sum. A fused multiply-add instead computes the *exact* product `a × b` internally, with full digits and no rounding, adds the exact `c` to it, and rounds **only once** at the very end. That single difference — one rounding instead of two — is the entire concept.

**Why it matters, payoff one: accuracy.** Each rounding step injects a small error. Two roundings can inject two errors, and the first one is especially harmful because it corrupts the product before the add ever sees it. The fused version carries the full-precision product all the way into the add, so the only error introduced is the unavoidable final rounding. This is why the fused result and the two-step result can differ slightly: they are genuinely different computations, and the fused one is the more faithful of the two.

**Why it matters, payoff two: speed.** A GPU is a processor with thousands of small arithmetic units running in parallel; each such unit is called a *lane*. The fused multiply-add is the fundamental instruction those lanes execute — a lane can complete one FMA in a single clock cycle. Because one FMA performs one multiply *and* one add, the convention is to count it as **two** floating-point operations. (A *floating-point operation*, or FLOP, is one arithmetic step on a non-integer number; a machine's speed is rated in FLOPs per second.) So a GPU's advertised peak speed is, in effect, just the number of FMAs all its lanes can finish per second, multiplied by two. The hardware's top speed is *defined* in terms of this one operation.

These two payoffs are why FMA sits at the center of GPU math. Almost all the heavy computation a GPU does is **sums of products** — a running total that keeps adding one more product to itself. The clearest example is the *dot product*: take two lists of numbers, multiply them position by position, and add up all those products into a single number. Written as FMAs, this is a chain — start an accumulator `c` at zero, and each step does `c = a × b + c`, folding the next product into the running total. Every step is exactly one FMA. Matrix multiplication is built directly on this: each entry of the output matrix is a dot product of one row and one column, hence its own chain of FMAs. Convolutions, the core operation of image-processing neural networks, are the same shape — each output is a running sum of products of nearby inputs and weights. Because all of this reduces to sums of products, making the single multiply-and-add fast *and* accurate is precisely what makes a GPU good at this kind of math. The most specialized GPU units, *tensor cores*, push this further: each one is a dense block of FMA units wired together to perform many fused multiply-adds at once on small tiles of two matrices, completing a little matrix multiply in a single instruction.

**Worked instance.** Take the dot product of the lists `(1, 2, 3)` and `(4, 5, 6)`. The accumulator `c` starts at `0`. The first FMA computes `c = 1 × 4 + 0 = 4`. The second takes that running total and adds the next product: `c = 2 × 5 + 4 = 14`. The third does the same once more: `c = 3 × 6 + 14 = 32`. The answer is `32`, reached in three FMAs — three single-rounding steps, one per term. Contrast the unfused route: compute `1 × 4`, `2 × 5`, and `3 × 6` as three separate multiplies, then add them in three separate additions — six operations and six roundings to reach the same `32`. The fused version does it in half the operations and, because each step rounds once instead of the multiply-then-add pair rounding twice, with less accumulated error. That halving and that tighter accuracy, repeated across the billions of products inside a matrix multiply, are the whole reason FMA is the GPU's basic operation.

## Prerequisites

- [[arithmetic]]

## Sources

- `linux-internals-complete.html` §15 — "FMA — the basic GPU operation"; glossary entry "FMA".
