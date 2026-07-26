---
id: dynamic-array
title: Dynamic Array
summary: A dynamic array is a list that stores its elements in one unbroken run of memory cells and can grow as you add more.
type: concept
tags: [algorithms]
prereqs: [arithmetic]
sources: [study-notes.html#9]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Dynamic Array

## Summary

A dynamic array is a list that stores its elements in one unbroken run of memory cells and can grow as you add more. Reading the element at a given position is instant because the address of that cell is found by a single multiply-and-add. Adding one element to the end is, on average, also instant: when the run of cells fills up the structure quietly allocates a fresh run of double the size and copies everything across, but because the size doubles each time these expensive copies happen so rarely that the cost spread over all the additions stays constant. The price you pay is that inserting or removing an element anywhere except the end forces every element after it to slide over, which is slow. Python's `list` and C++'s `vector` are dynamic arrays.

## Grounded explanation

**The central object.** A dynamic array keeps its elements in a *contiguous block* of memory: a single stretch of memory cells with no gaps, laid out one element immediately after the next. Memory is a long row of numbered cells; the *address* of a cell is its number. The block has two numbers attached. Its **length** is how many elements you have actually stored. Its **capacity** is how many cells the block can hold before it is full. The defining rule (the invariant the structure always keeps true) is *capacity ≥ length*: there is always room for what is stored, usually with some spare cells at the end waiting to be filled. This spare room is the whole trick — it is what lets the array grow cheaply.

**Random access is one step.** Because the elements sit back-to-back and every element occupies the same fixed number of bytes (call it the *element size*), the position of element number `i` can be computed directly. Let `base` be the address of the first element. Then the address of element `i` is

> `address = base + i × elementsize`

— a single multiplication and a single addition, both of which are [[arithmetic]]. It does not matter whether `i` is `2` or `2,000,000`: the work is the same fixed amount. We call an operation whose cost does not grow with the number of stored elements **O(1)**, or *constant time* (the "n" inside the O is the length; O(1) means the cost ignores n). So reading or writing `a[i]` by index is O(1). This is the dynamic array's headline strength: instant access to any position.

**Appending, and why it is usually cheap.** *Appending* means adding one element just past the current last one, growing the length by one. If there is a spare cell (capacity > length), appending is trivial: write the element into the next free cell and increase the length by one — O(1). The problem is the moment the block is full (capacity = length) and you append again. There is no spare cell, and you cannot simply extend the block, because the cells right after it may already belong to other data. So the structure must **resize**: ask the memory system for a brand-new, larger contiguous block, copy all the existing elements across into it one by one, and only then write the new element. Copying every element is work proportional to the length — an operation whose cost grows in step with n is called **O(n)**, or *linear time*. A single append can therefore be expensive.

**The doubling insight.** The non-obvious design choice that makes the structure work is *how much* larger the new block should be. The answer is: **double the capacity** each time. Doubling, rather than adding a fixed number of cells, is what keeps appends cheap on average. To see why, we reason about *amortized* cost — the total cost of a long run of operations divided by the number of operations, i.e. the true average per operation even though individual ones vary. The claim is that appending is **amortized O(1)**: any single append might be O(n), but across many appends the average is constant.

Here is the justification, not just the result. Suppose you start with capacity 1 and append `n` elements. Resizes happen only when the block is full, and each resize doubles the capacity, so resizes occur at lengths `1, 2, 4, 8, …` — the powers of two. At a resize that takes the capacity to size `k`, the copying cost is the `k` (more precisely, the elements present, which is the old capacity) elements moved across. Adding up the copy work over all resizes needed to reach `n` elements gives a sum of powers of two:

> `1 + 2 + 4 + 8 + … + (up to about n)`

A run of doubling numbers has a special property: each term equals the sum of all the smaller terms plus one, so the whole sum is always just under *twice the last term*. Since the last term is at most `n`, the total copying done across **all** resizes is less than `2n`. Spread that `2n` total over the `n` appends that triggered it and the average is under `2` copies per append — a constant, independent of how large `n` grows. That is the amortized O(1) guarantee, and it rests entirely on doubling: the costly copies get *rarer* exactly as fast as they get *bigger*, so their total stays linear instead of exploding.

**Insertion and deletion in the middle.** The same contiguity that makes access fast makes mid-list editing slow. To insert an element at position `i`, every element currently at `i` and beyond must move one cell to the right to open a gap — and to delete at `i`, every later element must move one cell left to close the gap. The number of elements that shift is proportional to how many come after the insertion point, so in the worst case (inserting or deleting near the front) it is O(n). *Searching* for a value by its content, when the array is not sorted, is likewise O(n): you may have to inspect every element. These are the costs the cheat sheet records as "insert/del mid O(n), search O(n)".

**Worked instance.** Start with an empty dynamic array of capacity 1, and append five elements, calling them `e0` through `e4`. Track length, capacity, and copies:

- Append `e0`: capacity 1, length 0 → there is room, write it. Length 1. No copy.
- Append `e1`: length 1 equals capacity 1 → full. Resize 1 → 2, copying the 1 existing element. Then write `e1`. Length 2. **Copies so far: 1.**
- Append `e2`: length 2 equals capacity 2 → full. Resize 2 → 4, copying the 2 existing elements. Write `e2`. Length 3. **Copies so far: 1 + 2 = 3.**
- Append `e3`: capacity 4, length 3 → room. Write it. Length 4. No copy.
- Append `e4`: length 4 equals capacity 4 → full. Resize 4 → 8, copying the 4 existing elements. Write `e4`. Length 5. **Copies so far: 1 + 2 + 4 = 7.**

So five appends triggered resizes at capacities `1 → 2 → 4 → 8` and cost `1 + 2 + 4 = 7` total copies. Note `7` is just under `2 × 5 = 10` — the "less than 2n" bound in action — and the seven copies were spread over five appends, well under two each. Most appends (`e0`, `e3`) cost nothing extra; the doubling makes the expensive ones rare.

Now exercise the other two operations on this same array. *Index access*: with element size 8 bytes and the block's first element at address `base`, reading `a[3]` computes `base + 3 × 8 = base + 24` — one multiply, one add — and jumps straight there, regardless of length. *Mid-insertion cost*: had this array instead held 1000 elements and you inserted a new element at the very front (position 0), all 1000 existing elements would each have to slide one cell to the right before the new one could be written — 1000 moves for a single insert, the O(n) penalty that the fast indexing cannot avoid.

**Putting it together.** A dynamic array buys you instant indexed access and amortized-instant growth at the end, at the cost of slow edits in the middle — which is exactly why you reach for it whenever you need an ordered sequence with fast access by position and mostly append at the end.

## Prerequisites

- [[arithmetic]]

## Sources

- `study-notes.html` §9 "Data structures cheat sheet" — the dynamic array row (`list`: index O(1), append O(1)*, insert/del mid O(n), search O(n)) and the footnote "append is amortised O(1)".
