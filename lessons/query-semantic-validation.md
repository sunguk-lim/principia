# Query Semantic Validation

## Meaning

A query can parse, execute and obey every access policy while answering the wrong question. Query semantic validation checks the meaning of its result: which entity each row represents, which records qualify and how values combine. It is distinct from syntax validation, query-plan efficiency and authorization.

## Mechanism

Specify output grain, keys, units, time boundary and treatment of nulls and duplicates before judging generated [[sql]]. Grain means the entity represented by one output row, such as one order rather than one order line. Build small fixtures that make a mistaken join or filter produce a different result from the specification. An independently derived reference result is stronger than a second query copied from the same mistaken assumptions.

[[metamorphic-testing]] checks justified relationships when exhaustive expected outputs are difficult. Reordering input rows should not change an unordered total; adding an excluded record should not change a filtered result. These relations depend on the business contract: duplicating a transaction is not an invariant if it represents a second real purchase.

## One example

Two hypothetical orders have amounts 30 and 50. Their intended total is 80. The first has two line items and the second has three. Joining orders to lines and summing the order amount repeats values, giving 2×30 + 3×50 = 210. Every returned row may be authorized and every join condition syntactically correct, yet the result is wrong because the aggregation grain changed.

Compute the order total before the one-to-many join, or aggregate line-level values according to the actual requirement. SUM(DISTINCT amount) is not a general repair: two different orders can have equal amounts and should both count. Add such an equal-amount case to prevent a superficially plausible fix from passing.

## Check your understanding

Is a successful query enough evidence of a correct metric? No; validate the result's intended grain and aggregation semantics.
