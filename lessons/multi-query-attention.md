# Multi-query attention

Incremental decoding repeatedly reads the stored keys and values for earlier tokens. With ordinary multi-head attention, every query head has its own key and value history. That can make the KV cache large enough for memory traffic to limit generation speed.

Multi-query attention keeps several query heads but shares one key head and one value head among them. The queries still differ, so each can produce a different weighting over the common history. The cache holds fewer key/value vectors per token. If eight query heads each had their own key/value head, replacing those eight KV sets with one reduces this portion of the cache by roughly a factor of eight at fixed width and datatype. It does not shrink the model weights by eight or guarantee an eightfold speedup.

Sharing keys and values may cost quality because the heads have less freedom to represent different aspects of the past. The benefit depends on whether the original workload was bottlenecked by KV storage or bandwidth, and on the hardware and kernel. Compare the same training and serving conditions, measuring cache bytes, inter-token latency, throughput, and task quality at several context lengths and batch sizes.

A middle ground is to share one KV head within each small group of query heads rather than across every query head. That is grouped-query attention.

**Check:** Which tensor traffic does MQA reduce, and why might the end-to-end latency improve less than the cache-size ratio?
