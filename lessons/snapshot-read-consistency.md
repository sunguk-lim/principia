# Snapshot Read Consistency

## Meaning

A snapshot read answers a query against one coherent version of state. It differs from merely reading old values: the version boundary must apply to all facts used in the result. A snapshot can be internally consistent while intentionally stale relative to current state.

## Mechanism

Choose a committed revision or the database's documented read-view boundary, then resolve related data inside that view. The [[transaction-isolation]] contract determines whether the view is fixed for a statement, a transaction or an explicit historical revision. Do not assume two independent requests share a snapshot merely because they run close together.

For a versioned graph, nodes and edges should resolve under the same revision. Cache entries and later lookups must carry that identity or explicitly revalidate freshness. A view assembled from one revision's component and another revision's decision can invent a contradiction that never existed in any committed version. Conversely, a coherent snapshot can preserve a real earlier mistake; consistency is not factual truth.

## One example

An invented revision R3 contains component C with store=Redis and decision D saying Redis is selected. Revision R4 atomically changes C to Postgres and supersedes D with a Postgres decision. A reader pinned to R3 sees both old facts; one pinned to R4 sees both new facts. Reading C from R4 but D from an unversioned R3 cache yields a mismatched account. Naming the query's revision exposes which result is intended.

## Boundaries and check

Snapshot consistency does not guarantee serializable writes, current authorization or freshness. An old snapshot may contain data the caller is no longer permitted to see, so enforce the applicable access policy separately. Retention and garbage collection determine which historical views remain available. Test concurrent updates between related reads, cache-version mismatches, missing revisions and permission changes. PostgreSQL's statement-versus-transaction views and Git's committed trees are concrete version-boundary examples, not interchangeable APIs.


## Check your understanding

Can a coherent old snapshot be stale or wrong? Yes; consistency, freshness and truth are separate properties.
