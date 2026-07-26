---
id: linked-list
title: Linked List
summary: "A linked list stores a sequence of values by putting each value in its own small record, called a node, and having every node hold — alongside its value — a pointer: a stored…"
type: concept
tags: [algorithms]
prereqs: [arithmetic]
sources: [study-notes.html#s9]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Linked List

## Summary

A linked list stores a sequence of values by putting each value in its own small
record, called a **node**, and having every node hold — alongside its value — a
**pointer**: a stored reference that says where the next node lives. You reach the
whole sequence through one starting pointer, the **head**, and you follow pointers
from node to node to travel along it. This is the opposite design choice from a
contiguous block of slots: a linked list cannot jump straight to "the i-th value"
(it must walk i pointers to get there), but once you are *standing at* a node it can
insert or delete a neighbour by rewriting only a pointer or two, without moving any
other value. That single trade — give up instant indexing, gain instant local
rewiring — is the whole point of the structure.

## Grounded explanation

**The defining object.** A linked list is built from **nodes**. A node is a tiny
bundle holding two things: a *value* (the element you actually want to store) and a
*pointer*. A pointer is simply a stored answer to the question "where is the next
node?" — a reference that lets you go from one node to another. In a **singly linked
list** each node holds one pointer, to the *next* node. In a **doubly linked list**
each node holds two pointers, one to the *next* node and one to the *previous* node,
so you can travel in both directions. The very last node's "next" pointer points at
nothing (a special empty value meaning "the list ends here"). You hold one pointer
from outside, the **head**, which names the first node; that single handle is your
only entry into the chain, and from it you reach every other node by following
pointers. There is no master table of "node 0, node 1, node 2"; the nodes can sit
anywhere, and the only thing tying them into an order is the chain of pointers.

**Why this is worth contrasting.** The natural alternative is to lay the values out
in one continuous run of equally sized slots — slot 0, then slot 1 right after it,
then slot 2, and so on (a *contiguous array*). Because the slots are the same size
and packed back-to-back, you can compute exactly where the i-th value sits by a
single piece of [[arithmetic]]: its position is the start of the run plus i times the
slot size. So an array reaches *any* value in a fixed number of steps regardless of
i — call this **constant-time** access, written **O(1)**, the notation for "the cost
does not grow as the collection grows." A linked list cannot do this. Its nodes are
scattered and the only way to find the i-th node is to start at the head and follow
i pointers, one after another. The work is therefore proportional to i: for a list of
length n, reaching deep into it costs on the order of n steps — **linear time**,
written **O(n)** ("cost grows in step with the collection's size"). This is the price
the linked list pays, and it is the first half of the trade.

**Why you would ever accept that price — the invariant that makes splicing cheap.**
Consider *removing* a value. In the contiguous array, the slots must stay packed with
no gaps, or the position-by-arithmetic trick breaks. So deleting the value in the
middle forces every value after it to slide one slot toward the front to close the
hole — work proportional to how many values follow, again O(n). In a linked list
nothing is packed and nothing must slide. The order is carried *only* by the pointers,
so to remove a node you simply make its neighbours point past it: the node before it
is told to point at the node after it, and the removed node is just dropped out of the
chain. That is a fixed amount of work — a couple of pointer rewrites — no matter how
long the list is: **O(1)**. The same is true for inserting a new node beside one you
are already standing at: you redirect a pointer or two and the newcomer is spliced in.
This is the structure's key insight, and the reason its cost profile is the mirror
image of the array's. We call this local rewiring a **splice**. The crucial caveat —
the thing that keeps the trade honest — is *"a node you are already standing at."* The
O(1) splice assumes you already hold the relevant node. If you only know "the i-th
one," you must first *walk* to it (the O(n) cost from before), so a splice by position
is not free; a splice given the node is. A doubly linked list strengthens this: because
each node also knows its predecessor, you can unhook a node knowing only that node
itself, with no separate search for "the one before it."

**The trade, stated plainly.** A contiguous array gives **O(1) indexing** (jump to any
position instantly) but **O(n) splicing** (insert/delete in the middle forces a shift).
A linked list gives the reverse: **O(n) indexing** (you must walk) but **O(1) splicing**
(rewire a pointer or two, given the node). Neither is "better"; you pick the one whose
cheap operation is the operation your problem repeats.

**A worked instance.** Take three nodes chained A → B → C: the head points at A, A's
next pointer points at B, B's next points at C, and C's next points at nothing. Now
delete the middle value B. You set A's next pointer to point at C instead of B. That
is the entire operation: **two pointer writes** (read where B pointed — to C — and
store that into A's next), and B falls out of the chain. The list is now A → C, and
the cost did not depend on the list having 3 nodes or 3 million; it is O(1). Compare
deleting the middle element of a contiguous array of 1000 values: to keep the slots
packed you must shift roughly the 500 values that came after the hole one slot
forward — about 500 moves, and that count grows with the array. Now instead *find* the
700th value in the linked list: you start at the head and follow 700 pointers, one per
step, before you arrive — about 700 pointer-follows, growing with how deep you reach.
The two examples show both halves of the trade on the same structure: cheap local
edits, expensive positional reach.

**Where the O(1) splice earns its keep (in plain terms).** Two everyday container ideas
are sequences with all the action at the ends. A *stack* only ever adds and removes at
one end (the most-recently-added value comes off first). A *queue* adds at one end and
removes at the other (the longest-waiting value comes off first). Both want their
add/remove to be O(1), and a doubly linked list — which can splice instantly at either
end because it holds both directions — delivers exactly that. A heavier example is an
*LRU (least-recently-used) cache*: a fixed-size store that, when full, evicts whichever
item was used longest ago. It keeps items in a doubly linked list ordered by recency;
every time an item is used it is spliced out of its spot and re-spliced at the
"most-recent" end, and eviction just drops the node at the "least-recent" end — each of
these is an O(1) splice on a node the cache already holds, which is precisely the
operation a linked list makes cheap.

## Prerequisites

- [[arithmetic]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the Linked list row
  (Python: manual; key ops: insert/del at node O(1), search O(n); reach for it when:
  O(1) splice, LRU cache, pointer work), read against the Dynamic array row (index
  O(1), insert/del mid O(n)) for the contrast.
