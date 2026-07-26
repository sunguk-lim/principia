---
id: queue
title: Queue
summary: "A queue is a collection that hands its values back in the exact order they arrived: the first value put in is the first value taken out — a discipline called FIFO, short for…"
type: concept
tags: [algorithms]
prereqs: [linked-list, dynamic-array]
sources: [study-notes.html#s9]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Queue

## Summary

A queue is a collection that hands its values back in the exact order they arrived:
the first value put in is the first value taken out — a discipline called **FIFO**,
short for *first-in, first-out*. You only ever do two things to it. You **enqueue**, which
adds a new value at the **back** (the most-recently-arrived end), and you **dequeue**,
which removes and returns the value at the **front** (the longest-waiting end). Because
adds happen at one end and removals at the other, the line never reorders: values leave
in the same sequence they joined, exactly like people waiting their turn. The whole value
of the structure is this fairness — in-order, no-cutting service — and the engineering job
is to make both the add-at-back and the remove-from-front cost a fixed, tiny amount of work
no matter how long the line grows.

## Grounded explanation

**The defining object and its one rule.** A queue is a sequence with a strict access rule:
you may only add at one designated end, the **back**, and only remove from the other
designated end, the **front**. Adding is called **enqueue**; removing-and-returning is
called **dequeue**. The rule has a name — **FIFO**, *first-in, first-out* — and it is the
entire concept: whichever value has been waiting longest is the next one to leave. Contrast
this with the other end-discipline you might impose on a sequence, where you add and remove
at the *same* end so the most-recently-added value comes off first (*last-in, first-out*,
a *stack*); that one reverses arrival order. A queue preserves it. Everything else about a
queue is in service of enforcing this one rule cheaply.

**Why "cheaply at both ends" is the hard part.** The obvious way to store a sequence is a
contiguous run of equally sized slots — slot 0, then slot 1 packed right after it, and so on
(a [[dynamic-array]]; in Python, a `list`). Appending a new value at the back of such a run is
fine: you write it into the next free slot, a fixed amount of work that does not grow as the
collection grows — **constant time**, written **O(1)** (the notation for "the cost does not
grow with the collection's size"). But a queue must remove from the *front*, and there the
contiguous layout betrays you. To stay packed with no gap at the start, removing the first
value forces every remaining value to slide one slot toward the front to fill the hole — work
proportional to how many values remain, which for a collection of size n is on the order of n
steps: **linear time**, written **O(n)** ("cost grows in step with the size"). So a naive
array-backed queue makes one of its two required operations slow. (This is exactly why, in
Python, removing the first element of a list with `list.pop(0)` is avoided: it is that O(n)
front-shift in disguise.) A queue needs **O(1) at *both* ends**, and a plain array cannot give
the front for free.

**The insight: back it with a structure whose ends are both cheap.** This is precisely the
operation a [[linked-list]] makes cheap. Recall its trade: a [[linked-list]] gives up instant
jump-to-the-i-th-value but gains **O(1) splicing** — inserting or removing a node, *given that
node*, costs only a pointer rewrite or two, no matter how long the chain is. A queue holds two
nodes from outside: a handle on the **front** node and a handle on the **back** node. To
dequeue, you read the value at the front node and advance the front handle to the next node —
a splice at a node you already hold, O(1). To enqueue, you attach a new node after the back
node and advance the back handle to it — again a splice at a node you already hold, O(1). The
front-shift that crippled the array never happens, because a [[linked-list]] carries its order
in pointers, not in packed positions; removing the front node disturbs nothing else. (The same
guarantee can be had from an *array cousin* called a circular buffer — a fixed-size array where
the front and back wrap around the ends instead of shifting — but the [[linked-list]] backing is
the one that needs no fixed capacity and shows the O(1)-at-both-ends property most directly. In
Python the ready-made version is `collections.deque`, whose `append` adds at the back and whose
`popleft` removes from the front, each O(1).)

**Why FIFO is the point, not an accident.** The reason you reach for a queue rather than any
old container is that *in-order, fair processing* is the thing your problem needs. Whatever has
waited longest is served next; nothing jumps the line. This shows up wherever order of arrival
must be honoured: a scheduler's run-queue hands the processor to whichever task has been ready
longest; a producer–consumer buffer lets a fast producer drop items at the back while a slower
consumer takes them from the front in the same sequence they were produced. The most
instructive use is **breadth-first search (BFS)** — a way of exploring a network of connected
items ("nodes") outward from a start. BFS keeps a queue of nodes it has discovered but not yet
explored, called the *frontier*. It dequeues a node, looks at that node's immediate neighbours,
and enqueues each newly seen neighbour at the back. Because the queue is FIFO, every node sitting
at distance 1 from the start is dequeued (and so explored) before any node at distance 2, which
in turn comes before any at distance 3 — the search fans out one full "ring" at a time. That
level-by-level order is a direct consequence of FIFO, and it is what makes BFS find the
*fewest-edges* route to a node: the first time BFS reaches a node, it has arrived by the shortest
path counted in number of edges, because shorter rings were fully drained first.

**A worked instance — arrival order preserved.** Start with an empty queue and enqueue three
values in sequence: A, then B, then C. After enqueuing A the line is `A` (A is both front and
back). Enqueue B: it attaches behind A, giving front→`A B`←back. Enqueue C: it attaches behind
B, giving front→`A B C`←back. Now dequeue three times. The first dequeue returns the front, **A**,
and advances the front to B, leaving `B C`. The second returns **B**, leaving `C`. The third
returns **C**, leaving the queue empty. The output sequence is **A, B, C** — the same order they
went in. (Had this been the same-end discipline, a stack, the three removals would have produced
C, B, A — arrival order reversed; the queue's FIFO rule is exactly what keeps it A, B, C.) None of
the three dequeues shifted any other value: each was a single O(1) splice at the front node the
queue already held, and the cost would have been identical with three million values in line, not
three.

**A worked instance — BFS rings.** Picture a start node S connected to A and B; A connected on to
C; B connected on to C as well. BFS begins by enqueuing S, so the frontier is `S`. Dequeue S,
look at its neighbours A and B, enqueue both: frontier `A B`. Dequeue A (it waited longer than B),
see its unvisited neighbour C, enqueue it: frontier `B C`. Dequeue B; its only neighbour C is
already seen, so nothing new is enqueued: frontier `C`. Dequeue C; it has no unvisited neighbours;
the queue empties and the search ends. The order nodes were *first reached* is S, then A and B,
then C — distance 0, then distance 1, then distance 2 — strictly by ring. Because S was reached at
distance 0 and C was first reached while expanding a distance-1 node, BFS knows C lies two edges
from S, and that is the shortest such count. The FIFO queue is what enforced "drain distance 1
before touching distance 2," and that is the whole reason the answer is a shortest path by edges.

## Prerequisites

- [[linked-list]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the Queue (FIFO) row
  (Python: `deque`; key ops: `append` / `popleft` O(1) both ends; reach for it when: BFS,
  level-order), read against the Dynamic array row (insert/del mid O(n)) for the front-shift
  contrast and the Stack (LIFO) row for the arrival-order contrast. Also the "Essential Python
  idioms" block (`q = deque(); q.append(x); q.popleft()  # FIFO queue, O(1) both ends`) and the
  "Problem signal → structure" panel ("Shortest path on unweighted graph or grid / by levels →
  queue + BFS").
