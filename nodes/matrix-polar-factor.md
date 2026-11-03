---
id: matrix-polar-factor
title: Matrix Polar Factor
summary: A matrix polar factor separates orientation from positive directional stretching, yielding an orthogonal or rectangular semi-orthogonal factor.
type: concept
tags: [math/linear-algebra]
prereqs: [symmetric-eigendecomposition]
sources: [https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.polar.html, https://kellerjordan.github.io/posts/muon/]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Matrix Polar Factor

## Meaning

The polar factor separates a matrix's orientation from its stretching. For a square full-rank real matrix B, write B=U*H, where U transpose times U=I and H is symmetric with positive eigenvalues. U changes orientation without changing vector lengths; H carries directional stretching. Replacing B by U therefore changes the update's magnitude structure, not merely its coordinate representation.

## Mechanism

Using [[symmetric-eigendecomposition]], form H=(B transpose times B)^(1/2) and U=B*H^(-1). The square root is a matrix function in an orthonormal eigenbasis. Verify U transpose times U=H^(-1)*(B transpose times B)*H^(-1)=I. For a full-column-rank rectangular matrix with more rows than columns, the columns of U are orthonormal; for a full-row-rank wide matrix, use the corresponding left-factor construction and orthonormal rows. Rank deficiency requires distinguishing a partial factor from an orthonormal completion; the simple inverse formula no longer applies.

Iterative polynomial schemes can approximate this factor without a full decomposition. A classical scaled Newton–Schulz iteration is X_new=(3*X-X*X transpose*X)/2. Proper initial scaling and rank assumptions matter; finite iteration is an approximation. Optimizer implementations may deliberately use different polynomial coefficients for speed rather than compute the exact polar factor.

## One example

Take B=[[0,-2],[3,0]]. B transpose times B is diagonal [9,4], so H is diagonal [3,2]. Multiplying B by H inverse yields U=[[0,-1],[1,0]]. B stretches the first coordinate by 3 and the second by 2 while rotating; U keeps the rotation and removes both unequal stretches. U transpose times U is I, and U*H reconstructs B exactly.

## Check your understanding

Does any finite polynomial iteration produce exact orthogonality? No. Check orthogonality and reconstruction against a decomposition reference, with poorly conditioned, rectangular, zero and rank-deficient inputs. Keep numerical stabilization and intended approximation separate from claims about exact polar algebra.

## Prerequisites

- [[symmetric-eigendecomposition]]

## Sources

- <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.polar.html>
- <https://kellerjordan.github.io/posts/muon/>
