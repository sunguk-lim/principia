# Listwise Passage Reranking

## Meaning

Listwise passage reranking orders a group of retrieved passages in one joint judgment. It is a ranking procedure, not a particular model architecture or training objective.

## Mechanism

Assign stable identifiers to candidates and ask the model for their order. Validate the output as a permutation: every expected identifier exactly once, no invented identifiers. This protects the interface but cannot prove that the order is relevant or that the selected passages support an answer.

When the group is too large, overlapping windows make bounded local judgments. A tail-to-head pass can move useful candidates forward. Window boundaries still constrain which candidates are considered together, and several passes may produce different orders.

## One example

Start with A,B,C,D,E,F. A tail window containing C,D,E,F returns E,C,F,D. The list becomes A,B,E,C,F,D. Move the window two places toward the front: A,B,E,C returns E,B,A,C. The final list is E,B,A,C,F,D.

E moved to the front, but F never appeared beside A or B in this pass. The result is not proof that a global comparison would place F below both. Window size, stride and initial order are part of the algorithm, not irrelevant implementation details.

## Check your understanding

Can valid permutation syntax certify a good evidence order? **No.** Test relevance, evidence sufficiency and position sensitivity separately. Shuffle inputs, check unknown/duplicate/missing IDs, compare equal candidate pools and budgets, and record time and token cost. Candidate recall is an upstream limit: a missing supporting passage needs additional retrieval, not a more confident permutation.
