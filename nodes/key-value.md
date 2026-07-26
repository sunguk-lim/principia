---
id: key-value
title: Key–Value Mapping
summary: An abstract mapping from distinct keys to values — a set of (key, value) pairs with unique keys — offering get/set/delete addressed by the key's content (associative access) rather than by position; the interface hash-maps, tries, and tree-maps each implement.
type: concept
tags: [algorithms]
prereqs: [set]
sources: []
status: explained
created: 2026-06-29
updated: 2026-06-29
---

# Key–Value Mapping

## Summary

A **key–value mapping** stores data as pairs — a *key* and the *value* attached
to it — so that you retrieve, replace, or remove a value by naming its key
rather than by knowing where it sits. A phone book is the everyday example: you
look a person (the key) up to get their number (the value), and you neither know
nor care which physical page it landed on. The defining rule is that **keys are
unique**: each key names at most one value, so "the value for key `k`" is always
a single, unambiguous answer. This is an *abstract interface* — the three
operations *get*, *set*, and *delete*, all addressed by key — not a particular
way of storing the data; a `hash-map`, a balanced tree, and a `trie` are
different concrete machines that all present this same key–value interface.

## Grounded explanation

**The object: a set of pairs with distinct keys.** A key–value mapping is a
[[set]] of *ordered pairs* `(k, v)` — the key `k` bound to its value `v` —
subject to one constraint that makes it a *mapping* rather than just any set of
pairs: **no two pairs share a key**. Because the keys are distinct, they form a
[[set]] in their own right (the *keyspace*), and naming a key selects exactly one
pair. That single constraint is the whole idea: it guarantees the phrase "the
value for `k`" denotes one value, never two. (Drop the constraint and you have a
*multimap*, where a key may carry several values — a different structure.) The
keys must support [[set]] membership and equality, since every operation begins
by asking "is `k` already a key, and if so which pair is it?"; the values carry
no such requirement and may repeat freely (two different people may share a phone
number).

**What it contributes: associative access.** Compare two ways of reaching data.
An array gives you *positional* access: you must know an item is at index `7` to
fetch it — the address is a position you are responsible for tracking. A
key–value mapping gives you *associative* (content-addressed) access instead: the
address **is** the key itself, a piece of meaningful data you already hold — a
username, a word, an account id. You ask for the value *of* `"alice"`; you never
ask "which slot is Alice in?" This is the contribution and the reason the
structure is everywhere: real lookups are almost always "given this identifier,
what is attached to it?", and a mapping answers exactly that question directly.

**The interface — three operations, each keyed.** The mapping exposes:

- **set(k, v)** — bind value `v` to key `k`. If `k` is not yet in the keyspace,
  add the pair `(k, v)`; if it *is* (membership says yes), **overwrite** its value
  with `v`. The uniqueness invariant is maintained *by* this overwrite — setting
  an existing key replaces rather than duplicates, so the keyspace stays a [[set]].
- **get(k)** — return the value bound to `k`, or report "absent" if `k` is not in
  the keyspace. This is the read that associative access exists for.
- **delete(k)** — remove the pair whose key is `k`, shrinking the keyspace by one.

Every operation names a key and consults [[set]] membership on the keyspace
first; none refers to a position. That is what makes the interface *abstract* —
it says nothing about *how* membership is decided or where the pair lives, only
*what* the three operations mean.

**Why "abstract" matters — one interface, many machines.** Nothing above says how
to find the pair for a key. Different implementations answer that differently and
trade off accordingly: a `hash-map` computes the storage location from the key
and gives `O(1)` average access but no key order; a balanced search tree keeps
keys sorted and gives `O(log n)` access *with* ordered traversal; a `trie`
stores keys character by character and shares common prefixes. They are distinct
nodes precisely because the *mechanism* differs — but each one, viewed from
outside, is just *get / set / delete by key*. Naming the interface separately
from any one machine is what lets you say "use a key–value store here" before
deciding which structure pays for it.

**Worked instance.** Model a phone book as a key–value mapping `B`, starting from
the set of pairs

```
B = { ("alice", "555-1234"), ("bob", "555-7777") }
```

The keyspace is the [[set]] `{"alice", "bob"}`.

1. **get("bob")** → membership says `"bob"` is a key; its pair is
   `("bob", "555-7777")`, so the result is `"555-7777"`. We named the person, not
   a position.
2. **set("alice", "555-9999")** → `"alice"` is already a key, so this
   **overwrites**: the pair `("alice", "555-1234")` becomes
   `("alice", "555-9999")`. The keyspace is unchanged — still
   `{"alice", "bob"}` — because no *new* key was introduced. Uniqueness held: we
   did not end up with two `"alice"` pairs.
3. **set("carol", "555-0000")** → `"carol"` is *not* in the keyspace, so this
   **adds** the pair. Now
   `B = { ("alice","555-9999"), ("bob","555-7777"), ("carol","555-0000") }` and
   the keyspace grows to `{"alice", "bob", "carol"}`.
4. **delete("bob")** → remove the pair keyed `"bob"`; the keyspace shrinks to
   `{"alice", "carol"}` and `get("bob")` now reports "absent".

At no step did we mention an index, a slot, or an order — every action was driven
purely by a key and a [[set]]-membership test on the keyspace. That is the
key–value mapping in full: a set of uniquely-keyed pairs, accessed by the content
of the key.

**Where this shows up.** It is the model behind a dictionary / associative array
in every language (Python's `dict`, Java's `Map`, JS objects), behind key–value
databases and caches such as `redis`, and behind countless one-off lookups
("user id → session", "word → count"). Those are incidental instances; the
durable idea is the uniquely-keyed, content-addressed mapping above.

## Prerequisites

- [[set]]

## Sources

_none_
