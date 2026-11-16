---
id: rabitq
title: RaBitQ
summary: RaBitQ uses a randomized binary codebook and a corrected inner-product estimator to approximate vector distances under an explicit probabilistic error model.
type: concept
tags: [ml/information-retrieval]
prereqs: [binary-embedding-quantization, matrix-multiplication, vector-dot-product, expectation]
sources: [https://arxiv.org/html/2405.12497v1]
status: explained
created: 2026-11-17
updated: 2026-11-17
---

# RaBitQ

## Meaning

RaBitQ is a randomized vector quantizer and distance estimator. It is not simply [[binary-embedding-quantization]] followed by counting differing bits. The original construction stores one sign bit per dimension together with correction metadata, and uses the query values to estimate distance.

## Mechanism

Let x be a database vector, q a query, c a chosen center, and D the coordinate count. Define radii r_x=||x-c|| and r_q=||q-c||, where ||v|| is the square root of the [[vector-dot-product]] of v with itself. For nonzero radii define unit directions u=(x-c)/r_x and v=(q-c)/r_q. The exact squared distance is r_x^2+r_q^2-2r_x r_q(u·v). A zero radius needs a separate direct-distance case.

Apply a shared random orthogonal transform, a [[matrix-multiplication]] that preserves dot products, to spread directions before sign coding. Conceptually the codebook consists of rotated vectors whose D coordinates before rotation are each plus or minus 1/sqrt(D). It has 2^D entries but is not explicitly materialized. Let u_hat be the selected unit codeword in the original coordinate system. Store its signs, radius and correction alpha=u_hat·u. Estimate u·v with (u_hat·v)/alpha rather than treating u_hat as exactly u.

Why divide? The component of u_hat along u is alpha times u. Dotting that part with v gives alpha(u·v); division removes this shrinkage. A perpendicular component remains as estimation error. The paper analyzes that error over the random rotation and establishes an unbiased estimator and probabilistic bounds under its construction. [[expectation]] over randomized transforms is not an assertion that every single answer equals the exact dot product.

## One example

For an illustrative code realization, let r_x=2, r_q=3, alpha=.8 and u_hat·v=.24. The corrected directional estimate is .24/.8=.3, giving squared distance 4+9-2×2×3×.3=9.4. Substituting the uncorrected .24 gives 10.12. If the true u·v were .35, the exact distance would be 8.8: correction reduces a particular shrinkage but does not remove every realization's error. These are explanatory values, not benchmark results.

## Validation and check

Test estimator error, nearest-neighbor recall, outlier queries, seeds and retained metadata cost against exact distances and tuned alternatives. Candidate pruning and final rescoring introduce additional contracts. A theoretical distance-error statement does not guarantee perfect neighbor order when distances are nearly tied, and the paper's benchmark superiority remains an author-reported empirical result. Does one bit per dimension describe all index memory? No: radii, correction factors, center/transform state, IDs and search structure remain.

## Sources

- <https://arxiv.org/html/2405.12497v1>
