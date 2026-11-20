# Deletion Tombstone

## Meaning

A deletion tombstone records that a particular identity was deleted under a particular ordering rule. Removing an object and forgetting that it existed loses information: another copy may still hold the old value. The tombstone makes absence an explicit state that can defeat older data rather than an invitation to refill a missing record.

## Mechanism

[[replication]] creates multiple copies that may not receive a deletion together. Preserve the deletion's identity and ordering metadata alongside, or instead of, the old payload. A receiver compares the incoming update with the retained deletion; an update ordered before that deletion must not restore the object. The exact rule can be timestamps, source revisions or an authoritative sequence and must be specified rather than inferred from arrival time.

For an ingestion coordinator, [[single-writer-state-coordination]] can own a document's observed revision and deletion fence. A fence is the stored boundary rejecting obsolete work. Workers must check it when publishing, not merely when they start. The source's ordering must distinguish a legitimate later recreation from a delayed old edit. An unordered content hash alone cannot say which event is newer.

## One example

A document has revision 7. Deletion at revision 9 reaches the index coordinator, while a slow worker still holds revision 8. If physical removal leaves no revision record, the worker may upload revision 8 and recreate the document. Retaining a tombstone at 9 allows the coordinator to reject 8 even after its computation finishes. An authorized recreation at revision 10 is a different state transition, not evidence that 8 should have been accepted.

The same problem appears when a disconnected replica rejoins. Cassandra's primary documentation shows how a deletion marker prevents an old surviving value from being copied back during repair. Its particular grace period and compaction rules are implementation-specific, not a universal timer for every application.

Reclaiming a tombstone needs a justified bound on replica repair, queued work and replay. Physical erasure is separate from logical exclusion; an old backup must not silently restore deleted state.

## Check your understanding

Why can immediate removal resurrect data? Because a later old copy can no longer be distinguished from a valid missing-record insert.
