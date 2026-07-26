---
id: predecessor-query
title: Predecessor Query
summary: "A predecessor query asks one question of a collection of stored numbers (called keys): given a query value T, return the largest stored key that is strictly less than T — the key…"
type: concept
tags: [algorithms]
prereqs: [binary-search, binary-search-tree]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Predecessor Query

## Summary

A *predecessor query* asks one question of a collection of stored numbers (called *keys*): given a query value `T`, return the largest stored key that is *strictly less than* `T` — the key that comes just before `T`, with `T` itself excluded. The motivating example is a log store keyed by timestamp, answering "give me the most recent record dated strictly before time `T`." The single useful lesson is that the *same* query wants *different* machinery depending on **how the keys arrive**. If they arrive already in increasing order (or never change), keep them in a sorted array and answer each query with [[binary-search]] in about `log2(n)` comparisons, while each new key is just appended for almost no cost. If they can arrive out of order, a sorted array becomes slow to update, so the keys live in a [[binary-search-tree]] instead, which answers the predecessor query *and* absorbs each out-of-order arrival, both in about `log2(n)` work. One query, two regimes — you match the structure to the arrival pattern.

## Grounded explanation

**The question, stated exactly.** Suppose a collection holds some numbers, the *keys* — for the running example, the timestamps at which log records were written. A *predecessor query* takes a query value `T` and returns the largest stored key that is *strictly less than* `T`: the closest key below `T`, with `T` itself never counting even if it happens to be present. "Strictly less" is the load-bearing word. If `T = 25` and the keys include `20` and `30`, the answer is `20`; if `T = 20` and `20` is stored, the answer is *not* `20` (that is not strictly less) but the largest key below `20`. When no stored key lies below `T` at all, the honest answer is "no predecessor." In the log store this reads as: *the most recent record dated strictly before time `T`* — and the boundary convention (strictly-before vs at-or-before) is part of giving a correct answer, not a detail to leave vague.

**The defining insight: the query is fixed, the right structure is not.** The contribution of this concept is not a clever trick for finding the predecessor — finding it is easy once the keys are organized. The contribution is recognizing that the *cost* of answering it well is decided by a question you must ask up front: **do the keys arrive already in order, or can they arrive out of order?** Two arrival patterns ("cases") split here, and each picks a different structure. This is the whole "why": the query never changes, but the access pattern does, and a structure that is perfect for one pattern is wasteful for the other.

**Case A — keys arrive in increasing order (or are static).** This is the natural pattern for a log driven by a forward-moving clock: each new timestamp is greater than or equal to the previous one, so the keys are *already sorted* the moment they land. Here the right structure is a *sorted array* — a list of keys laid out left to right in nondecreasing order, addressed by *index* counting from `0`.

- *Inserting* a new key is a plain *append* to the end. Because the new key is at least as large as everything before it, appending keeps the array sorted with no rearranging. That is constant work per insert — call it `O(1)`, meaning the cost does not grow with how many keys are already stored.
- *Answering* the predecessor query is exactly [[binary-search]]. Recall that `bisect_left` returns the first index whose key is *greater than or equal to* `T` — equivalently, the position just after the last key that is *strictly less than* `T`. That description is precisely the boundary we want: the strict predecessor sits at the index *one to the left* of `bisect_left`'s answer. So: run `bisect_left` for `T` to get an index `i`; if `i = 0` no key is below `T` and there is no predecessor; otherwise the predecessor is the key at index `i − 1`. Binary search costs about `log2(n)` comparisons, written `O(log n)` — the count of times you can halve `n` keys down to one.

Why a sorted array and not something fancier? Because when keys are already ordered, the append sidesteps the one thing arrays are bad at (see the next paragraph), and binary search already delivers the query in logarithmic time. Nothing more is needed.

**Case B — keys can arrive out of order.** Now suppose timestamps do *not* arrive sorted — a record dated `10` shows up after one dated `30`. A sorted array breaks here. To keep it sorted you cannot just append the `10`; you must binary-search for where `10` belongs (cheap, `O(log n)`) and then *physically open a gap* by shifting every later key one slot to the right to make room. That shifting touches up to `n` keys, so each out-of-order insert costs `O(n)` — work that grows with the size of the store. Do that on every arrival and the store crawls. This is the exact caveat [[binary-search]] warns about: binary search makes *lookup* fast, but it does nothing to make *insertion into an array* fast.

The fix is to store the keys in a [[binary-search-tree]] (kept balanced). Take it as a known structure: an ordered tree that gives `O(log n)` for *both* insertion and the predecessor query on data that changes over time, precisely because it never has to shift a block of elements — it rewires a few links instead. To answer the predecessor query inside the tree you walk down from the root, at each node comparing the node's key against `T`: every key strictly less than `T` is a candidate, so you remember the largest such candidate seen so far and keep descending toward larger keys while they stay below `T`; when the walk ends, that remembered candidate is the predecessor (or "none" if you never saw a key below `T`). One root-to-leaf walk, `O(log n)`.

**The contrast, stated as costs.** Same query — "largest key strictly below `T`" — answered in `O(log n)` either way. What differs is the *insert* cost under each arrival pattern, and that is what decides the structure:

- Case A (in-order arrivals): sorted array — insert `O(1)` by appending, query `O(log n)` by [[binary-search]].
- Case B (out-of-order arrivals): a sorted array would cost `O(n)` per insert (shifting), so use a [[binary-search-tree]] — insert `O(log n)`, query `O(log n)`.

Pick the array's cheap append when you can guarantee order; pay for the tree's flexibility only when arrivals force you to. Choosing wrongly — a sorted array under out-of-order arrivals — turns a logarithmic store into a linear one. This same predecessor primitive is what *range queries* ("all records between two times") are built from — two predecessor searches plus the slice between them — and it is the lookup that real time-series databases generalize, splitting data into time-sorted blocks and binary-searching within the located block; the surrounding storage machinery addresses scale, not this `O(log n)` core.

**Worked instance.** Take keys with values `10, 20, 30, 40`.

*Case A.* They arrive in increasing order, so the sorted array is `[10, 20, 30, 40]` at indices `0, 1, 2, 3`. Query `T = 25`. Run `bisect_left` for `25`: the first key `≥ 25` is `30` at index `2`, so `i = 2`. Since `i > 0`, the predecessor is the key at index `i − 1 = 1`, which is `20`. Check it directly: `20` is below `25`, and the only other key below `25` is `10`, which is smaller — so `20` is indeed the *largest* key strictly below `25`. Correct. Now query `T = 10`. `bisect_left` for `10` returns the first key `≥ 10`, which is `10` itself at index `0`, so `i = 0`. Because `i = 0`, there is *no* predecessor — nothing in the array is strictly less than `10`. This is the non-degenerate boundary the "strictly less than" wording forces: even though `10` is present, it does not count as its own predecessor, and below it there is nothing.

*Case B.* Now the same four timestamps arrive *out of order*: `30`, then `10`, then `40`, then `20`. A sorted array would have to shift elements to slot the `10` ahead of the `30` and the `20` between `10` and `30` — `O(n)` per insert. Instead insert each into a [[binary-search-tree]], `O(log n)` each, with no shifting: the `30` becomes the root; `10` is smaller so it hangs to its left; `40` is larger so it hangs to its right; `20` is smaller than `30` (go left) but larger than `10` (settle to `10`'s right). The tree now holds exactly the keys `{10, 20, 30, 40}` in order, never having moved a block of elements. Predecessor query for `T = 25`: walk from the root `30`. `30` is not below `25`, so it is no candidate; `25 < 30`, go left. Reach `10`: it *is* below `25`, remember it as the best-so-far; `25 > 10`, go right. Reach `20`: it is below `25` and larger than the remembered `10`, so update best-so-far to `20`; go right, but there is no further node. The walk ends with `20` — the same answer Case A produced, reached by a single `O(log n)` descent rather than a shift-heavy array update.

## Prerequisites

- [[binary-search]]
- [[binary-search-tree]]

## Sources

- `etc/study-notes.html` — "An ordered log store and the predecessor query": the predecessor query as "largest key strictly less than `T`", Case A (in-order arrivals → sorted array, append `O(1)`, `bisect_left` query `O(log n)`, with the `O(n)` insert-shift misstep) and Case B (out-of-order arrivals → balanced search tree, `O(log n)` insert and query), plus the range-query and time-series generalizations.
