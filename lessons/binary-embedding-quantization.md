# Binary Embedding Quantization

## Meaning

Binary embedding quantization replaces every numeric embedding coordinate with one bit. The compact code makes approximate retrieval cheaper to store and compare, while throwing away information that may matter for ranking.

## Mechanism

A simple rule assigns one to a positive coordinate and zero otherwise. Both documents and queries must use the same threshold convention. Bits are packed into bytes. Hamming distance counts positions where two codes differ, so fewer differing bits indicate a closer binary code—not necessarily the closest original vector.

A system can retrieve more candidates with binary codes and then rescore them. Keeping full-precision document vectors for rescoring changes memory accounting; using only a full-precision query with binary documents is a different option. Measure both instead of treating every reranking design as free.

## One example

The query [0.8,-0.2,0.1,-0.9] becomes 1010. A document with [0.7,-0.1,0.4,-0.8] has the same code and distance zero. Another with [-0.1,-0.3,0.6,-0.7] becomes 0010 and differs at one bit. Many vectors can share 1010, so the code no longer tells us their relative magnitudes.

A 1,024-coordinate float32 vector needs 4,096 payload bytes. Its packed binary code needs 128. That is a 32-fold reduction in vector payload only. The index, identifiers, documents, rescoring representations and answer model still consume space.

## Check your understanding

Does a 32-fold smaller payload guarantee a 32-fold smaller RAG service? **No.** Report complete storage and compare candidate recall, final evidence support, latency and rescoring cost. Quantization is useful when its measured quality/cost tradeoff fits the actual corpus, not merely when its bit count looks attractive.
