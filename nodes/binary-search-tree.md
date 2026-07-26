---
id: binary-search-tree
title: Binary Search Tree
summary: A binary search tree (BST) stores ordered data not as a contiguous array but as a branching structure of linked nodes, arranged so that the same halving idea behind binary-search…
type: concept
tags: [algorithms]
prereqs: [binary-search]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Binary Search Tree

## Summary

A binary search tree (BST) stores ordered data not as a contiguous array but as a branching structure of linked nodes, arranged so that the same halving idea behind [[binary-search]] works on the structure itself. Each node holds one key and links to at most two children, a left and a right, under one rule — the *BST property*: every key in a node's left branch is smaller than the node's key, and every key in its right branch is larger. To look something up you start at the top and, at each node, compare and step left or right, discarding a whole branch with every comparison — about `log2(n)` steps for `n` keys, exactly the speed of [[binary-search]]. The decisive gain over a sorted array is that a BST also *inserts* and *deletes* in about `log2(n)` steps: you splice a new node into place by adjusting one link, with no shifting of other elements. That is its reason to exist — it keeps both lookup and update fast when data changes, where a sorted array kept lookup fast but made insertion slow.

![Binary search tree built from 5,3,8,1,4 (root 5, left 3 with children 1 and 4, right 8); a descend-loop register traces looking up key 4 in three comparisons, one comparison per level discarding a whole branch](binary-search-tree.svg)

## Grounded explanation

**The problem it answers, and why a sorted array is not enough.** [[binary-search]] gives a fast lookup — about `log2(n)` comparisons, where `log2(n)` is the number of times you can halve a count of `n` down to one — but only on a *sorted array*: a row of values laid out in adjacent numbered slots, in increasing order. As noted in [[binary-search]], that arrangement has a weakness. Finding *where* a new value belongs is cheap (`log2(n)` comparisons), but actually *inserting* it is not: every value sitting after the insertion point must slide one slot over to open a gap, which is up to `n` moves of work. So a sorted array is excellent when the data is fixed but costly when values keep arriving and must be slotted in out of order. A binary search tree is the structure that removes this weakness while keeping the fast lookup.

**The central object: a tree of linked nodes.** A *node* is a small record holding one *key* (the value being stored) plus two links called *children*: a *left child* and a *right child*. A link may be empty, meaning "no child on that side." One node is the *root* — the single entry point, with nothing above it. Reading the links downward, every node is reached from exactly one node above it (its *parent*), and following links never loops back; this downward-branching, loop-free shape is what the word *tree* names here. A node with no children is a *leaf*. The *depth* of a node is how many links you cross to reach it from the root (the root has depth `0`), and the tree's *height* is the depth of its deepest node — this height is what the lookup cost will turn out to depend on.

**The defining rule: the BST property.** The keys are not placed arbitrarily. For *every* node in the tree, the rule holds that all keys stored anywhere in its left child's branch are *smaller* than that node's own key, and all keys anywhere in its right child's branch are *larger*. ("Branch" means the node and everything reachable below it.) This single rule, applied at every node at once, is the *BST property*, and it is the tree's analogue of "the array is sorted." It is what lets a comparison at one node condemn an entire branch — the same logic by which sortedness let [[binary-search]] throw away half an array.

**The one step of lookup, and why it discards a whole branch.** To find whether a key is present, start at the root and repeat one step. Compare the key you want against the current node's key. Three outcomes:

- They are *equal* — the search succeeds; this node holds it.
- The wanted key is *smaller*. By the BST property every key in the right branch is larger than this node's key, hence larger than what you want, so none of them can match; discard the entire right branch and step to the left child.
- The wanted key is *larger*. Symmetrically, the whole left branch is too small to match; discard it and step to the right child.

If the link you must follow is empty, the key is absent. Each comparison throws away one branch and descends one level, so the search visits one node per level — at most *height* nodes. This is the same "one comparison kills half the candidates" mechanism as [[binary-search]]; the difference is only that the halves are now branches of a linked tree rather than halves of an array index range. When the tree is well-shaped, each branch holds roughly half the remaining keys, so the height is about `log2(n)` and lookup costs about `log2(n)` comparisons.

**The decisive win: insertion costs no shifting.** Here the tree beats the sorted array. To insert a new key, run the very same downward walk you would use to look it up. Compare at each node and step left or right until you reach an *empty* link — the spot where the key would have been found had it existed. Place the new node there by filling that one empty link. Nothing else in the tree moves; you adjusted a single link. Because the walk descends one level per comparison, this is about `log2(n)` work — the same as the lookup — and crucially with *no shifting* of existing nodes. Contrast the sorted array, where opening a slot forced up to `n` elements to slide. This is exactly the trade the source draws between two cases of an ordered log store: when timestamps "arrive in increasing order" (Case A) a sorted array with appends suffices, but when "timestamps may arrive out of order" (Case B) "a plain array cannot [stay sorted] cheaply," and a *balanced search tree* (a BST kept well-shaped, defined below) gives `O(log n)` for *both* insertion and the predecessor query. The notation `O(log n)` just means "grows like `log2(n)`" — the cost rises only as fast as the number of halvings, not as fast as `n` itself. Deletion follows the same spirit: find the node, then relink its children so the BST property still holds, again touching only links near that node rather than shifting an array.

**Ordered operations come for free.** Because the BST property orders the keys spatially — smaller to the left, larger to the right — visiting the tree in the order "everything in the left branch, then this node, then everything in the right branch," applied recursively, emits the keys in increasing order. This *in-order traversal* yields a sorted listing without any separate sort. The same ordering makes neighbor questions cheap: the *successor* (next-larger stored key) and *predecessor* (next-smaller — the very predecessor query the source poses for the log store) are found by a short walk, and a *range query* — every key between two bounds — is a walk to one bound followed by an in-order sweep to the other. All of these stay near `log2(n)` when the tree is well-shaped. (A *binary search tree* should not be confused with a *heap*, a different binary-tree structure whose rule only relates each node to its children by size and which gives no sorted ordering; the BST property is the stronger left-smaller/right-larger rule used here.)

**The catch, and what fixes it.** The lookup and insertion costs above were all stated as "about `log2(n)` *when the tree is well-shaped*" — meaning the height stays near `log2(n)`. Nothing in the BST property forces that. If keys are inserted *already in sorted order* — say `1`, then `2`, then `3`, then `4` — each new key is larger than all before it, so it always attaches as a right child of the previous one. The tree becomes a single rightward chain with no branching: a structure shaped like a list, of height `n - 1`. Lookup then walks all `n` nodes, costing `O(n)` and erasing the advantage. This *degenerate* case is why plain BSTs are not the end of the story. *Balanced* search trees — variants such as AVL trees and red-black trees — add bookkeeping that detects a branch growing too tall on insertion and locally restructures (rotating a few links) to keep the height pinned near `log2(n)`, guaranteeing `O(log n)` for lookup, insertion, and deletion regardless of arrival order. This is the "balanced search tree" the source's Case B reaches for. The balancing mechanics are a topic of their own; the point here is the guarantee they buy.

**The trade, stated plainly.** A sorted array with [[binary-search]] gives fast `O(log n)` lookup but slow `O(n)` insertion — ideal for *static* data fixed up front. A balanced binary search tree gives `O(log n)` for *both* lookup and insertion — ideal for *dynamic* data that changes over time, the out-of-order Case B. You trade the array's compact, shift-on-insert layout for a linked, splice-on-insert one, and in exchange insertion stops being the slow operation.

**Worked instance.** Insert the keys `5, 3, 8, 1, 4` into an empty tree, in that order. (These are deliberately *not* pre-sorted, so the tree genuinely branches rather than degenerating into a chain.)

- Insert `5`: the tree is empty, so `5` becomes the root.
- Insert `3`: compare with root `5`; `3 < 5`, step left; the left link is empty, so `3` becomes the root's left child.
- Insert `8`: compare with `5`; `8 > 5`, step right; the right link is empty, so `8` becomes the root's right child.
- Insert `1`: compare with `5` (`1 < 5`, go left to `3`); compare with `3` (`1 < 3`, go left); empty, so `1` becomes the left child of `3`.
- Insert `4`: compare with `5` (`4 < 5`, go left to `3`); compare with `3` (`4 > 3`, go right); empty, so `4` becomes the right child of `3`.

The resulting tree: root `5`, with left child `3` and right child `8`; the `3` in turn has left child `1` and right child `4`; the `8` is a leaf. Check the BST property at the root: its left branch holds `{3, 1, 4}`, all smaller than `5`; its right branch holds `{8}`, larger. At node `3`: left branch `{1}` smaller, right branch `{4}` larger. The rule holds everywhere.

Now *look up* `4`. Start at root `5`: `4 < 5`, step left to `3`. At `3`: `4 > 3`, step right to `4`. At `4`: equal — found. Three comparisons, each descending one level, exactly the branch-discarding walk described above.

Now read the tree *in order* — left branch, node, right branch, recursively. From the root: first its left branch (which itself gives `1`, then `3`, then `4`), then the root `5`, then its right branch (`8`). The output is `1, 3, 4, 5, 8` — sorted, produced with no sorting step.

Finally, *insert* `6`. Walk down: at `5`, `6 > 5`, go right to `8`; at `8`, `6 < 8`, go left; that link is empty, so `6` becomes the left child of `8`. Two comparisons, one new link filled, and not a single existing node moved — the `O(log n)`, no-shift insertion that a sorted array could not offer.

## Prerequisites

- [[binary-search]]

## Sources

- `etc/study-notes.html` — "An ordered log store and the predecessor query," Case A vs Case B: when timestamps arrive out of order, "a plain array cannot [stay sorted] cheaply," so "use a balanced search tree" for `O(log n)` insertion *and* the predecessor query — the trade this node builds on against the sorted-array `O(n)` insert.
