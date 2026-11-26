# KV Cache

## Meaning

A KV cache stores the per-layer keys and values already computed for earlier tokens in causal autoregressive inference. A later token reuses those states instead of projecting the whole earlier sequence again. It saves repeated computation by keeping more state.

## Mechanism

A causal token state depends on its permitted past, not on later tokens. Under a compatible model, positions, masks and execution contract, earlier keys and values can be retained. Process the new token, append its keys and values and calculate its attention against the required cached history. Each layer has its own cache.

Reusing earlier states does not eliminate attention reads. Full-history decode still reads relevant earlier keys and values for the new query. An implementation must align positions and masks with both past and new tokens. Incompatible model changes or invalid state cannot be repaired merely by preserving the same bytes.

## One example

Assume one sequence, two layers, four retained positions, two KV heads, three scalar coordinates per head and two bytes per scalar. Keys and values together occupy `2 × 1 × 2 × 4 × 2 × 3 × 2 = 192` payload bytes. One new retained token adds 48 bytes, making 240.

At fixed architecture and batch, this payload grows linearly with retained positions. That is different from the quadratic interaction count of a full dense prefill. The example excludes allocation padding, temporary buffers and quantization metadata; query-head count is not automatically KV-head count.

## Check your understanding

Does caching make every future decoding step constant-time? No. It avoids repeated old-state projection but leaves history-dependent reads and new computation. Compare cached and recomputed outputs, masks and positions under the intended numerical tolerance. Measure total memory and latency separately; KV state is not necessarily the dominant cost for every workload.
