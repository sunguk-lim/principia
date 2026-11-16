# Vector ANN Index Families

## Meaning

Vector indexes trade exactness, recall, memory, and update cost. Flat scan is exact; IVF prunes by coarse clusters; HNSW traverses a graph; PQ compresses vectors; IVF-PQ combines pruning and compression.

## Mechanism

[[nearest-neighbor-search]] gives the common objective. IVF probe count, HNSW search breadth, and PQ code size are different knobs. ScaNN is one implementation combining partitioning, approximate scoring, and rescoring. Compare all methods at the same recall target against an exact flat baseline.

## One example

A million embeddings fit in memory but scanning each one is too slow. IVF probes a handful of clusters; if the correct neighbor lies just across a centroid boundary, a low probe count misses it. Increasing probes improves recall while raising query work.

Exact rescoring fetches original vectors for the acquired candidates and recomputes the original distance. It can repair their ordering but cannot discover an excluded item. Suppose exact distances rank A=.1, B=.2, C=.3, while candidate selection returns only B,C. Exact rescoring still cannot return A; for top two, recall against A,B is one half. More candidates can recover A at the cost of scoring and original-vector reads. Retained originals also remain a storage term even when the first stage uses tiny codes. A learned relevance reranker is a different scoring operation, not necessarily exact vector-distance recomputation.

## Check your understanding

**Question:** Why is lower latency alone not enough to choose an ANN index? **Answer:** The index may have lower recall, higher memory use, slower updates, or worse downstream answer quality.
