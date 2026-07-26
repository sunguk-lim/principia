---
id: heap
title: Heap
summary: A heap (more precisely a binary heap) is a container that lets you repeatedly grab the smallest item without ever fully sorting your data.
type: concept
tags: [algorithms]
prereqs: [arithmetic]
sources:
  - etc/study-notes.html — "Data structures cheat sheet" / "Essential Python idioms" (heapq)
status: explained
created: 2026-06-23
updated: 2026-06-29
---

# Heap

## Summary

A heap (more precisely a *binary heap*) is a container that lets you repeatedly grab the smallest item without ever fully sorting your data. You can insert an item and pull out the current minimum, and each of those two operations costs only about `log n` steps (where `n` is the number of items) instead of the `n` steps a naive scan-for-the-minimum would cost. It achieves this by keeping items in a clever half-sorted arrangement — just sorted *enough* that the smallest is always sitting in front, but never paying to sort the rest. That makes it the structure of choice whenever a program must keep handing out the most extreme element from a changing collection: a scheduler picking the next earliest task, finding the k smallest of a stream, or always advancing the closest frontier in a shortest-path search.

## Grounded explanation

**The problem it solves.** Suppose you hold a bag of numbers and you will repeatedly ask: "give me the smallest one, remove it, and let me keep adding more." If you keep the bag unsorted, finding the minimum means scanning every item — `n` comparisons each time. If instead you keep the bag fully sorted, finding the minimum is instant, but *inserting* a new item means shoving it into the right slot and shifting everything after it — again proportional to `n`. A heap escapes both costs: it keeps the data only *partially* ordered, just enough that the minimum is always known, so both inserting and removing-the-minimum cost only about `log n` steps. The phrase `log n` here means: roughly the number of times you can halve `n` before reaching 1 (for a thousand items that is about ten steps, for a million about twenty) — vastly cheaper than `n` itself.

**The shape: a complete binary tree.** Picture the items arranged as a *tree* — a branching diagram where each item (a *node*) sits above at most two items below it, called its *children*; the item above a node is its *parent*; the single topmost node with no parent is the *root*. A *binary* tree means each node has at most two children. A *complete* binary tree adds a packing rule: every level (every horizontal row of the tree) is entirely filled except possibly the last, and the last row is filled from the left with no gaps. This packing rule is what forces the tree to stay shallow: with `n` nodes packed this way, the tree is only about `log n` rows deep, because each new full row roughly *doubles* the number of nodes. That depth is exactly why the operations below cost `log n` — they walk from the root to the bottom or back, which is a `log n`-length path.

**The clever trick: store the tree as a flat array, with no pointers.** You might expect a tree to need explicit links — each node remembering where its children live in memory. A heap needs none. Because the tree is *complete*, you can lay its nodes into a plain array (an indexed list of slots, position `0`, `1`, `2`, …) by reading the tree top-to-bottom, left-to-right. The root goes in slot `0`, its two children in slots `1` and `2`, the next row in slots `3, 4, 5, 6`, and so on. The magic is that family relationships then become pure index [[arithmetic]]: for the node sitting at index `i`,

- its **left child** is at index `2i + 1`,
- its **right child** is at index `2i + 2`,
- its **parent** is at index `(i − 1) // 2`, where `//` means integer division (divide and throw away any remainder).

Check the consistency: the left child of index `i` is `2i + 1`; running the parent formula on it gives `(2i + 1 − 1) // 2 = (2i) // 2 = i`, back to where we started. So moving "up to my parent" or "down to a child" is just multiplying or dividing an index — no stored links, no memory chasing. This is *why* a heap is fast and compact: the entire tree structure is implicit in the addition and division of integers.

**The invariant: the heap property.** What keeps the minimum always in front is a single rule maintained at all times, called the *heap property*: **every parent's value is less than or equal to both of its children's values** (this is a *min-heap*; flip the comparison to "greater than or equal" and you get a *max-heap* that surfaces the largest instead). Notice this is a *local* promise — it only constrains each parent against its own children, not against distant cousins. But locally promising "I am no bigger than my children" at every node forces a *global* consequence: the root, having no parent and being ≤ its children, who are ≤ *their* children, and so on, must be ≤ every node in the tree. So the smallest item is guaranteed to sit at index `0`, readable instantly. The heap never sorts the rest — it only enforces this one inequality everywhere, which is far less work than total order yet enough to pin the minimum at the top.

**Insert = append, then sift up.** To add an item, place it in the first free slot — the next array index, which by the packing rule is the leftmost open spot in the bottom row. This keeps the tree complete but may break the heap property, because the newcomer could be smaller than its parent. Repair it by *sifting up*: compare the new item with its parent (found by the `(i − 1) // 2` formula); if it is smaller, swap them; repeat from the item's new position. Each swap lifts the item one row toward the root, and since the tree is only `log n` rows deep, at most `log n` swaps are needed. Why does this restore the invariant rather than just relocate the problem? Each swap only moves a *smaller* value above a *larger* one, which is exactly the direction the property wants, and it cannot violate the property elsewhere because the item we lifted is smaller than what was there before. We stop the moment the item is no longer smaller than its parent — at which point every parent-child pair is correct again.

**Pop-minimum = take the root, refill, then sift down.** To remove and return the smallest item, take the root at index `0` — that *is* the minimum. Now the root slot is empty, but we cannot leave a hole in a complete tree. So move the *last* element (the final array slot) up into the root and shrink the array by one; the tree stays complete. The moved element is probably too big to be at the top, so *sift down*: look at its two children (indices `2i + 1` and `2i + 2`), find the smaller of them, and if that child is smaller than our element, swap with it; repeat from the new position. We descend toward the *smaller* child specifically because that child must become the new parent of both — it has to be ≤ its sibling too, and the smaller one satisfies that. Each step moves down one row, so again at most `log n` swaps. We stop when the element is no larger than both children, restoring the property.

**Worked instance.** Take a min-heap and push the values `5, 3, 8, 1` one at a time. Write the array as `h`, with index `0` on the left.

- Push `5`: `h = [5]`. It is the root; nothing to sift.
- Push `3`: append at index `1`, giving `h = [5, 3]`. Its parent is at `(1 − 1) // 2 = 0`, value `5`. Since `3 < 5`, swap → `h = [3, 5]`. The new item is now at index `0` (the root); stop.
- Push `8`: append at index `2`, giving `h = [3, 5, 8]`. Its parent is at `(2 − 1) // 2 = 0`, value `3`. Since `8 > 3`, the property already holds; stop. `h = [3, 5, 8]`.
- Push `1`: append at index `3`, giving `h = [3, 5, 8, 1]`. Its parent is at `(3 − 1) // 2 = 1`, value `5`. Since `1 < 5`, swap → `h = [3, 1, 8, 5]`. The `1` is now at index `1`; its parent is at `(1 − 1) // 2 = 0`, value `3`. Since `1 < 3`, swap → `h = [1, 3, 8, 5]`. The `1` reached the root; stop.

The array `[1, 3, 8, 5]` is **not** sorted — `8` sits before `5` — yet the smallest value, `1`, is correctly at the front, and every parent is ≤ its children (parent `1` ≤ children `3` and `8`; parent `3` ≤ child `5`). That is the whole point: half-sorted, minimum exposed.

Now pop the minimum three times.

- **Pop 1.** The root `1` is the answer. Move the last element (`5` at index `3`) to the root and shrink: `h = [5, 3, 8]`. Sift down from index `0`: children are at index `1` (`3`) and index `2` (`8`); the smaller is `3`. Since `5 > 3`, swap → `h = [3, 5, 8]`. The element (`5`) is now at index `1`; its children would be at indices `3` and `4`, which are past the end — no children, so stop. Returns **1**.
- **Pop 3.** The root `3` is the answer. Move the last element (`8` at index `2`) to the root and shrink: `h = [8, 5]`. Sift down from index `0`: only child is at index `1` (`5`); index `2` is past the end. Since `8 > 5`, swap → `h = [5, 8]`. Stop. Returns **3**.
- **Pop 5.** The root `5` is the answer. Move the last element (`8` at index `1`) to the root and shrink: `h = [8]`. Sift down: no children. Returns **5**.

The values came out `1`, then `3`, then `5` — in sorted order. But notice what we *paid*: each push and each pop touched only a `log n`-length path from root to leaf, never a full sort of all items. The heap delivered sorted-order access to the extremes while only ever maintaining one local inequality. This is exactly why it powers task schedulers (always run the highest-priority job next), top-k selection over a stream, merging many sorted lists, and shortest-path search that always expands the nearest unvisited node first — all cases where you need the current extreme again and again, but never need the bulk of the data sorted.

## Prerequisites

- [[arithmetic]]

## Sources

- `etc/study-notes.html` — "Data structures cheat sheet" (Heap / priority queue: push/pop O(log n), peek O(1); reach for it on top-k, running min/max, Dijkstra, merge-k) and "Essential Python idioms" (`heapq.heappush` / `heapq.heappop` min-heap, max-heap via negation, `heapq.heapify` O(n) build).
