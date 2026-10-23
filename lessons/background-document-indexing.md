# Background Document Indexing

## Meaning

Background document indexing separates accepting a document from making it searchable. A durable work record drives extraction, chunking, representation construction, and index writes after the upload request returns. A progress notification is only a view of this process, not proof that searchable evidence is complete or current.

## Mechanism

Record document identity, content version, access scope, and a job identity before beginning slow work. A [[transactional-outbox]] can couple a local metadata change with work-delivery intent; separate object storage still needs its own successful-write and reconciliation boundary. Workers extract permitted text or pages, apply [[retrieval-chunking]], produce representations and write them into a [[vector-database]]. Keep source/version/page identity through every stage using [[dataset-lineage]].

Retrying a worker must not create duplicate evidence or overwrite a newer version with stale output. Key staged units by source version and unit identity, track completed work, and reject results from a superseded version. Choose a visibility rule: publish only when all required units are validated, or explicitly expose bounded partial coverage. A document marked uploaded is not necessarily indexed. A counter saying “20 pages processed” does not by itself prove vector writes, metadata, permissions and retrieval all agree.

## One example

Document D version 4 has three pages. Worker one finishes pages 1 and 2 and then crashes. A retry discovers their completed, version-bound records and processes page 3 without duplicating the first two. Before publication, version 5 arrives. If the active version is now 5, the old worker must not publish version 4 as current merely because it completed last. A conditional version check and staged-to-active publication step make that race explicit.

Deleting a document or revoking access must affect source records, staged work, index entries and relevant caches. A late retry must not resurrect deleted evidence. Progress events may be lost or repeated; clients should reconcile against authoritative job state rather than advance correctness state from notifications alone. Model outages, parsing failures and protected PDFs require visible per-stage failure outcomes, not fabricated success.

Compare synchronous and queued ingestion on upload latency, time-to-searchable, partial-failure recovery, stale-version retrieval, duplication, permission leakage and operational cost. Test crashes at each durable boundary and simultaneous updates. Azure indexer documentation supplies a primary example of out-of-request extraction and index maintenance; it explicitly warns that indexing can contend with query resources. Asynchronous ingestion does not imply separate or free compute, nor identical state or deletion guarantees across implementations.

## Check your understanding

If a background task reaches 100% page extraction, is the new document necessarily safe to retrieve? No. Validate index writes, version, coverage and permissions under an explicit publication rule.
