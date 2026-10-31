# Hierarchical Document Retrieval

## Meaning

Hierarchical document retrieval searches through document or section branches instead of scoring every passage in one flat step. A tree provides a map of where evidence might be; the system opens selected branches and reads the underlying source.

## Mechanism

Internal entries hold descriptions such as section titles, summaries and page ranges. Given a query, the selector keeps a bounded set of promising children, expands them, and repeats until it reaches useful passages. An evidence check can open additional branches when the first material is insufficient.

The selection method is a separate choice. Generated reasoning, a relevance classifier or another scorer can operate on a hierarchy. Offline grouping can still use embeddings even when query-time navigation does not. Authorization must cover summaries and full text alike.

## One example

A report contains Finance, Operations and Risk branches. A question about debt selects Finance. Its text refers to a table in Appendix G under Risk. If the system follows that pointer and verifies the table's year, it can collect the needed evidence. If it pruned Risk permanently, later reranking inside Finance cannot find the missing table.

This is the central tradeoff: opening fewer branches saves scoring work, but every early exclusion limits later evidence. Summaries and layout parsers can be wrong, so preserving a tree does not guarantee that a table or cross-reference survives correctly.

## Check your understanding

Does removing the vector database remove retrieval failures? **No.** Failures can move to tree construction, branch selection and stale summaries. Evaluate evidence containment at each level, final citation support, latency, build cost and bounded fallback behavior against flat and hybrid retrieval baselines.
