---
id: affine-recurrence-scan
title: Affine Recurrence Scan
summary: An affine recurrence scan composes state-update maps associatively to compute every recurrent prefix with a parallel tree.
type: concept
tags: [parallel-computing]
prereqs: [scan, matrix-multiplication, work-span-model]
sources: [https://docs.jax.dev/en/latest/_autosummary/jax.lax.associative_scan.html, https://arxiv.org/html/2312.00752v2]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# Affine Recurrence Scan

## Meaning

A recurrence can have a sequential-looking equation without requiring a strictly left-to-right evaluation. When each transition has a compact affine representation, composing transitions is associative. A prefix scan can compute every prefix map in parallel, then apply each map to the initial state. Associativity permits regrouping; it does not permit reordering time steps.

## Mechanism

Let h_t be a d-vector state, A_t a d×d matrix, and b_t a d-vector, with h_t=A_t h_(t-1)+b_t. Represent a transition by (A_t,b_t). Define an ordered combine of earlier map (A,b) and later map (C,e) as

$$(A,b)\star(C,e)=(CA,Cb+e).$$

[[matrix-multiplication]] shows that this pair represents applying the earlier map first and the later map second. Both groupings of three ordered maps produce the same matrix product and translated vector, so ⋆ is associative. [[scan]] computes all ordered prefixes. Applying prefix pair (P_t,q_t) to h_0 yields h_t=P_t h_0+q_t. The [[work-span-model]] gives O(log T) tree depth for T maps when combine cost is treated as fixed; a work-efficient scan uses O(T) combines. A simple doubling implementation can instead use O(T log T) work.

## Worked example

Use scalar maps f_1(h)=2h+1, f_2(h)=3h+4 and f_3(h)=0.5h-2, with h_0=2. Sequential states are 5, 19 and 7.5. The first combined pair is (2,1)⋆(3,4)=(6,7). Combining with (0.5,-2) gives (3,1.5), hence h_3=3×2+1.5=7.5. Combining the last two first gives (1.5,0), and (2,1)⋆(1.5,0) again gives (3,1.5). Reversing f_1 and f_2 would not preserve the states.

For dense d×d transitions, composing matrices can cost more than one matrix-vector recurrence step. Diagonal or structured transitions make compact combination practical. Coefficients may depend nonlinearly on the known current input while remaining affine in the previous state. Nonlinear dependence on the previous state does not generally admit this pair representation. Floating-point regrouping also changes rounding. Compare outputs and gradients against a sequential reference across lengths, dtypes and conditioning; then measure actual kernel work, memory traffic and latency rather than promising universal scan acceleration.

## Check your understanding

**Question:** Is associative composition necessarily commutative? **Answer:** No. Change parentheses, not temporal order.

## Prerequisites

- [[scan]]
- [[matrix-multiplication]]
- [[work-span-model]]

## Sources

- <https://docs.jax.dev/en/latest/_autosummary/jax.lax.associative_scan.html>
- <https://arxiv.org/html/2312.00752v2>
