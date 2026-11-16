# Vector Index Reconciliation

## Meaning

Vector-index reconciliation compares a derived search index with authoritative versioned records and repairs missing, stale, deleted or unauthorized evidence.

## Mechanism

Choose an authoritative document identity and desired version. A version must cover the content and transformations that determine indexed units; permissions and deletion state may require separate revisions. [[background-document-indexing]] stages derived units. Reconciliation compares desired identities, active versions, unit coverage and access state with observed index records. Classify missing, stale, extra and incomplete entries separately.

A repair can race with another update. Use [[optimistic-concurrency-control]] at the authoritative publication boundary: publish the repaired version only if the assumptions under which it was built still hold. A remote vector store may not support that same atomic check. In that case combine version-bound staging with an authoritative active-version filter or another explicit coordination protocol; do not pretend two services share one local transaction.

Deletion needs durable evidence that older jobs cannot undo. A retained deletion revision, often called a tombstone, lets workers reject an old insert even after the content record disappears. Permission changes additionally require [[retrieval-authorization-boundary]] before evidence enters context. Repairing stored metadata eventually is not a substitute for enforcing a current access decision when that is the safety contract.

## One example

Source D is at version eight, but the index holds version seven and two of version eight's three units. Queue depth is zero because a worker acknowledged early. The reconciler stages all three version-eight units, validates coverage and requests activation. Meanwhile D advances to version nine. The conditional activation fails; version eight must not become current just because its repair finished last. If D was instead deleted at revision nine, a retry of the old insert must respect that deletion.

## Validation and check

Inject lost events, duplicate delivery, out-of-order completion, deletion during a scan and permission revocation. Measure discrepancy age, time to repair, stale retrieval and forbidden evidence, not just job success. Bounded scans have a freshness window; a live changing corpus is not one atomic snapshot unless the source supplies that contract. AWS grounds the dual-write and duplicate-delivery boundary; Azure supplies an implementation example of index maintenance. The repair protocol here is an independent systems design, not a guarantee of either service. Does reconciliation make every read current? No: explicitly define the permitted lag and read-side controls.
