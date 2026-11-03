---
id: muon-optimizer
title: Muon Optimizer
summary: Muon transforms matrix momentum toward a polar-like update before applying a shape-scaled parameter step.
type: concept
tags: [ml/deep-learning]
prereqs: [momentum, matrix-polar-factor]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.optim.Muon.html, https://kellerjordan.github.io/posts/muon/]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Muon Optimizer

## Meaning

Muon applies a matrix-level transformation to [[momentum]] rather than rescaling each entry independently. Its update approximates the orientation part of a matrix momentum buffer, reducing the dominance of large stretching directions. This mechanism is intended for eligible matrix parameters, not every scalar, bias or embedding by default.

## Mechanism

Form a momentum buffer from gradients, with an optional Nesterov-style lookahead convention. Normalize its matrix scale, then apply a bounded number of Newton–Schulz-style polynomial iterations. [[matrix-polar-factor]] explains the idealized operation: remove directional stretching while keeping orientation. Fast Muon polynomials only approximate that objective; finite iterations and reduced precision need not produce exactly orthonormal rows or columns.

Apply the transformed direction using a learning rate and an explicitly chosen matrix-shape scaling. Implementations differ on aspect-ratio adjustment, target update magnitude and decay. Select hidden matrix parameters according to the model and implementation contract and give other parameters a specified auxiliary optimizer. Being two-dimensional alone does not prove that an embedding should use the hidden-layer policy.

## One example

Take an illustrative momentum matrix B=[[0,-2],[3,0]]. Its exact polar factor is U=[[0,-1],[1,0]]. A step with learning rate 0.1 and no shape adjustment subtracts 0.1*U, rather than 0.1*B. The original directional magnitudes 2 and 3 both become 1, but the orientation and signs remain. A production finite-iteration implementation will generally produce an approximation, and any shape multiplier changes the actual step magnitude.

## Check your understanding

Can an exact-polar teaching example certify a fast low-precision kernel? No. Compare the approximate transform with a numerical reference across matrix shapes, near-zero and poorly conditioned inputs. Measure full training quality, peak state/workspace, iteration cost and time-to-quality. Retune the declared update-scaling convention and auxiliary optimizer; a headline learning rate without those choices is an incomplete algorithm specification.

## Prerequisites

- [[momentum]]
- [[matrix-polar-factor]]

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.optim.Muon.html>
- <https://kellerjordan.github.io/posts/muon/>
