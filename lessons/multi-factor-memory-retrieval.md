# Multi-Factor Memory Retrieval

## Meaning

A memory ranker can combine three different questions: is the record relevant to this query, important under a stored rubric, and recently used? The combined score is a selection policy, not a proof that similarity retrieval is inadequate for every task. It operates only after permission and validity checks have defined eligible records.

## Mechanism

For memory m, let R, I and Q be normalized recency, importance and relevance values, respectively. Choose nonnegative weights w_R, w_I and w_Q and compute S(m)=w_R R+w_I I+w_Q Q. [[access-based-memory-decay]] defines one recency feature; [[memory-importance-estimation]] supplies stored importance; [[cosine-similarity]] can measure query–memory embedding relevance. Rank eligible items and include a subset that fits the available context, accounting for record length and redundancy.

The Generative Agents paper min-max scales each feature to [0,1] and uses equal weights. These are experiment choices, not universally calibrated settings. Candidate-set normalization can change scores when an unrelated extreme record appears. A constant feature has no range and needs an explicit fallback. Very high importance must not let an irrelevant record crowd out necessary evidence indefinitely.

## One example

Use hypothetical already-normalized features. Memory A has (R,I,Q)=(0.9,0.2,0.8); B has (0.3,0.9,0.7). Equal-weight sums are 1.9 and 1.9, requiring a tie rule. Doubling the importance weight gives A=2.1 and B=2.8. That preference change follows from the policy, not newly discovered facts. If B is unauthorized for this caller, remove it before ranking rather than merely lowering its score.

## Check your understanding

Does equal weighting mean the three raw features have equal influence? Only after specifying their normalization and candidate distribution.
