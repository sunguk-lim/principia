# Decision-Model Hierarchical Retrieval

## Meaning

Decision-model hierarchical retrieval chooses branches using bounded relevance judgments, rather than generating navigation prose at every step. It combines a hierarchical search architecture with a specific scoring interface.

## Mechanism

Place the query and candidate descriptions in shared context. Ask whether each candidate is relevant, keep a limited number, and expand their children. Repeat until passages are available. The application still enforces permissions, budgets and fallback; a model score is not authority.

Distinguish two response types. Several binary relevance questions produce separate yes/no probabilities, so their yes scores need not sum to one. A multiple-choice question treats its options as competitors and returns one normalized distribution. Changing the candidate pool or splitting it across calls can change the meaning of scores, so comparability needs testing.

## One example

Three document branches receive yes scores 0.8, 0.7 and 0.2. Their total is 1.7, which is not an error: each is a separate binary judgment. A budget of two expands the first two documents. Their passages receive scores 0.6, 0.9 and 0.4. A later choice between the best two might return 0.65 and 0.35, now summing to one.

The third document was never opened. If it held the only supporting passage, better ranking among the surviving passages cannot recover it. Expansion budgets therefore affect coverage as well as cost.

## Check your understanding

Does avoiding a query-time embedding retriever eliminate all offline indexing? **No.** The hierarchy can still require parsing, grouping and summaries, potentially using embeddings. Compare evidence coverage, ordering, final grounding and total latency separately; a paper's headline improvement is not a universal guarantee.
