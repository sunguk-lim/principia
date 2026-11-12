# Transaction Retry after Conflict

## Meaning

A serialization or stale-version conflict says the previous attempt cannot safely publish under its original assumptions. A retry is a new attempt at the intended operation using current information. Repeating only the final write can preserve the very stale calculation that caused the conflict.

## Mechanism

Under [[optimistic-concurrency-control]], classify the failure, discard the failed speculative result, read a fresh consistent state and rerun the logic that chooses values and statements. Keep a stable operation identity across attempts, but distinguish attempt identities. Bound retries, use contention backoff where appropriate and return an explicit unresolved outcome when progress fails.

A [[tool-call-execution-contract]] separates database rollback from remote effects. If a payment may already have happened, refreshing the local database does not authorize sending it again. Query an execution receipt or use the external system's documented duplicate-suppression contract. Permanent validation failures and revoked permissions are not transient conflicts to hammer until something succeeds.

## One example

An invented quota has ten slots and two free. A worker reads two free slots and plans to allocate two. Another commits an allocation first. The original worker's version check fails. It must re-read the remaining one slot and reconsider the two-slot request; resubmitting the old allocation with an updated version would violate the quota. The correct result may now be rejection rather than an eventual successful retry.

## Boundaries and check

PostgreSQL explicitly requires retrying the complete transaction, including the logic deciding values and SQL. Not every uniqueness error is transient. Test repeated conflicts, changed eligibility, crash after external success and exhausted retry budgets. Record attempts and final observed effects; a successful retry should preserve intent and invariants, not just eliminate an error message.


## Check your understanding

Can a retry reuse old computed values with a fresh version? No; it must reconsider the complete decision against current state.
