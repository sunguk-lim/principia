# FlashAttention Version Comparison

## Meaning

FlashAttention versions solve the same mathematical attention problem while changing how GPU work is scheduled. Their names identify implementation generations, not a guaranteed speed order for every workload.

## Mechanism

The first [[flash-attention]] avoids writing a full attention score matrix to HBM. FlashAttention-2 improves work partitioning and parallelism. FlashAttention-3 uses newer asynchronous execution capabilities to overlap GPU operations. The [[memory-hierarchy]] remains central, while [[gpu-tile-programming]] determines whether a particular tile schedule keeps the device busy.

## One example

On one GPU, benchmark causal attention with the same batch, sequence length, head dimension, dtype, and software version for all supported kernels. Compare outputs within an appropriate numerical tolerance and record kernel time and peak memory. Repeat with longer sequences before concluding which version is better.

## Check your understanding

**Question:** Why can FlashAttention-3 fail to beat an older version on a given setup? **Answer:** Hardware support, shape, precision, feature coverage, and fallback behavior may prevent its scheduling advantages from applying.
