# Inference Context Parallelism

## Meaning

Inference context parallelism distributes one request's token dimension across multiple devices. It addresses long-context work, not independent request throughput by itself.

## Mechanism

Prefill and decode have different shapes. Prefill computes many new token representations, so splitting query tokens can reduce time to first token. Decode computes only a few new queries but must read a potentially large KV history; splitting that history can reduce per-device cache use. The shards must still exchange or combine information so attention sees the whole permitted context. A bigger device group trades memory pressure against link traffic.

## One example

A model has few KV heads but a tensor-parallel group of many GPUs. Head sharding may duplicate KV history across devices. Decode context parallelism can shard token positions instead, then combine partial attention results. Measure cache occupancy and inter-token latency before adopting it.

## Check your understanding

**Question:** Why might prefill and decode choose different partitions? **Answer:** Prefill needs to distribute work over many query tokens, while decode is often constrained by stored KV history and communication per generated token.
