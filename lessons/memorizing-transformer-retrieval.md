# Memorizing Transformer Retrieval

## Meaning

A memorizing transformer stores earlier key-value representations and selects old states by approximate similarity. This is direct retrieval, unlike passing only a recent recurrent summary.

## Mechanism

Local attention handles nearby tokens; an external nearest-neighbor lookup adds selected distant representations. Search error, eviction, representation drift, and access latency can all limit the gain.

## Example

A rare name introduced early may be found again if its stored key matches a later query. If the query misses or the memory was evicted, accepting a long input does not make the detail recoverable.

## Boundaries and trade-offs

This memory stores representations rather than original sentences. The current query selects a few candidates, which reduces the amount of old context attended directly but introduces a search problem. Approximate nearest-neighbor search can miss, and a retrieved vector may no longer mean the same thing if the encoder changes. Eviction and access policy matter whenever the store outlives a short run.

## Validation

Test with long-range facts at controlled distances, and include irrelevant but similar distractors. Compare retrieval recall, task answer accuracy, latency, and storage footprint. Ablate memory size and nearest-neighbor quality separately. A failed answer might reflect a missing stored state, a search miss, or incorrect use of a correct result; these are different fixes. Do not equate large memory capacity with faithful retrieval or authorization to reuse old information.

## Understanding check

How would you separate a retrieval-selection benefit from simply giving the model more memory?
