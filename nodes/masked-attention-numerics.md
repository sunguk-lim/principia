---
id: masked-attention-numerics
title: Masked Attention Numerics
summary: Masked attention numerics distinguishes excluding invalid keys from defining empty-query behavior and tests both under the executed floating-point format.
type: concept
tags: [ml/deep-learning]
prereqs: [transformer-attention, mixed-precision-training]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html, https://docs.pytorch.org/docs/2.15/notes/numerical_accuracy.html]
status: explained
created: 2026-10-31
updated: 2026-11-23
---

# Masked Attention Numerics

## Meaning

An attention mask has two obligations: exclude invalid keys for a valid query, and define what happens when a query has no valid keys. The second case is not an ordinary probability distribution. A large negative constant does not supply a semantic answer to an empty set.

## Mechanism

In [[transformer-attention]], a score bias is applied before row-wise normalization. Negative infinity represents exclusion in the mathematical nonempty case. But the familiar stable implementation subtracts each row's maximum before exponentiating. For an entirely negative-infinity row, that subtraction is undefined. A backend may explicitly handle the empty row; a naive implementation may return non-finite values. These are different implementations, not a universal claim that every fused attention kernel fails.

[[mixed-precision-training]] makes representability part of the contract. A finite number in a wider format can become infinity in a narrower one. IEEE binary16's largest finite magnitude is 65,504, so minus one billion is not a finite binary16 sentinel. Adding multiple very negative finite biases can also overflow. Upcasting a later normalization cannot repair earlier overflow or a logically inverted mask.

## Worked example

Take three keys with value scalars 2, 5 and 8. For an invalid query, filling all three scores with the same finite number gives normalized weights one third each, so the output becomes `(2+5+8)/3=5`. That is a finite but meaningless mixture: there were no permitted values to average. If instead all scores are negative infinity, a naive maximum-subtraction implementation encounters negative infinity minus negative infinity. Neither result establishes correct empty-query behavior.

For a valid query permitting only the first two keys, equal allowed scores should yield `(2+5)/2=3.5`, with no contribution from the third key. This nonempty reference checks exclusion independently of the empty-row test. With additive finite biases, residual score differences and rounding can also affect the invalid row; it is not guaranteed to be exactly uniform.

## Validation and boundaries

Define invalid-query behavior explicitly, for example a safe zero result and exclusion from the supervised loss, and ensure the implementation does not propagate invalid intermediates into gradients. Multiplying an already non-finite loss by zero is not a repair. Test finite forward results and gradients, all-padding cases, causal-plus-padding composition, representative dtypes and actual backend dispatch. Use a simple wider-precision reference for valid rows. A padded query can be semantically ignorable even though its computational path must still be numerically safe.

## Boolean conventions and query rows are separate contracts

A padding label says which positions are padding; an attention API decides how a boolean value is interpreted. In the inspected PyTorch 2.15 scaled-dot-product-attention API, True means that the key participates. In MultiheadAttention's key_padding_mask, True instead marks a key to ignore. Passing the same boolean array between those interfaces without translating it reverses the intended evidence boundary.

For keys with values [2,5,8], suppose the third position is padding. The padding mask is [False,False,True], while the corresponding participation mask is [True,True,False]. For equal allowed scores, the valid output is (2+5)/2=3.5. Reusing the padding mask as participation selects only 8: the result is finite but semantically wrong. This error is independent of the all-invalid-row numerical problem above.

Key exclusion does not automatically suppress padded query outputs. Specify how invalid query rows are handled and excluded from downstream objectives. Test mask shape and broadcasting, causal-plus-padding composition, non-square cached decoding and the actual backend. The inspected API documents a causal/explicit-mask restriction; construct a compatible combined mask when needed rather than assuming every backend accepts both controls. Pin the API version because a mathematical mask definition does not establish one library's argument convention.

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html>
- <https://docs.pytorch.org/docs/2.15/notes/numerical_accuracy.html>
