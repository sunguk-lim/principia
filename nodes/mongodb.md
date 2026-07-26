---
id: mongodb
title: MongoDB
summary: "MongoDB is a distributed document database defined by how it composes its parts — records are schema-flexible BSON documents under the [[document-model]], stored by the WiredTiger engine in [[b-tree]]s with snapshot isolation via [[mvcc]] and durability via a [[write-ahead-logging]] journal, reachable through secondary [[database-index]]es and groupable into multi-document ACID [[transaction]]s, kept highly available by replica sets doing log-based [[replication]] with automatic failover via [[leader-election]], and scaled out by [[sharding]] collections across replica sets on a shard key."
type: concept
tags: [databases/document-database]
prereqs: [document-model, b-tree, database-index, mvcc, write-ahead-logging, transaction, replication, leader-election, sharding]
sources:
  - "https://www.mongodb.com/docs/manual/ — MongoDB Manual (overview)"
  - "https://www.mongodb.com/docs/manual/core/wiredtiger/ — MongoDB Manual: WiredTiger Storage Engine"
  - "https://www.mongodb.com/docs/manual/replication/ — MongoDB Manual: Replication (replica sets, oplog, write concern)"
  - "https://www.mongodb.com/docs/manual/sharding/ — MongoDB Manual: Sharding (shard keys, chunks, mongos)"
status: explained
created: 2026-07-03
updated: 2026-07-03
---

# MongoDB

## Summary

**MongoDB** is a **distributed document database** — and like PostgreSQL, the
point of treating it as its own concept is not any single subsystem, all of
which already exist as the prerequisite nodes below. The point is the
**composition**. Its data model is the [[document-model]]: records are
schema-flexible documents (encoded as **BSON**, binary JSON) grouped into
*collections*, embedding related data instead of normalizing it. Its storage
engine, **WiredTiger**, keeps collections and indexes in [[b-tree]]s, isolates
concurrent operations with [[mvcc]] snapshots, and makes writes durable with a
[[write-ahead-logging]] **journal**. Queries reach documents through secondary
[[database-index]]es, and since v4.0 multi-document ACID [[transaction]]s are
available when one document's atomicity isn't enough. Availability is the
**replica set**: leader-based [[replication]] through a logical operation log
(the **oplog**), with failover by majority-vote [[leader-election]] measured
in seconds. Scale-out is [[sharding]]: collections split by shard key into
chunks across many replica sets, routed by a front-end (`mongos`). What is
*MongoDB* is this particular bundle — document model over B-tree storage,
MVCC + journal beneath, replica sets beside, sharding above — assembled so
that each layer's guarantee is exactly what the next layer assumes.

## Grounded explanation

### Why MongoDB is its own node and not just the sum of its parts

Every prerequisite below is a general mechanism shared by many systems. What a
"MongoDB" node teaches is the **integration** — which branch of each design
fork this system takes, and why the choices reinforce one another:

- Where PostgreSQL puts relational tables and joins at the core, MongoDB puts
  the [[document-model]]'s embedded records — betting that
  tree-shaped data read in one fetch is the common case.
- That bet cascades downward: a whole record living in *one* document means
  a single-document write is already a meaningful atomic unit, which is why
  MongoDB ran for years on per-document atomicity alone and added
  multi-document [[transaction]]s late (v4.0), as the exception rather than
  the rule.
- It cascades sideways too: [[sharding]] can place each document wholly on
  one shard, so the dominant read — fetch a document by key — never crosses
  shards; and [[replication]] ships whole-document operations through the
  oplog cleanly.

A different composition of the *same* parts (say, hash-partitioned key-value
records without secondary indexes, or a relational engine with MVCC) is a
different database. MongoDB is *this* composition.

### The pieces, and the role each plays

- **Data model — [[document-model]].** Data is collections of documents:
  nested, schema-flexible trees of field-value pairs, embedded rather than
  normalized. The concrete encoding is **BSON** — binary JSON with extra
  types (dates, ObjectId, binary) and length-prefixed fields for fast
  traversal — an implementation detail of the model, not a separate idea.
  Every document carries a unique `_id`, its primary key.

- **Storage engine — WiredTiger, composing [[b-tree]] + [[mvcc]] +
  [[write-ahead-logging]].** WiredTiger is MongoDB's default storage engine —
  not a new mechanism but a package of three existing ones. Each collection
  and each index is a [[b-tree]] (documents stored in the collection's tree
  keyed by `_id`). Concurrent operations get **snapshot isolation** from
  [[mvcc]]: an update writes a new version of the document while readers
  continue on their snapshot — readers never block writers, document-level,
  not table-level, conflict granularity. Durability is the **journal**, a
  classic [[write-ahead-logging]] log: changes are appended to the sequential
  journal and fsynced, while the B-tree pages themselves are flushed lazily
  at checkpoints; crash recovery replays the journal since the last
  checkpoint.

- **Access paths — [[database-index]].** Queries that don't name `_id` would
  scan the collection; secondary [[database-index]]es (themselves B-trees,
  mapping a field's values to the documents holding them) restore O(log N)
  lookup — including indexes *into* embedded fields and arrays
  (`"author.name"`, multikey indexes), the document-model twist on a
  classical mechanism. As always, each index taxes every write.

- **Unit of work — [[transaction]].** A write to a *single* document —
  however deeply nested — is atomic by itself: the document is one B-tree
  value, one MVCC version, one journal record. Because the [[document-model]]
  embeds what a relational schema would split across tables, this
  single-document atomicity already covers most workloads — the model choice
  *is* the concurrency-control choice. When several documents must change
  together (a transfer between two account documents), multi-document ACID
  [[transaction]]s (v4.0+, cross-shard v4.2+) provide commit-or-rollback over
  WiredTiger snapshots.

- **Availability — the replica set: [[replication]] + [[leader-election]].**
  A **replica set** is MongoDB's deployment unit: one **primary** takes all
  writes, **secondaries** replay them via leader-based [[replication]]. The
  replication log is the **oplog** — a capped collection of *logical*
  operations ("in collection `orders`, set field `status` of document
  `_id=…`"). The oplog is **not** the WiredTiger journal: the journal is a
  *physical* [[write-ahead-logging]] record for crash-recovering one node's
  storage engine; the oplog is the *logical* change stream other nodes
  replay. One write therefore lands in **both** logs, serving two different
  guarantees. The **write concern** knob (`w:1` vs `w:"majority"`) sets how
  many replicas must hold an oplog entry before the client is acknowledged.
  When the primary dies, the secondaries run majority-vote
  [[leader-election]] (a Raft-like protocol with terms; candidates with stale
  oplogs are refused) and a new primary resumes in seconds.

- **Scale-out — [[sharding]].** When one replica set can't hold the data or
  absorb the writes, a collection is sharded on a **shard key** into
  **chunks** (contiguous key ranges — or ranges of the key's hash, MongoDB
  offering exactly the range/hash pair of partitioning functions), each chunk
  owned by one **shard**. Each shard is itself a full replica set — sharding
  and replication compose orthogonally. A router process, **mongos**, holds
  the chunk map (persisted in config servers): queries naming the shard key
  go to one shard; others scatter/gather. A **balancer** migrates chunks when
  shards grow uneven.

### Worked instance — one write, end to end through every piece

A ride-hailing app stores each order as one document in a sharded `orders`
collection (shard key `city`, hashed; each shard a 3-member replica set;
a secondary [[database-index]] on `status`). A driver accepts order `"o-42"`
in Seoul, and the app runs, with `w:"majority"`:

```js
db.orders.updateOne({ _id: "o-42", city: "Seoul" },
                    { $set: { status: "accepted", driver: "d-7" } })
```

1. **[[sharding]] routes.** The query names the shard key, so `mongos` hashes
   `"Seoul"`, finds in its chunk map that this hash range belongs to
   **shard B**, and forwards the update to shard B's replica set — one shard
   contacted, two untouched.
2. **[[replication]] receives.** Within shard B, only the **primary** may
   write; `mongos` delivers the update there.
3. **[[document-model]] + [[transaction]] scope the change.** The order —
   rider, route, fare, status — is *one* embedded document, so this update is
   a **single-document atomic write**: both `$set` fields take effect
   together or not at all. No multi-document transaction is needed; the data
   model absorbed it.
4. **WiredTiger applies it: [[b-tree]] + [[mvcc]].** The primary descends the
   collection's [[b-tree]] to the document (a few page reads), and per
   [[mvcc]] writes a **new version** with `status: "accepted"` — a dashboard
   query iterating orders on an older snapshot still sees `"assigned"`,
   unblocked. The `status` [[database-index]] B-tree is updated (the document
   moves from the `"assigned"` key to the `"accepted"` key).
5. **[[write-ahead-logging]] makes it durable — twice, for two reasons.** The
   change is appended to WiredTiger's **journal** (physical WAL, fsynced;
   B-tree pages flush lazily at the next checkpoint) and recorded as a
   logical **oplog** entry ("orders: set status/driver on `_id: o-42`").
6. **The majority ack.** Secondaries pull and apply the oplog entry; when one
   secondary confirms — 2 of 3 members hold it — the primary acknowledges,
   satisfying `w:"majority"`. If the primary's machine dies the next instant,
   nothing acked is lost.
7. **[[leader-election]] absorbs the failure.** Say it does die: the two
   secondaries time out on heartbeats, hold a term-numbered majority vote
   (the one holding oplog entry from step 6 is eligible; a stale member would
   be refused), and the winner resumes as primary. `mongos` retries the
   app's next write against the new primary. The app saw seconds of
   unavailability and zero data loss.

The **structure** is one BSON document in a B-tree, its MVCC version chain,
and its index entries; the **algorithm** is *route by shard key → primary →
atomic document update → journal + oplog → majority replicate → (failover if
needed)*; the **substrate** is three machines per shard times N shards, each
with dirty B-tree pages in memory and two logs on disk. That single traced
update — each prerequisite doing exactly its one job — *is* MongoDB: the
integration, not any one of the parts.

## Prerequisites

- [[document-model]] — MongoDB's data model: schema-flexible, embedded BSON
  documents in collections; the choice that makes single-document atomicity
  cover most workloads and single-shard placement cover most reads.
- [[b-tree]] — WiredTiger's storage structure: every collection and index is
  a high-fan-out balanced tree, so point lookups cost a few page reads.
- [[database-index]] — the secondary access paths over document fields
  (including embedded and array fields); O(log N) filters at the price of
  extra work on every write.
- [[mvcc]] — WiredTiger's isolation: updates write new document versions
  against reader snapshots, so readers never block writers, at
  document-level granularity.
- [[write-ahead-logging]] — the durability mechanism appearing twice: the
  WiredTiger **journal** (physical, crash-recovers one node) and, by the same
  log-then-apply principle, the oplog that replication ships.
- [[transaction]] — the ACID unit of work: implicit and single-document by
  default (the document model's dividend), explicit multi-document
  transactions since v4.0 when several documents must commit together.
- [[replication]] — the replica set's engine: leader-based replication
  through the logical oplog, with the write-concern knob trading latency
  against durability-under-failover.
- [[leader-election]] — automatic failover: majority-vote, term-numbered
  elections (Raft-like) that promote an up-to-date secondary in seconds,
  keeping the single-writer invariant without a human.
- [[sharding]] — horizontal scale-out: collections partitioned by shard key
  (range or hashed) into chunks across replica sets, routed by mongos,
  rebalanced by the balancer.

## Sources

- MongoDB Manual (overview) — https://www.mongodb.com/docs/manual/
- MongoDB Manual, "WiredTiger Storage Engine" — https://www.mongodb.com/docs/manual/core/wiredtiger/ (B-tree storage, snapshot/MVCC concurrency, journal and checkpoints).
- MongoDB Manual, "Replication" — https://www.mongodb.com/docs/manual/replication/ (replica sets, the oplog, write concern, elections).
- MongoDB Manual, "Sharding" — https://www.mongodb.com/docs/manual/sharding/ (shard keys, ranged vs. hashed sharding, chunks, mongos, the balancer).
