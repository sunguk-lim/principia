---
id: deque
title: Deque
summary: A deque — short for double-ended queue, and pronounced "deck" — is a sequence of values that lets you add a value at either end and remove a value from either end, and lets you do…
type: concept
tags: [algorithms]
prereqs: [linked-list, queue]
sources: [study-notes.html#s9]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Deque

## Summary

A deque — short for *double-ended queue*, and pronounced "deck" — is a sequence of
values that lets you add a value at either end and remove a value from either end,
and lets you do all four of those things cheaply: each one is a fixed amount of work
that does not grow as the deque gets longer (constant time, written **O(1)**). That
two-ended cheapness is the whole identity of the structure. It makes a deque a
superset of two simpler containers: if you only ever touch one end you have a *stack*
(last value in is the first out), and if you add at one end while removing from the
other you have a *[[queue]]* (first value in is the first out) — a deque does both, plus
the two combinations they each forbid. It is naturally built on top of a doubly
[[linked-list]], because that structure already makes inserting or deleting a node at
either end an O(1) splice. Its signature advanced use is the **monotonic deque**,
which answers "what is the largest value in a sliding window?" across an entire array
in total time proportional to the array's length.

## Grounded explanation

**The defining object, and why a [[linked-list]] backs it.** A deque is a sequence
with two ends — call them the **front** and the **back** — and it offers four
operations: push at the front, pop (remove) from the front, push at the back, pop
from the back. The defining promise is that every one of these four is **O(1)**: the
cost is a fixed handful of steps no matter how many values the deque holds (the
notation O(1) means "the cost does not grow as the collection grows," and its
opposite, O(n), means "the cost grows in step with the collection's size n"). The
prerequisite [[linked-list]] already explains why a *doubly* linked list delivers
exactly this. Recall that a doubly linked list stores each value in its own small
record (a *node*) that holds, besides the value, a pointer to the *next* node and a
pointer to the *previous* node; the structure's key property is that inserting or
removing a node you are already standing at costs only a couple of pointer rewrites
— a *splice* — regardless of length. A deque keeps a handle on the first node and a
handle on the last node, so it is always "standing at" both ends at once. Pushing at
the back is one splice beside the last node; popping the front is one splice beside
the first node; and because the list is *doubly* linked, popping a node also lets you
reach the node before it with no search, so removal at either end is O(1) too. The
deque is thus not a new mechanism — it is a doubly [[linked-list]] with its two ends
exposed as the only places you are allowed to touch.

**Why "both ends" is the point — stack and queue as the two halves it unifies.** Two
everyday containers each use a *subset* of the deque's four operations. A **stack**
uses one end only: you push values onto that end and pop them off the same end, so
the most-recently-added value is the first to leave (this last-in-first-out discipline
is what makes a stack the right tool for undo, for matching nested brackets, and for
remembering where to backtrack). A **queue** uses two ends but pairs them in a fixed
way: you push at the back and pop from the front, so the longest-waiting value leaves
first (first-in-first-out — the discipline behind processing things in arrival order,
such as exploring a graph level by level). A deque imposes no such restriction; it
permits all four end-operations freely. So whatever a stack can do, a deque can do by
ignoring one end, and whatever a queue can do, a deque can do by using the two ends in
the queue pattern — and it can additionally do what *neither* allows, such as pushing
back onto the front a value it just popped, or peeling values off both ends toward the
middle. That extra freedom is not idle: it is exactly what the monotonic deque needs.

**The signature use — the monotonic deque, and the invariant that makes it work.**
Here is the problem it solves. You are given an array and a fixed window width, and
the window slides one step at a time from the array's left end to its right end; at
each position you must report the **maximum** value currently inside the window. The
naive method re-scans all the values in every window, costing work proportional to the
window width at each of the array's positions — too slow. The monotonic deque does the
whole sweep in total time proportional only to the array's length, **O(n)**. The
trick is to keep in the deque not values but the *positions* (indices) of array
elements, and to maintain one **invariant**: the values at the stored positions are
strictly **decreasing** from front to back. Maintaining that invariant requires the
deque's two-ended freedom in two distinct moves:

- **Cleaning the back (this is the non-obvious step).** When a new element arrives, you
  first pop positions off the *back* of the deque as long as the new element's value is
  **greater than or equal to** the value at the back. The justification is a small
  argument worth stating, not just asserting: any earlier element that is no larger
  than the newcomer, *and* sits to the newcomer's left, can never again be a window
  maximum — every future window that would contain that earlier element also contains
  the newcomer (which is at least as large and stays in view at least as long), so the
  earlier one is permanently dominated and safe to discard. After this cleaning you
  push the new position on the back, and the decreasing invariant is restored.
- **Expiring the front.** As the window slides right, its left edge moves past old
  positions. If the position at the *front* of the deque has fallen outside the current
  window, you pop it from the front. (It might still hold a large value, but it has
  simply left the window, so it can no longer be the answer.)

Because the deque is kept decreasing and the front is kept inside the window, the value
at the **front position is always the current window's maximum** — that is the payoff
of the invariant. Reading the answer is therefore free: just look at the front.

**A worked instance — array `[1, 3, -1, -3, 5]`, window width 3.** Index the array
`0..4`. I sweep left to right, and for each new index I first clean the back, then drop
an out-of-window front, then (once the window is full) read the front as the maximum.
The deque holds *indices*; I show the values in parentheses for clarity.

- **i = 0 (value 1).** Deque empty; push 0. Deque: `[0(1)]`. Window not full yet.
- **i = 1 (value 3).** Back holds index 0 with value 1, and `3 >= 1`, so 1 is dominated
  — pop index 0 from the back. Deque now empty; push 1. Deque: `[1(3)]`. Still not full.
- **i = 2 (value -1).** Back holds value 3, and `-1 < 3`, so the invariant already holds
  — no back cleaning; push 2. Deque: `[1(3), 2(-1)]` (values 3, -1: decreasing, good).
  The window now spans indices 0–2 and is full; the front is index 1, so the **maximum
  is 3**.
- **i = 3 (value -3).** Back holds value -1, and `-3 < -1`, so no cleaning; push 3.
  Deque: `[1(3), 2(-1), 3(-3)]` (values 3, -1, -3: decreasing). The window now spans
  indices 1–3; the front index 1 is still inside it, so the **maximum is 3**.
- **i = 4 (value 5).** Clean the back: value at back is -3 and `5 >= -3`, pop index 3;
  now back value is -1 and `5 >= -1`, pop index 2; now back value is 3 and `5 >= 3`, pop
  index 1 — the deque empties because 5 dominates everything before it. Push 4. Deque:
  `[4(5)]`. The window now spans indices 2–4; check the front: index 4 is inside, so the
  **maximum is 5**.

The reported maxima are **3, 3, 5**, one per full-window position — and at i = 4 you
can see all three moves fire at once (three back-pops, then the push), which is why this
is a non-degenerate trace rather than one where the deque never empties.

**Why this is O(n), not slower.** The back-cleaning loop at i = 4 popped three things,
which might look like the cost can spike. But count globally instead of per step: each
index is **pushed onto the deque exactly once** (when its element is first seen) and is
**popped at most once** thereafter (either cleaned off the back by a later larger
element, or expired off the front when it leaves the window) — after it is popped it is
gone forever. So across the entire sweep the total number of push-and-pop operations is
at most two per index, i.e. proportional to n. A few steps doing several pops are
exactly paid for by other steps doing none; the *total* work is linear. This
amortized-counting argument — "each element enters once and leaves once" — is the
heart of why the monotonic deque turns a window-maximum scan from quadratic into O(n),
and it leans entirely on the deque's ability to push and pop at *both* ends.

## Prerequisites

- [[linked-list]]
- [[queue]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the Deque row (Python:
  `collections.deque`; key ops: push/pop both ends O(1); reach for it when:
  sliding-window max via monotonic deque), read against the Stack row (push/pop one
  end O(1); matching, undo, DFS) and the Queue row (append/popleft O(1); BFS,
  level-order) for the subset relationship, and the "problem signal → structure" note
  ("Next greater / window maximum → monotonic stack or deque"). The Linked list row in
  the same table supplies the O(1)-splice backing.
