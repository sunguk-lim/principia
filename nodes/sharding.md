---
id: sharding
title: Sharding (Horizontal Partitioning)
summary: "Splitting one large dataset horizontally across many machines by a shard key — each shard owns either a contiguous range of key values or a hash-of-key bucket — so storage and write throughput scale by adding machines, at the cost of routing every query to the right shard, rebalancing data as machines join, and losing cheap cross-shard operations."
type: concept
tags: [databases/distributed]
prereqs: [key-value, hash-map, replication]
sources:
  - "M. Kleppmann, Designing Data-Intensive Applications (O'Reilly, 2017), ch. 6 — Partitioning"
  - "https://www.mongodb.com/docs/manual/sharding/ — MongoDB Manual: Sharding"
status: explained
created: 2026-07-03
updated: 2026-07-03
---

# Sharding (Horizontal Partitioning)

## Summary

[[replication]] copies the *whole* dataset onto every machine, so it never
lets the data outgrow one machine. **Sharding** (horizontal partitioning) is the
complementary move: **split** the dataset so that each machine — each
**shard** — owns only a *subset* of the records, and the union of the shards
is the full dataset. The split is driven by a **shard key**: a chosen field of
each record, treated exactly as a key in a [[key-value]] mapping — the
record's address for placement purposes. A **partitioning function** maps each
key to its owning shard, in one of two standard ways: **range partitioning**
(each shard owns a contiguous interval of the key's sort order — good for
range scans, vulnerable to hotspots) or **hash partitioning** (a hash of the
key picks the shard, the [[hash-map]] bucket idea scaled from array slots to
machines — spreads load evenly, destroys key adjacency). Sharding is what
makes total capacity and write throughput **scale by adding machines**; its
price is a router in front of every query, **rebalancing** when machines
join or leave, and the loss of cheap operations that span shards.

## Grounded explanation

### The problem sharding solves — and the one it doesn't

A single machine bounds a database twice: **capacity** (the dataset must fit
its disk) and **write throughput** (every write consumes its CPU and I/O;
[[replication]] does not help, since *every* replica must apply *every*
write).
Sharding attacks both by dividing the records: with the data split N ways,
each shard stores ~1/N of the bytes and absorbs ~1/N of the writes, so both
grow linearly with machine count. What sharding does *not* provide is fault
tolerance — losing a shard loses that subset outright — which is why real
deployments replicate *each shard* (the two mechanisms compose; they don't
compete).

### The shard key, and the two partitioning functions

Placement needs a deterministic rule: *given a record, which shard owns it?*
The rule reads one field — the **shard key** — and treats the dataset as a
[[key-value]] mapping from that key to the record, then partitions the key
space:

- **Range partitioning.** Sort the key space and give each shard a contiguous
  interval: shard 1 owns keys A–H, shard 2 owns I–P, shard 3 owns Q–Z.
  Adjacent keys live together, so a **range query** ("all keys between K1 and
  K2") touches only the one or two shards whose intervals intersect it. The
  danger is **skew**: if writes concentrate in one interval, one shard does
  all the work.
- **Hash partitioning.** Compute `hash(key) mod N` (in spirit) and let the
  bucket number pick the shard — precisely a [[hash-map]]'s
  key-to-bucket-index step, with machines in place of array slots. A good
  hash scatters even adjacent keys uniformly, so load spreads regardless of
  the key distribution. The same scattering destroys adjacency: a range query
  now has no locality and must ask **every** shard (scatter/gather).

The trade is symmetric and unavoidable: range partitioning preserves order
and risks concentration; hash partitioning guarantees spread and forfeits
order. The right choice is a property of the workload's queries, not of the
data.

### Routing and rebalancing — the machinery sharding obligates

Two components exist *because* the data is split. A **router** holds the
key→shard map; every client query passes through it (a query *by* shard key
goes to exactly one shard; a query that doesn't mention the shard key must be
scattered to all shards and gathered). And **rebalancing** handles change:
when a shard fills up or a machine is added, ownership of some key
sub-ranges — MongoDB calls the movable units **chunks** — migrates to the new
machine, and the router's map is updated. Practical systems therefore
partition into many more chunks than machines, so rebalancing means *moving
some chunks*, never re-hashing the world (the reason naive `mod N` is only
"in spirit": changing N would remap nearly every key).

### Worked instance — one dataset, both partitionings, one hotspot

A `users` collection of 90 million records is split across shards **S1 S2
S3**, shard key `user_id`, ids issued sequentially (new user = highest id yet).

- **Range partitioning:** S1 owns ids 1–30M, S2 owns 30M–60M, S3 owns
  60M–90M. A range query — "users 45,000,000–45,100,000" — goes to S2 alone:
  one shard, one interval scan. But **every new signup** has an id above 60M,
  so **every insert lands on S3**: two shards idle while one melts. The
  monotonically increasing key is the classic range-partitioning hotspot.
- **Hash partitioning:** the router computes `hash(user_id)`; ids 90,000,001,
  90,000,002, 90,000,003 hash to (say) S2, S1, S3 — consecutive signups
  scatter across all three shards and insert load is ~1/3 each. The same
  scattering breaks the range query: ids 45,000,000–45,100,000 are now spread
  over all shards, so the query is sent to S1, S2, *and* S3 and the results
  merged — scatter/gather instead of one interval scan.
- **Routing either way:** "fetch user 51,203,441" names the shard key, so the
  router sends it to exactly one shard (S2 under range; whichever shard the
  hash picks under hash). "Find users named alice" does not mention
  `user_id` — under *both* schemes it is scattered to all three shards.

Same data, same machines — the partitioning function alone decides which
queries stay cheap and where the load concentrates.

## Prerequisites

- [[key-value]] — the abstraction the shard key imposes: for placement, every
  record is addressed by one field's value, and the partitioning function is
  a mapping over that key space.
- [[hash-map]] — the mechanism hash partitioning scales up: hash the key,
  take the result as a bucket index — with shards standing where the hash
  map's array slots stood, inheriting both the uniform spread and the loss of
  key ordering.
- [[replication]] — the complementary mechanism sharding is defined against:
  replication copies the whole dataset for availability but scales neither
  capacity nor writes, so real deployments shard for scale and replicate each
  shard for fault tolerance — the two compose.

## Sources

- M. Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), ch. 6 "Partitioning" — range vs. hash partitioning, skew and hotspots, rebalancing, request routing.
- MongoDB Manual, "Sharding" — https://www.mongodb.com/docs/manual/sharding/ (shard keys, ranged vs. hashed sharding, chunks and the balancer, mongos routing).
