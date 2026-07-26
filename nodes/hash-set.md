---
id: hash-set
title: Hash Set
summary: "A hash set is a hash-map stripped down to its keys: it stores a collection of items with no value attached to each one, so it answers exactly one question, and answers it fast —…"
type: concept
tags: [algorithms]
prereqs: [hash-map]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Hash Set

## Summary

A hash set is a [[hash-map]] stripped down to its keys: it stores a collection
of items with *no* value attached to each one, so it answers exactly one
question, and answers it fast — *is this item present?* Adding an item, removing
it, and testing whether it is in the set each cost constant average time,
written `O(1)`, the same as the hash map it is built from — the time does not
grow as the set fills up. Because it keeps only one copy of each item and can
check membership instantly, it has two everyday uses: *deduplication* (throw a
pile of items in and duplicates collapse to a single copy each) and *membership
testing* (replace a slow item-by-item scan of a list with one instant lookup).
In Python this structure is the built-in `set`.

## Grounded explanation

**The object: a hash map with the values thrown away.** Recall that a
[[hash-map]] stores *key → value* pairs and, given a key, can fetch, store, or
remove that key's value in constant average time `O(1)` — meaning the work stays
roughly the same whether the structure holds ten items or ten million, rather
than growing in proportion to the count `n` (which would be `O(n)`, "order n").
A hash set keeps that whole machinery but discards the values. It stores only
the *keys themselves* — now simply called the set's *elements* — and attaches
nothing to them. So where a hash map can tell you "the value paired with this
key," a hash set can only tell you "yes, this element is in the set" or "no, it
is not." The map's three operations rename accordingly: *set/get/delete a pair*
becomes *add an element*, *test whether an element is present* (the membership
test, written in Python as `x in s`), and *remove an element*. Each one is just
the corresponding hash-map operation with the value half ignored, so each
inherits the map's `O(1)` average cost.

**Why this gives `O(1)` membership — the inherited insight.** The entire reason
a hash set is fast is the trick it borrows wholesale from [[hash-map]]: it does
not *search* for an element, it *computes* where the element would live. To test
whether `x` is present, the set runs `x` through the same kind of hash function
and reduces the result to a bucket index, lands on exactly one bucket, and looks
only inside that one bucket's short list — never scanning the others. Storing
and finding both collapse to the same short calculation, independent of how many
elements the set holds. This is why membership is `O(1)` on average and not
`O(n)`: the set jumps straight to the one place `x` could be. Everything that
makes a [[hash-map]] fast — buckets, hashing, collision handling, resizing to
keep the buckets' lists short — is present unchanged; the hash set simply uses
it to answer a yes/no question instead of a fetch-the-value question.

**The defining contribution: one copy of each element.** The single behaviour
that distinguishes a set from a plain list is that an element is either *in* or
*not in* — there is no notion of "in twice." Adding an element already present
is, under the hood, exactly the hash map's *set* on a key that already exists:
it lands on the same bucket, finds the element already there, and changes
nothing. So a set silently absorbs repeats. This is not an extra feature bolted
on; it falls directly out of being a keys-only [[hash-map]], where each key
exists at most once. That property is what makes the two canonical uses below
work.

**Canonical use 1 — deduplication.** To remove duplicates from a pile of items,
add every item to a fresh hash set. Each *add* either inserts a brand-new
element or hits one already present and does nothing; when the dust settles, the
set holds exactly the distinct items, each once. *Worked instance:* deduplicate
the list `[3, 1, 3, 2, 1]` into a fresh empty set `s`.

- *add* `3` → bucket computed from `3` is empty, so `3` goes in. `s = {3}`.
- *add* `1` → its bucket is empty, `1` goes in. `s = {1, 3}`.
- *add* `3` again → the set computes `3`'s bucket, finds `3` already sitting
  there, and does nothing. `s = {1, 3}` — unchanged. **The duplicate
  collapses.**
- *add* `2` → new, goes in. `s = {1, 2, 3}`.
- *add* `1` again → finds `1` already present, does nothing. `s = {1, 2, 3}`.

Five adds, each `O(1)`, total `O(n)` for `n` items, and the result is the three
distinct values. Note the result `{1, 2, 3}` carries *no order*: like the
[[hash-map]] it is built from, an element's position is decided by its hash, not
by when it was added, so a set has no meaningful element order. The `{1, 2, 3}`
ordering above is just for reading; the structure makes no such promise.

**Canonical use 2 — membership testing, and the `O(n)` → `O(n)` win.** The
sharper use is replacing a repeated *scan* with a repeated *lookup*. Asking "is
`x` in this list?" by walking the list costs `O(n)` per question, because in the
worst case you compare against every element. Do that inside a loop — for each
of `n` items, ask whether you have seen it before by scanning what came earlier
— and the total is `O(n²)`: `n` questions, each up to `O(n)` work. Swap the
growing scanned-so-far list for a hash set, and each question becomes one `O(1)`
membership test, dropping the total to `O(n)`.

The standard pattern is a *"seen" set*: an initially empty set that accumulates
the elements already encountered, so each new element can be checked against
everything seen so far in one `O(1)` test. *Worked instance — detect whether a
list has any duplicate*, on `[3, 1, 3, 2, 1]`, with `seen` starting empty.

- element `3`: test `3 in seen` → no (`seen` empty). Not a duplicate; *add* `3`.
  `seen = {3}`.
- element `1`: test `1 in seen` → no. *add* `1`. `seen = {1, 3}`.
- element `3`: test `3 in seen` → **yes** — `3` is already there. A duplicate is
  found; stop and report "has a duplicate."

The membership test `3 in seen` did not scan the two prior elements; it hashed
`3`, jumped to its bucket, and found `3` there — `O(1)`. Across the whole list
that is one `O(1)` test per element, so detecting a duplicate costs `O(n)`
total, versus the `O(n²)` of re-scanning the prefix each time. This is the
concrete shape of the habit "swap an `O(n)` lookup for an `O(1)` hash": the same
"seen" set drives duplicate detection, and, in problems that walk a chain of
elements, cycle detection — *have I been at this element before?*

**What elements are allowed — hashable, inherited.** Because a hash set *is* a
keys-only [[hash-map]], its elements carry the map's restriction on keys
exactly: an element must be *hashable*, meaning the hash function always produces
the same number for it, which in turn requires the element to be *immutable* (its
value fixed for life, so its computed bucket never moves). Numbers, words, and
fixed tuples qualify and can be set elements; a list, whose contents can change,
cannot. The set inherits this rule wholesale — it is the same constraint
[[hash-map]] places on keys, seen from the element side.

## Prerequisites

- [[hash-map]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the Hash set row
  (`set`, `add / in / del O(1) avg`, "membership, dedup"), the "Problem signal →
  structure" panel ("Have I seen this / how many?" → hash map / set), and the
  closing habit ("swap an `O(n)` lookup for an `O(1)` hash").
