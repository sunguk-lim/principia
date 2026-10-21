# User-Data RAG Integration

## Meaning

User-data RAG integration connects an authorized external source to retrieval and generation while preserving identity, permissions, revisions and evidence. A working connector is only the beginning: indexed coverage, searchable content and correct answers are separate outcomes.

## Mechanism

The application receives delegated source access, imports permitted resources, preserves resource identity and revision, parses searchable units and enforces the caller's current permissions before evidence enters the prompt. It then retrieves, assembles context and checks answer support. A stale permission label can disclose content even if ranking and generation are excellent. Deletes and revocations need explicit visibility rules rather than waiting indefinitely for a successful refresh.

Pre-indexing pays ingestion and storage work before queries; query-time access asks the upstream source when needed. The former can amortize repeated searches but adds freshness and deletion lag. The latter can see newer information but depends on live authorization, availability, rate limits and latency. A tool protocol does not decide between these designs, and hybrid systems are possible.

## One example

A source changes at 10:00, its index refreshes at 10:20 and a question arrives at 10:10. An indexed query may return the prior revision, while a live query can return the new one if exposed by the source. During an upstream outage, an authorized cached revision may instead be more available. State revision and age. Revoked private content cannot remain visible just because the cache is operationally convenient.

Test permission crossover, source deletion, scope revocation, malformed parsing, changed revisions, index failures and prompt injection. Compare permitted recall, answer support, update lag, latency and cost using the same corpus and queries. Verify configuration-specific permission-sync contracts instead of assuming all connectors inherit every source ACL.

## Check your understanding

Does a successful source connection prove its private documents are safely searchable? No. Coverage, current permissions, freshness and prompt admission must each be verified.
