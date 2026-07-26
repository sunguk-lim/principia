---
id: key-value-store
title: Key–Value Store (key-value database)
summary: A database whose data model is the key-value mapping — store and fetch opaque values by unique key — made durable, networked, and concurrent; values are opaque and the only access path is the key, a restriction that buys horizontal scale by partitioning the keyspace across machines.
type: concept
tags: [databases/key-value-store]
prereqs: [key-value, atomic-operation]
sources: []
status: explained
created: 2026-06-29
updated: 2026-06-29
---

# Key–Value Store (key-value database)

## Summary

A **key–value store** (or key–value database) is a database whose data model is
the [[key-value]] mapping: you store a *value* under a unique *key* and later
fetch, overwrite, or delete it by naming that key — nothing else. What lifts it
from the in-process mapping (a language's `dict`) to a *database* is everything
around that model: the data is **durable** (it survives a restart, written to
storage rather than living only in one process's memory), reachable **over the
network** by many clients at once, and kept correct under that concurrency. The
defining bargain is that the store treats each value as an **opaque blob** — it
does not look inside values, index their contents, or let you query by them; the
*only* way to reach a value is its key. That restriction is not a weakness but
the source of the store's signature strength: because every operation names
exactly one key, the keyspace can be split across many machines, so the store
scales to enormous size and request rates that a query-rich relational database
cannot match. Redis, DynamoDB, and etcd are key–value stores.

## Grounded explanation

**Start from the data model we already have.** A [[key-value]] mapping is a set of
uniquely-keyed pairs with three operations — *get*, *set*, *delete*, each
addressed by the key. A key–value store is that exact interface promoted into a
*database*: the same get/set/delete by key, but now the pairs outlive the process
that wrote them, sit on a server that many clients reach across a network, and
stay consistent while those clients hit them simultaneously. The data model is
unchanged; what is added is durability, remote access, concurrency control, and
scale. So the concept is *not* a new way of organizing data — it is the key-value
mapping made into durable, shared infrastructure.

**Why it exists as its own kind of database — the two things it is not.** Place it
between two neighbors. On one side is an in-process [[key-value]] mapping — a
`dict` — which has the right access model but forgets everything when the process
stops and is private to that one process; it is not a database. On the other side
is a *relational* database, which is durable and shared but organizes data into
tables with columns and lets you ask rich questions: filter by any field, join
rows across tables, aggregate. The key–value store deliberately gives all of that
up. It offers no joins, no secondary indexes on value contents, no query language
beyond "fetch the value for this key." The question it answers is only ever
"given this key, what is its value?" The reason to accept so spare an interface is
what the spareness buys, which is the next point.

**The defining trade: opaque values + key-only access → horizontal scale.** Because
the store never inspects a value and every operation targets exactly one key, the
keyspace can be **partitioned** (also called *sharded*) across many machines: run
the key through a fixed function that maps it to one of `N` servers — the same
*compute-the-location-from-the-key* idea the [[key-value]] mapping already uses
internally, now lifted from array slots to whole machines — and that key's pair
lives on, and is served by, exactly that server. A request routes to one
partition and touches no other. Crucially, since there are no joins or
cross-key queries, **no operation ever needs data from two partitions at once**,
so adding machines adds capacity almost linearly with no coordination between
them. This is the payoff the relational database cannot easily match: its joins
and multi-row queries *do* span the whole dataset, which is exactly what resists
being chopped across machines. The key–value store trades query power away and
receives near-unlimited horizontal scale in return — the same shape of bargain a
vector database makes (give up exactness, gain speed), here *give up rich
queries, gain scale*.

**Staying correct under concurrency — atomicity per key.** Many clients reach the
same server and may touch the same key at the same instant: two clients both
incrementing a counter stored under `"visits"`, say. If their read-modify-write
sequences interleave, one increment is lost. A key–value store prevents this by
guaranteeing that operations on a single key are **atomic** — indivisible, as if
they happened one at a time. This is the [[atomic-operation]] guarantee lifted up
a level: where [[atomic-operation]] makes a read-modify-write on one *memory
location* indivisible against other threads, the store makes an operation on one
*key* indivisible against other clients (a single `SET`, or a compare-and-set that
updates the value only if it still holds an expected one). The same invariant —
*once an operation on this slot begins, no other operation on it can interleave* —
is what makes a shared key–value store safe to hammer concurrently; without it the
"shared by many clients" property would corrupt data rather than serve it. Per-key
atomicity is cheap precisely because of the partitioning above: one key lives on
one machine, so guaranteeing its operations don't interleave is a local matter, not
a distributed agreement across servers.

**Durability — the "database" in key-value database.** The pairs are written to
durable storage (disk or its modern equivalents), often by first appending each
write to a sequential log before applying it, so that a crash or restart loses
nothing: on restart the store replays its storage and the keyspace returns intact.
This is the property that most separates the store from the `dict` it resembles,
and it is kept as prose here because it is shared by every database, not special to
the key-value model.

**Worked instance — a partitioned session store.** A web service must remember each
logged-in user's session. Model it as a key–value store: the **key** is a session
id like `"sess:8a3f"`, the **value** is an opaque blob — the serialized session
(user id, cart contents, expiry). The service never asks the store "find all
sessions for user 42" (that would need to look *inside* values — exactly what a
key-value store refuses); it only ever does `get`, `set`, and `delete` by session
id, which is all a session needs.

Run it across `N = 2` servers, `A` and `B`. To store `set("sess:8a3f", blob)`, the
store hashes the key and reduces it to a server — suppose it lands on `A` — and the
pair lives on `A`. A later `get("sess:8a3f")` hashes the same key, routes to `A`
again, and returns the blob from there, never consulting `B`. A different session
`"sess:1c20"` might hash to `B`; it is served entirely by `B`. The two servers
share nothing and need no coordination, because no request ever spans both — so to
handle twice the sessions you add two more servers and re-spread the keys, and
throughput roughly doubles. Now suppose the session blob holds a request counter
and two of the user's tabs fire at once, each doing "read counter, add one, write
back." Both target the *same* key on `A`; `A`'s per-key [[atomic-operation]]
guarantee serializes them, so the counter ends at `+2`, not a lost `+1`. That is
the whole concept in motion: one key → one partition (scale), one key → atomic
(correctness), value opaque and fetched only by key (the model), all of it durable
across a restart (the database).

**Where this shows up.** Redis is a key–value store kept in memory for speed;
DynamoDB is a managed one built for massive horizontal scale; etcd is a small,
strongly-consistent one used to hold a cluster's configuration. They differ in
durability, scale, and consistency guarantees, but each is an instance of the model
described here — opaque values fetched by unique key, durable and concurrent, scaled
by partitioning the keyspace. These are incidental product names; the durable idea
is the key-value mapping turned into a partitioned, atomic, persistent database.

## Prerequisites

- [[key-value]]
- [[atomic-operation]]

## Sources

_none_
