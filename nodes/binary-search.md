---
id: binary-search
title: Binary Search
summary: Binary search finds a target value in a sorted sequence — one whose elements are arranged from smallest to largest — by repeatedly halving the range it still needs to examine.
type: concept
tags: [algorithms]
prereqs: [arithmetic]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Binary Search

## Summary

Binary search finds a target value in a *sorted* sequence — one whose elements are arranged from smallest to largest — by repeatedly halving the range it still needs to examine. It looks at the middle element of the current range: if that element equals the target, it is done; if the target is smaller, the whole upper half can be discarded; if larger, the whole lower half can be discarded. Each comparison throws away half of the remaining candidates, so a sequence of `n` elements is settled in about `log2(n)` comparisons instead of the `n` comparisons a one-by-one scan would need. That difference is the whole point: roughly 32 comparisons for four billion items, versus four billion.

## Grounded explanation

**The setting and the term.** A *sequence* here is a list of values laid out in numbered positions, called *indices*, counted from `0`. The sequence is *sorted* (also called *ordered*) when reading it left to right gives values that never decrease — each is greater than or equal to the one before. *Binary search* is a procedure that, given such a sorted sequence and a *target* value to look for, reports either where the target sits or that it is absent. The word *binary* means "two": every step splits the unsearched region into two halves and keeps only one of them.

**The central object: a shrinking range.** At all times the procedure tracks a *range* — a contiguous stretch of the sequence, named by its low index and high index, that still might contain the target. Everything outside the range has already been ruled out. The range starts as the entire sequence. The procedure's one job is to shrink that range until either the target is found inside it or the range becomes empty (low index passes high index), which means the target is not present.

**The one step, and why it is allowed to discard half.** Pick the *middle* index of the current range — roughly the average of the low and high indices, using the `+` and `÷` of [[arithmetic]] (and rounding down to land on a whole index). Compare the value at that middle index against the target. Three outcomes:

- The middle value *equals* the target — the search ends; the position is the middle index.
- The middle value is *greater than* the target. Because the sequence is sorted, every element from the middle position rightward is also greater than or equal to that middle value, hence also greater than the target. None of them can be the target, so the entire half from the middle rightward is discarded; the new range is everything strictly to the left of the middle.
- The middle value is *less than* the target. By the same sorted ordering, every element from the middle leftward is less than or equal to the middle value, hence also less than the target. That whole half is discarded; the new range is everything strictly to the right of the middle.

The *why* lives in that justification: sortedness is what lets a single comparison condemn an entire half. The thing being preserved at every step — the *invariant* — is "if the target is anywhere, it is inside the current range." The first comparison cannot move the target out of the range because the discarded half provably cannot hold it; so the invariant survives each step, and when the range finally narrows to one matching element (or to nothing), the answer is correct.

**Why this is fast (the WHY behind `log2 n`).** Start with `n` candidates. After one comparison at most about `n ÷ 2` remain; after two, about `n ÷ 4`; after `k` comparisons, about `n ÷ 2^k`. The search can stop once that count drops to `1`, i.e. once `2^k` reaches `n`. The number of halvings needed to take `n` down to `1` is written `log2(n)` — the base-2 logarithm, defined as exactly that count of repeated halvings (equivalently, the exponent `k` for which `2^k` equals `n`). For `n` near four billion (`2^32`), that is 32 comparisons. A *linear scan* — checking positions one at a time — would in the worst case touch all four billion. Halving collapses a multiplication-sized cost into an exponent-sized one; that is the entire advantage.

**Worked instance (target present).** Search for `7` in the sorted sequence `[1, 3, 5, 7, 9, 11]`, whose indices run `0` through `5`.

- Range is indices `0..5`. Middle index = `(0 + 5) ÷ 2`, rounded down, = `2`. The value there is `5`. Since `5 < 7`, discard the middle and everything left of it; the new range is indices `3..5`, i.e. `[7, 9, 11]`.
- Range is indices `3..5`. Middle index = `(3 + 5) ÷ 2` = `4`. The value there is `9`. Since `9 > 7`, discard the middle and everything right of it; the new range is index `3..3`, i.e. `[7]`.
- Range is index `3..3`. Middle index = `3`. The value there is `7`, which *equals* the target. Found, at index `3`.

Three comparisons. A linear scan checking `1, 3, 5, 7` in turn would have taken four, and up to six for the worst case (`11`). On just six elements the gap is small; multiply the sequence length and the gap becomes the four-billion-versus-32 chasm above.

**Worked instance (target absent) and the boundary nuance.** Now search for `6` in the same `[1, 3, 5, 7, 9, 11]`. The value `6` is not in the sequence, so the useful answer is not "found" but *where it would belong* — its *insertion point*, the index at which inserting `6` would keep the sequence sorted. There are two reasonable conventions, and **naming which one you mean is part of being correct**, because they can return different indices when the target is present and matters at the boundary when it is absent:

- *bisect_left* returns the *first* index whose element is greater than or equal to the target. Equivalently, it is the position just after the last element that is *strictly less* than the target. For `6` it returns index `3` (the first element `≥ 6` is `7`, at index `3`).
- *bisect_right* returns the *first* index whose element is *strictly greater* than the target — i.e. just after the last element that is *less than or equal to* the target. For `6` it also returns index `3` (the first element `> 6` is again `7`).

For an absent value the two agree. They diverge on a value that *is* present: searching for `7`, `bisect_left` returns index `3` (the `7` itself, the first element `≥ 7`), while `bisect_right` returns index `4` (the `9`, the first element `> 7`). One brackets the matches on the left, the other on the right. A common companion question is "what is the largest stored value strictly less than the target?" — its *strict predecessor*. With `bisect_left` giving index `3` for target `6`, the element just before it, at index `2`, is `5` — the strict predecessor of `6`. This is exactly how an ordered log store finds "the most recent record strictly before time `T`": `bisect_left` for `T`, then step one index left.

**A caveat that binary search does not fix.** Locating the insertion point is `O(log n)` — `log2(n)` comparisons. But *actually inserting* a new value into a sorted plain array is not cheap: every element after the insertion point must shift one slot to the right to make room, which is up to `n` moves — `O(n)` work. So binary search speeds up *lookup*, not *insertion into an array*. When values arrive already in increasing order, this is sidestepped by appending to the end (no shifting); when they can arrive out of order, the slow shift is what motivates other structures — balanced search trees, skip lists, sorted containers — that keep both lookup and insertion fast. Those are separate concepts; the point here is only that the `O(log n)` is a property of the *search*, not of mutating the array.

## Prerequisites

- [[arithmetic]]

## Sources

- `etc/study-notes.html` — "An ordered log store and the predecessor query": the predecessor query, the `bisect_left` / `bisect_right` distinction, and the insertion-point `O(n)` caveat.
