# Batch-Invariant Inference

## Meaning

Batch-invariant inference keeps a request's numerical result unchanged when unrelated requests change around it. It is stronger than repeating one fixed batch and obtaining the same output.

## Mechanism

An inference server can change the group of active requests after every generation step. Although each request has separate logical state, kernels may choose reduction partitions according to the combined batch shape. Different rounded partial sums can change logits. Fixing the per-request arithmetic across those batch changes removes this particular dependence on traffic.

The guarantee belongs to the complete numerical path, including normalization, matrix multiplication, attention, cache handling and distributed reductions. A greedy sampler alone cannot supply it. Stochastic sampling additionally needs a reproducible random-number policy; changed input tokens or model weights are not numerical nondeterminism.

## One example

A's best two scores are 12.3417 and 12.3415 when run with B. When run with C and D they become 12.3414 and 12.3416. Both complete batches may be perfectly repeatable, but A chooses a different token in each. Its later continuation then changes because the prefix changed.

To test invariance, keep A's tokens and model fixed while changing batch size, position, neighboring prompt lengths and admission timing. Compare numerical results and locate the first divergent token. A test consisting only of repeated single-request calls is too narrow.

## Check your understanding

Does a deterministic-kernel mode guarantee identity across every model, GPU and release? **No.** Supported platforms, model paths and distributed shapes define its scope. Verify that scope and measure the latency/throughput cost. Batch invariance is a numerical property, not proof that the generated answer is correct.
