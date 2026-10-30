# Masked Attention Numerics

## Meaning

Masking invalid attention keys and handling a query with no valid keys are different problems. [[transformer-attention]] forms a weighted average over permitted values. If none are permitted, the application must define a separate result rather than assume ordinary normalization provides one.

## Mechanism

A common stable normalization subtracts the row maximum before exponentiation. An entirely negative-infinity row makes that subtraction undefined. Some backends explicitly handle this case; others can expose non-finite intermediates. A finite sentinel avoids that particular subtraction but can assign weight to entries that should not participate.

Under [[mixed-precision-training]], also check the format in which the mask is created and combined. Minus one billion cannot be represented as a finite binary16 value. Adding very negative finite biases can overflow before a later higher-precision normalization runs. Numerical safety therefore depends on the whole path, not just one final cast.

## One example

Three value scalars are 2, 5 and 8. If an invalid query receives three identical finite scores, normalization gives one third to each value and returns 5. This is finite but has no valid interpretation because every key was excluded. For a valid query allowing only the first two keys with equal scores, the expected output is 3.5. Testing both cases separates exclusion correctness from empty-query behavior.

## Check your understanding

Can zeroing a loss after it becomes non-finite guarantee safe gradients? No. Prevent or safely handle the invalid computation and exclude invalid queries according to the training objective. Validate outputs and gradients on the actual backend, including all-padding and combined causal/padding masks. Do not infer that all fused kernels share the same empty-row implementation.
