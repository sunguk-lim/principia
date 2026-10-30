# Pointwise Passage Reranking

## Meaning

Pointwise passage reranking scores one query-passage pair independently, then sorts the candidates. It operates inside the candidate boundary of a [[retrieval-evidence-gate]]: it can improve ordering but cannot create a missing passage.

## Mechanism

A cross-encoder processes query and passage tokens together using [[transformer-attention]], allowing their representations to interact before producing a score. This is one possible model architecture, not the definition of pointwise ranking. A prompted language model can also provide one-passage scores. Training objective, architecture and inference-time ranking procedure should not be conflated.

Independent pairs can be batched. However, their output scores must be comparable within the query. Sorting requires meaningful relative scores; using a fixed confidence threshold additionally requires evidence that its acceptance errors are acceptable. Scores need not be calibrated probabilities merely to rank candidates.

## One example

For a return-deadline question, retrieved passages A, B and C receive illustrative scores 0.2, 0.9 and 0.6. B states the deadline, C describes packaging, and A gives company history. A two-passage context budget keeps B and C. If B was absent from retrieval, reranking A and C still cannot answer the deadline question.

Now suppose another highly scored passage describes an older policy. High relevance does not resolve its conflict with a newer policy. Keep source dates and versions, then evaluate answer support separately from ordering.

## Check your understanding

Does a score of 0.9 establish a 90 percent chance that a passage is true? No. Inspect the scoring contract and validation. Compare against the initial order on held-out questions, measuring evidence retention, answer quality, latency and cost at the same candidate depth and context budget.
