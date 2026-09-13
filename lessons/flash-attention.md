# FlashAttention

## Meaning

**Goal:** explain how tiling avoids storing the complete attention matrix.

FlashAttention reorganizes [[transformer-attention]] around the GPU's memory hierarchy: large off-chip memory and smaller, faster on-chip memory. It preserves the mathematical attention operation; floating-point results need not be bit-for-bit identical.

## Mechanism

Process query, key, and value blocks rather than materializing all pairwise scores. For each query, carry a running maximum, a normalizer, and an unnormalized weighted-value sum. When a larger score arrives, rescale both sums using the same correction from [[online-softmax]]. Divide the final weighted sum by the normalizer.

## One example

For two keys with scores $[0,\log 2]$ and scalar values $[3,9]$, the shifted weights are $[1/2,1]$. Their normalizer is $1.5$ and their weighted sum is $10.5$, giving output $7$. Processing one key at a time reaches the same mathematical result after rescaling the first contribution.

## Check your understanding

Does avoiding the full score matrix make dense attention's arithmetic linear in sequence length?

**Answer:** no. Dense pairwise computation remains quadratic. The improvement is reduced memory traffic and avoidance of quadratic intermediate storage. Actual traffic depends on tile sizes, head dimension, and available fast memory; it is not universally linear. Speedups depend on hardware and workload.

Reference: [FlashAttention](https://arxiv.org/abs/2205.14135).
