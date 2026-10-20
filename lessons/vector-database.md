# Vector Database

## Meaning

A vector database turns stored [[embedding]] vectors into an operated similarity-search service. It keeps identifiers, provenance and metadata with the coordinates and manages persistence, updates, deletion and filtering. It may be a specialized product or a feature inside a relational database.

## Mechanism

[[nearest-neighbor-search]] ranks candidates under a chosen distance. Exact search evaluates eligible candidates and returns the true nearest set under its numeric contract. It is often a useful production choice for small collections or selective filters. Approximate indexes explore a smaller candidate region, trading recall for speed, memory and update costs.

pgvector documents both exact and approximate search inside PostgreSQL. Therefore neither a dedicated product nor approximate search is definitional. The important database contract is serving the correct eligible evidence under change, not simply making a geometric query fast.

The query plan must also specify when permission and metadata filters apply. Retrieving a small global candidate set and filtering afterward can leave too few results even though more eligible neighbors exist. Some plans expand the search; others need different index or filtering choices. Verify actual behavior rather than assuming a top-k request always returns k permitted records.

## One example

Vectors A=(0,0), B=(1,0), C=(2,0), D=(3,0) are queried with q=(1.2,0). Distances are 1.2, 0.2, 0.8 and 1.8, so global exact top-2 is B,C. If only A,C are permitted, exact filtered top-2 is C,A. Filtering the global top-2 yields only C, a different result.

Compare approximation against exact search using recall and downstream answer quality, plus latency, memory, build and update cost. Keep vector-model versions compatible and propagate source deletion and permission changes. Similar vectors can still differ in decisive factual content.

## Check your understanding

**Question:** Is a vector database necessarily a separate approximate-search product? **Answer:** No. Exact or approximate vector search can live inside a relational store; lifecycle, eligibility and quality contracts determine whether the system meets the task.
