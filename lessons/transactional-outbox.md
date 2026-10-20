# Transactional Outbox

## Meaning

A transactional outbox prevents a local state change and its required notification from becoming an unsafe pair of independent writes. It commits the state change and an outgoing-event record together, then sends the committed event later. It does not atomically commit arbitrary remote effects.

## Mechanism

Within one [[transaction]], update the domain record and insert an event into an outbox table. Either both writes commit or neither does. A separate relay reads committed outbox records and delivers them to a [[queue]] or destination, retrying when delivery is uncertain.

The relay can crash after sending but before marking delivery complete. Therefore a receiving system can see duplicates. An [[idempotent-operation-key]], stable event ID or equivalent consumer-side record must coordinate duplicate detection with the receiver's actual state change. Recording a message as processed before a non-atomic external action only moves the ambiguity to another boundary.

Ordering is another contract. If one entity emits ordered state transitions, preserve their sequence through relay concurrency and retries. Outbox rows also need observability, bounded retry policy, retention and recovery from a stopped relay. Keeping an event forever is not proof it was delivered; deleting it after an uncertain send can lose the notification.

## Worked example

An order changes from pending to confirmed. One database transaction updates order 42 and inserts event `order-42-confirmed-v3`. If the transaction rolls back, neither confirmation nor event exists. If it commits and the process dies, the relay can discover and send the event later.

Suppose the destination accepts the event but the relay loses the acknowledgement. It sends the same event again. A consumer that atomically records the event ID with its local update applies that update once. If the consumer instead sends an email through another service, it also needs that service's deduplication or reconciliation contract; the outbox alone did not make email exactly-once.

AWS's pattern guidance explicitly calls out duplicate messages and idempotent consumers. Test rollback, concurrent relays, lost acknowledgements, per-entity ordering and crashes at both local and remote boundaries.

## Check your understanding

**Question:** What is atomic here? **Answer:** Local business state plus delivery intent, not the complete cross-service effect.
