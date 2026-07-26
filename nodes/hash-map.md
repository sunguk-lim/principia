---
id: hash-map
title: Hash Map
summary: A hash map stores pairs of a key and its associated value — for example the key "cat" paired with the value 9 — so that, given a key, you can fetch, overwrite, or remove its value…
type: concept
tags: [algorithms]
prereqs: [key-value, arithmetic]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-29
---

# Hash Map

## Summary

A hash map stores pairs of a *key* and its associated *value* — for example the
key `"cat"` paired with the value `9` — so that, given a key, you can fetch,
overwrite, or remove its value almost instantly, no matter how many pairs are
stored. It achieves this by turning each key into a number and using that number
to compute an array position where the pair lives, so a lookup jumps straight to
the right spot instead of checking every stored pair one by one. Getting,
setting, and deleting a pair therefore each take *constant average time* — the
work does not grow as the map fills up — which is why it is the default tool for
"have I seen this before?" and "how many of each?" questions. In Python this
structure is the built-in `dict`.

## Grounded explanation

**The object and the problem it solves.** A hash map is one implementation of the
[[key-value]] mapping — a collection of *key → value* pairs. A key is whatever you look things up by (a word, an
identifier, a number); the value is the data attached to that key. The two core
operations are *set* (store or overwrite the value for a key) and *get* (retrieve
the value for a key); *delete* (remove a key's pair) is the third. The naive way
to support these is a plain list of pairs: to *get* the value for a key you walk
the list comparing keys until you find a match. If the list holds `n` pairs, that
scan touches up to `n` of them — its cost grows in proportion to `n`. We write
this growth as `O(n)`, read "order n": the time is roughly proportional to the
number of stored pairs. The hash map's entire purpose is to replace that growing
scan with work that stays *constant* — roughly the same whether the map holds ten
pairs or ten million — written `O(1)`, "order 1," meaning the cost does not grow
with `n`.

**The central trick: compute the location instead of searching for it.** The map
keeps a backing array — a fixed-length row of numbered slots, called *buckets* —
of some size `m` (say `m = 8`, so the slots are numbered `0` through `7`). To
store a pair, the map first runs the key through a *hash function*: a fixed
procedure that reads the key and produces a large whole number, the key's *hash
code*. The only properties that matter are that the same key always yields the
same number, and that different keys tend to yield numbers that scatter widely and
unpredictably. That hash code is usually far too big to be a slot number, so the
map reduces it to a valid index using one arithmetic step — the *remainder* (using
the division operation `÷` of [[arithmetic]]): divide the hash code by `m` and
keep what is left over. This remainder, called *hash code modulo m*, is always a
whole number from `0` to `m − 1` — exactly the range of legal slot numbers. That
remainder is the key's *bucket index*. The pair is then placed in that bucket.

The payoff appears at lookup. To *get* a key's value, the map repeats the very
same two steps — hash the key, take the remainder modulo `m` — and lands on the
same bucket the pair was stored in. It looks only inside that one bucket, not
across the whole map. Because hashing a key and taking one remainder cost the same
amount of work regardless of how many pairs the map holds, the lookup is `O(1)` on
average. This is the key insight: the map does not *search* for where a key lives;
it *computes* the location directly from the key itself, so storing and finding
both reduce to the same short calculation.

**Why the hash function output must then be reduced — the invariant.** The bucket
index must always be a legal slot number, `0` to `m − 1`; a hash code of, say,
several billion is not. Taking the remainder modulo `m` enforces exactly that
invariant: dividing any whole number by `m` leaves a remainder strictly smaller
than `m` and never negative, so the result is guaranteed to be a usable slot. This
is the one "magic-looking" step, and it is pure [[arithmetic]] — division keeping
the leftover.

**Collisions, and why they are unavoidable.** Because many possible keys get
crushed into only `m` buckets, two different keys can land on the same bucket
index — their hash codes leave the same remainder modulo `m`. This is a
*collision*. It is not a bug; with more possible keys than buckets it is bound to
happen sometimes. A bucket therefore cannot hold just one pair; it must cope with
several. The common resolution is *chaining*: each bucket holds a short list of
the pairs that landed there. On *set*, the map appends the pair to that bucket's
list (replacing any pair already present with the same key). On *get*, the map
goes to the computed bucket and then walks only that bucket's short list,
comparing keys, to find the match. (An alternative scheme, *open addressing*,
stores at most one pair per bucket and, on a collision, *probes* — steps to the
next bucket, and the next, until it finds an empty one or the sought key; lookup
follows the same probe sequence. Either way the principle is the same: compute a
starting bucket, then resolve the few pairs that share it.)

**Keeping the chains short — load factor and resizing.** The whole `O(1)` promise
depends on each bucket's list staying short. Define the *load factor* as the
number of stored pairs divided by the number of buckets, `n ÷ m` — the average
number of pairs per bucket (a division from [[arithmetic]]). If you keep adding
pairs without adding buckets, `n` grows while `m` stays fixed, the load factor
climbs, the average chain gets longer, and each lookup must walk a longer list —
drifting back toward `O(n)`. To prevent this, the map watches the load factor and,
when it crosses a chosen threshold (commonly around `0.75`), performs a *resize*:
it allocates a larger backing array — typically about double the buckets — and
*rehashes*, recomputing every existing key's bucket index against the new, larger
`m` and reinserting each pair. With more buckets, the same pairs spread thinner,
chains shrink back toward length one, and operations return to `O(1)` average. A
single resize is expensive (it touches all `n` pairs), but because the array
doubles, resizes happen rarely enough that the *average* cost per operation,
spread over many operations, stays constant. This averaging-out is what "`O(1)`
average" means, and it is also why the *worst case* is still `O(n)`: if an
adversary or an unlucky run of keys all collide into one bucket, that bucket's
chain holds them all and a lookup must walk the lot.

**What keys are allowed — hashable keys.** For all of this to work, a key must be
*hashable*: the hash function must always produce the *same* number for that key.
If a key's contents could change after it was stored, its hash code — and thus its
bucket index — would change, and the map would later look in the wrong bucket and
fail to find the pair. So keys must be *immutable* (their value fixed for life):
words, numbers, and fixed tuples qualify; a list, whose contents can change, does
not. Values carry no such restriction.

**Worked instance.** Take a map with `m = 8` buckets, slots `0`–`7`, initially all
empty. Store three pairs.

- *Set* `"cat" → 9`. Hashing `"cat"` yields some large number; suppose it is
  `4795`. Reduce it: `4795 ÷ 8` leaves remainder `3` (since `8 × 599 = 4792`, with
  `3` left over), so `4795 modulo 8 = 3` — the bucket index is `3`. Place
  `("cat", 9)` in bucket `3`'s list.
- *Set* `"dog" → 4`. Suppose hashing `"dog"` gives `2710`; `8 × 338 = 2704`,
  remainder `6`, so bucket `6`. Bucket `6` is empty, so its list becomes
  `[("dog", 4)]`. No collision.
- *Set* `"x" → 1`. Suppose hashing `"x"` gives `99`; `8 × 12 = 96`, remainder `3`,
  so bucket `3` — the same bucket already holding `"cat"`. **Collision.** With
  chaining, the map appends to bucket `3`'s list, which becomes
  `[("cat", 9), ("x", 1)]`.

Now *get* `"cat"`. The map hashes `"cat"` again — the same `4795` — takes
`4795 modulo 8 = 3`, goes to bucket `3`, and walks its short list: it compares
`"cat"` against the first entry's key `"cat"`, matches, and returns `9`. It never
touched buckets `0`,`1`,`2`,`4`,`5`,`6`,`7`, nor the pair `("dog", 4)` — only the
one bucket the computation pointed at, and only the one or two pairs sharing it.
That is the entire mechanism: hash once, reduce by modulo to a bucket, resolve the
few collisions there. Had many more keys also hashed to bucket `3`, that one list
would grow long and this lookup would slow toward `O(n)` — the worst case the load
factor and resizing exist to hold off.

**One more property: no order.** Because a pair's position is decided by its hash
code, not by when it was inserted or by any sorting of the keys, a hash map gives
no meaningful order to its keys. If you need keys kept in sorted order, a hash map
is the wrong tool; it trades order away for its `O(1)` speed.

**Where this shows up.** In Python the hash map is the built-in `dict`. A close
relative, the `set`, is a hash map that stores keys with no attached values — used
purely to answer "is this item present?" and to remove duplicates, also `O(1)`
average. Two standard conveniences are built on `dict`: a `Counter`, which is a
`dict` specialized to tally how many times each key appears (a frequency map), and
a `defaultdict`, which is a `dict` that supplies a fresh default value the first
time a missing key is accessed (handy for grouping items under keys without
checking first). These are incidental tool names; the underlying structure in
every case is the hash map described above.

## Prerequisites

- [[arithmetic]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the hash map / hash
  set rows (`dict`, `set`, `get / set / del O(1) avg`), the "Essential Python
  idioms" block (`Counter`, `defaultdict`), and the "Problem signal → structure"
  panel ("Have I seen this / how many?" → hash map / set; "swap an O(n) lookup for
  an O(1) hash").
