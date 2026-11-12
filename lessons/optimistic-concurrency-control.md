# Optimistic Concurrency Control

## Meaning

Optimistic concurrency control lets a worker compute without holding a long-lived exclusive lock, then rejects publication when the assumptions it read are stale. Optimism concerns when conflict is checked, not a willingness to accept lost updates.

## Mechanism

Read data with a version. Compute a proposed change and publish only if the current version still matches. For a single record, an [[atomic-operation]] can combine the comparison and write; separate “check then update” calls leave a race. A SQL-style condition such as UPDATE ... WHERE id=:id AND version=:expected can implement a row-scoped compare-and-update when the affected-row count and transaction semantics are handled correctly.

The broader [[concurrency-control]] objective can include read sets, predicates and multiple rows. One record version cannot protect a cross-record invariant unless every relevant change invalidates that version or another transactional mechanism validates it. Version validation is not automatically full serializability. Keep external effects outside speculative execution or reconcile them separately.

## One example

A record begins at version 7 with count=10. Two workers each propose adding one. A atomically writes count=11, version=8 conditional on version 7. B's same condition affects zero rows and must not report success. B re-reads 11 at version 8, recomputes 12 and can attempt a new conditional write. Simply replacing the expected version while keeping a stale absolute value of 11 would still lose the second increment.

## Boundaries and check

Define conflict scope, retry limits and behavior under repeated contention. Versions can be counters or immutable revision identities; timestamps require a reliable equality contract and are not intrinsically safe. Test both competing writes and changes to read-only dependencies. A failed comparison means the proposal needs reconsideration, not that the user's intended operation is necessarily invalid.


## Check your understanding

Can the version be checked in one call and written in another? Not safely without an indivisible validation-and-write boundary.
