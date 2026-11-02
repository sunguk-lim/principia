# Materialized View

## Meaning

A materialized view is a stored query result whose refresh is separate from reading it. It avoids repeating an expensive derivation for every read, but it can lag behind the source. The key contract is which source state the stored result represents and when it will be refreshed.

## Mechanism

An ordinary logical view retains a query definition. A materialized view retains the result as well. In PostgreSQL, refreshing executes the stored query again and replaces the materialized contents. Reads obtain the stored rows until a later refresh exposes newer data. Not every implementation maintains changes incrementally; verify its actual refresh behavior.

Track source cutoff, refresh completion and publication separately. A successful refresh over an incomplete upstream table is still incomplete. Late events can change a historical total even after the next refresh. Choose a cadence from acceptable staleness and measured refresh cost rather than assuming that more frequent updates are always useful.

## One example

A stored sales summary reports $120 for store A. A new $30 qualifying sale reaches the source. The materialized summary still reports $120 until refreshed; afterward it reports $150. This is the mechanism's trade-off: inexpensive repeated reads use an older computation. A logical view reading the source might include the sale sooner, at greater repeated query cost.

A batch-derived operational table has an additional boundary. Generating new prices does not mean every physical label and checkout has applied them. Validate and publish the intended version under a consumer contract, then reconcile actual application separately.

## Check your understanding

Does a fresh refresh timestamp prove all source events are included? **No.** Upstream gaps and late data remain possible. Compare against a declared source snapshot, test refresh failure and concurrent reads, and measure staleness as well as query speed. Ask for explicit output ordering rather than relying on row order after refresh.
