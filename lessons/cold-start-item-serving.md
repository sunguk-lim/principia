# Cold Start Item Serving

## Meaning

A new catalog item often lacks a learned ID embedding. A safe ranking path must still produce bounded features and meet a latency target.

## Mechanism

Use content and taxonomy attributes, an unknown embedding, or a versioned online metadata lookup. Feature hashing bounds vocabulary but does not create semantic similarity. Set deadlines and fallbacks for the online path.

## Example

A new film can use genre and description features before any interactions. A category unknown vector avoids a crash, but cannot distinguish two films in that category; a failed metadata store needs a measured fallback.

## Boundaries and trade-offs

A fallback has two jobs: keep the inference contract valid and retain enough item meaning to rank usefully. A global unknown vector solves only the first. Category vectors add coarse meaning but may reinforce popular-category bias. Content features can distinguish items without interactions, yet their extraction and freshness must be controlled. Online stores can supply current metadata, but they place a dependency inside the response path.

## Validation

Create a chronological replay in which candidate items appear only after training. Track the rate of unknown IDs and metadata misses by item age. Compare global unknown, taxonomy fallback, and content-derived representations while holding the ranking model and traffic distribution fixed. For online lookups, inject delays and outages and verify deadlines and fallback semantics. Check warm-item as well as cold-item quality; a clever cold-start path should not silently damage familiar items.

## Understanding check

Why can increasing retraining frequency fail to solve a metadata lookup outage or cold-item feature gap?
