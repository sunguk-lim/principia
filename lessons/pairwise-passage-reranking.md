# Pairwise Passage Reranking

## Meaning

Pairwise passage reranking compares two retrieved passages for one query, then turns those preferences into a final order. It cannot repair a missing candidate; the [[retrieval-evidence-gate]] still has to distinguish missing evidence from poor ordering.

## Mechanism

Ask for A versus B, then reverse the presentation to check whether the judgment is positional. One published Pairwise Ranking Prompting policy treats inconsistent order-reversed results as a tie. An all-pair aggregator gives one point for a win and half a point for a tie, with a declared rule for equal totals. Other policies use sorting or limited passes, changing both comparison cost and sensitivity to the initial ranking.

For n candidates, comparing every unordered pair requires n(n-1)/2 comparisons. Asking in both orders doubles the judgments. Batching can reduce dispatch overhead but does not remove this model work.

## One example

Suppose A beats B, B beats C and C beats A. Each receives one point. This cycle has no unique consistent ordering; an initial-order tie-breaker merely makes the output deterministic.

Instead, let A versus C be a tie while A beats B and B beats C. The totals become A=1.5, B=1 and C=0.5, so the aggregator orders A, B, C. Three unordered pairs required six judgments when each was shown both ways.

## Check your understanding

Can a pairwise model be dropped into a sorting algorithm with a guarantee of a globally consistent result? Not generally. Its preferences may be noisy or cyclic. Specify tie and invalid-output policies, and evaluate reversal consistency, evidence retention, answer support, latency and cost on held-out queries. A ranking procedure is separate from its training objective and underlying model architecture.
