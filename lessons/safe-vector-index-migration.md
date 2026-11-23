# Safe Vector-Index Migration

## Meaning

A vector-index migration changes a deployed representation without silently mixing incompatible evidence or losing source updates. The unit being released is a compatible **query encoder, document encoder, index and retrieval configuration**, not just a new index name. Keeping queries available and keeping evidence current are separate obligations.

## Mechanism

[[vector-index-reconciliation]] establishes agreement with authoritative source identities and versions. Begin with an identified source boundary, build a target index or a separate vector field, and record the document/query model pair, preprocessing, dimensions, distance rule and schema. Matching dimensions is necessary for some interfaces but not evidence of a shared coordinate system. Do not compare vectors from unrelated models merely because both contain the same number of entries.

Choose a concurrent-change policy before backfilling. A write pause simplifies the boundary but delays updates. A consistent snapshot plus replay needs a retained change position and coverage of creates, edits, deletions and permissions. Two live ingestion paths reduce the pause but introduce partial-write failures and extra work; writing both is not automatically one transaction. Reconcile the target at the intended cutover revision, not only at the date the backfill started.

Use [[measurement]] to define acceptance before switching: representation coverage, authorized retrieval, judged relevance, latency, failure handling and operating cost. Exercise the actual query-vectorization identity and network path. Similarity scores and thresholds may change with a model, so carry over a threshold only after validation.

## One example

An invented source snapshot contains 100 documents at change position 500. While model B builds its target, position 501 edits D7, 502 deletes D8 and 503 revokes one reader's access to D9. A completed backfill still reflects position 500. Replay and validate all three changes before claiming the target is caught up to 503. D8 must disappear, D9 must enforce current permissions, and the query path must use B's compatible query encoder.

| Release state | Search target | Query representation | Required evidence |
| --- | --- | --- | --- |
| Baseline | Index A | Encoder A | Current production baseline |
| Candidate | Index B | Encoder B | Coverage and replay through 503 |
| Cutover | B selected by routing | B selected by the same release contract | Acceptance gates passed |
| Rollback | A, if still valid | A | A's freshness and permission state rechecked |

An alias can simplify routing, but its service-specific update boundary does not atomically switch an independently configured query encoder. Bind both in an application release or use a compatible server-side vectorization contract. Test a stale client that sends A vectors to B and reject it explicitly.

## Check your understanding

Is a successful target load enough to switch? No. It proves neither current source coverage nor a compatible query path.
