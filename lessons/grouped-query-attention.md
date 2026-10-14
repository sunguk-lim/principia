# Grouped-query attention

Grouped-query attention places several query heads in each key/value group. If there are eight query heads, one KV group is multi-query attention, eight KV groups approximate ordinary multi-head attention, and a choice such as two or four groups lies between them. Every query head still computes its own attention weights, but heads in one group read the same stored keys and values.

The number of KV groups controls a trade-off. Fewer groups reduce cache memory and traffic during decoding. More groups give the model more distinct past representations and may preserve quality. The effect on latency is not necessarily proportional to group count: memory parallelism, batch size, sequence length, and kernel behavior matter. A serving system should measure the actual workload rather than assume that one group is always fastest.

An existing multi-head checkpoint can sometimes be adapted by pooling key/value projections within groups and continuing training. This is a conversion method described in the GQA paper, not a free drop-in switch for every checkpoint. Evaluate converted and originally trained variants separately. Compare task quality, long-context behavior, cache size, first-token and inter-token latency, throughput, and peak memory under matched conditions.

**Check:** For eight query heads, what changes when the model uses two KV groups instead of one? What might improve, and what becomes more expensive?
