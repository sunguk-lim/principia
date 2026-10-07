# Hierarchical Sparse Attention Index

## Meaning

Instead of comparing each query to every past token, a sparse attention index chooses candidates. A hierarchical index makes an early broad choice and lets later stages search within that chosen pool.

## Mechanism

[[transformer-attention]] normally scores the full history. Candidate selection can reduce attention memory traffic, but it introduces an index-building cost and an early recall risk. If the first stage omits the one relevant token, deeper stages cannot recover it by searching only the surviving pool. Sharing candidates or index keys across layers may save [[kv-cache]] space while making their mistakes correlated.

Compare with dense and local-window attention at matched model quality. Place important facts at varied context positions and measure candidate recall, latency, and bytes, not merely aggregate next-token loss.

## One example

A 100K-token document has an answer near its beginning. A query about that fact will fail if the broad index selects only the recent paragraphs, however fast the later attention calculation becomes.

## Check your understanding

**Question:** What is the key accuracy risk? **Answer:** False-negative candidate selection before full attention is computed.
