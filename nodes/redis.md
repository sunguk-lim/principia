---
id: redis
title: Redis (in-memory data-structure store)
summary: A key-value store whose keyspace is one big hash-map kept entirely in RAM, and whose values are not opaque blobs but typed data structures (string, list, set, hash, sorted set) the server mutates in place — one command at a time on a single thread, so every command is atomic by construction.
type: concept
tags: [databases/key-value-store]
prereqs: [key-value-store, hash-map, memory-hierarchy, linked-list, hash-set, atomic-operation]
sources: [https://redis.io/docs/latest/develop/data-types/]
status: explained
created: 2026-06-26
updated: 2026-06-29
---

# Redis (in-memory data-structure store)

## Summary

Redis (REmote DIctionary Server) is a **[[key-value-store]]**: at its core sits one giant
[[hash-map]] — the *keyspace* — mapping a string key to a value, with the usual O(1)-average
get / set / delete. Two design choices make it more than a dictionary. First, the whole keyspace
lives **in memory** ([[memory-hierarchy]]): the dataset sits in RAM, not on disk, so every
operation is nanosecond-latency memory work instead of a millisecond disk seek. Second — its
defining contribution — a value is **not an opaque blob** but a *typed data structure* the server
understands and mutates **in place**: a string, a list (a [[linked-list]]), a set (a [[hash-set]]),
a hash (a nested [[hash-map]]), or a sorted set. You send a small command naming the structure and
the edit; the server applies it server-side and returns the result. Because a single thread runs
one command to completion before the next, every command is an [[atomic-operation]] for free.

## Grounded explanation

### What it is — a keyspace that is a hash-map of typed structures

The top level of Redis *is* a [[hash-map]]: keys (always strings, e.g. `"session:42"`) → values.
This gives the "key-value store" its name and its average-O(1) lookup. The twist is the **value
side**. In a plain cache the value is a byte blob you can only `GET` and `SET` whole. In Redis the
value carries a **type**, and the server exposes operations *on that type*:

| Redis value type | underlying structure | example command | what the server does |
|---|---|---|---|
| string / integer | a byte string | `INCR`, `SET`, `GET` | overwrite, or parse-add-one in place |
| list | a [[linked-list]] (doubly linked) | `LPUSH`, `RPOP` | push/pop at either end in O(1) |
| set | a [[hash-set]] | `SADD`, `SISMEMBER` | insert / membership test, no duplicates |
| hash | a nested [[hash-map]] | `HSET`, `HGET` | field→value map *inside* one key |
| sorted set | a score-ordered structure | `ZADD`, `ZRANGE` | keep members ranked by a numeric score |

So the data model is recursive: the keyspace is a [[hash-map]], and a *single value* in it can
itself be a [[hash-map]] (a Redis hash), a [[linked-list]] (a Redis list), or a [[hash-set]]
(a Redis set). (The sorted set is built on a skip-list + a [[hash-map]] of scores; the skip-list
is incidental detail here, so it stays prose, not a prerequisite.)

### Why it works — the three choices, and the "why" behind each

**Why in-memory.** The entire speed story is the [[memory-hierarchy]] gap: a RAM access is ~100 ns,
a disk seek ~10 ms — five orders of magnitude. By keeping the working set in RAM, Redis turns every
read and write into a memory operation, so latency is dominated by the network round-trip (Redis
speaks a simple request/response protocol over TCP), not by storage. Durability is then bolted back
on as an option — periodically *snapshotting* RAM to a disk file, or *appending* each write command
to a log that can be replayed on restart — so an in-memory store can still survive a reboot. (The
specific file formats are operational reference, not concepts, so they stay prose.)

**Why a data-structure server, not a blob cache.** Suppose you keep a job queue. With a blob value
you must `GET` the whole list, append in the client, and `SET` it back — three steps, the full value
crossing the wire twice, and a window where two clients clobber each other. Redis collapses this to
one `LPUSH`: the [[linked-list]] lives server-side, so the client ships only the *operation* and the
new element, and the server splices it in O(1). The structure's locality (server-side) plus a
single small command is the whole win.

**Why single-threaded is not a bug.** Redis executes commands on **one** thread, one at a time to
completion. Counter-intuitively this is a feature: there are no locks, no lock contention, and no
context-switch overhead, and — crucially — each command becomes an [[atomic-operation]] *by
construction*. `[[atomic-operation]]` defines atomicity as an indivisible read-modify-write that no
other operation can interleave with; Redis achieves exactly that property, but through *serialization
on a single thread* rather than a hardware compare-and-swap. Because each command is already
memory-fast, one thread can saturate the service, and you get atomicity without ever reasoning about
a lock.

### Worked instance — one keyspace, one session of commands

Start with an empty keyspace (an empty top-level [[hash-map]]) and run, in order:

```
SET   session:42  "alice"      → keyspace now maps "session:42" → (string) "alice"
HSET  user:7  name alice age 30 → key "user:7" → a nested hash-map { name:"alice", age:"30" }
HGET  user:7  age              → "30"           (field lookup inside the value)
LPUSH jobs  "a"               → "jobs" → list [a]
LPUSH jobs  "b"               → list [b, a]     (LPUSH prepends at the head)
RPOP  jobs                    → "a", list now [b]   (pop the tail; O(1), it is a doubly [[linked-list]])
SADD  tags  redis db          → "tags" → set {redis, db}, returns 2 (two new members)
SADD  tags  db                → returns 0       ([[hash-set]] semantics: "db" already present, no dup)
SISMEMBER tags redis          → 1
```

Now the atomicity payoff, made concrete. Two clients **C1** and **C2** both want to count a page
view on the same key, starting at `page:views = 0`:

- **The race you would have** with a client-side read-modify-write: C1 `GET`→0, C2 `GET`→0, C1
  `SET 1`, C2 `SET 1`. Two views, final value **1** — a lost update.
- **With Redis `INCR`**: each client sends one `INCR page:views`. The single thread serializes them
  — runs C1's increment 0→1 *to completion*, then C2's 1→2. Final value **2**, correct, with no lock
  written anywhere. `INCR` is the read-modify-write of [[atomic-operation]], made indivisible by the
  single-thread discipline.

This ties the three levels of one example together: the **structure** (the keyspace is a
[[hash-map]]; `page:views`'s value is a string-integer), the **algorithm** (the command mutates the
structure server-side, serialized to one at a time), and the **substrate** (it all happens in RAM,
top of the [[memory-hierarchy]], so each `INCR` is a handful of nanoseconds and the thread never
blocks on disk).

## Prerequisites

- [[hash-map]] — the keyspace itself, and one of the value types (the Redis hash)
- [[memory-hierarchy]] — "in-memory" means the dataset sits in RAM; the RAM-vs-disk gap is the speed
- [[linked-list]] — the Redis list value type (doubly linked → O(1) push/pop at both ends)
- [[hash-set]] — the Redis set value type (membership, no duplicates)
- [[atomic-operation]] — each command is an indivisible read-modify-write, here via single-thread serialization

## Sources

- Redis data types — https://redis.io/docs/latest/develop/data-types/
