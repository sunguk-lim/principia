---
id: graph
title: Graph (Adjacency List)
summary: A graph is a set of vertices (also called nodes) — things — together with a set of edges — connections between pairs of those things.
type: concept
tags: [algorithms]
prereqs: [hash-map]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Graph (Adjacency List)

## Summary

A graph is a set of *vertices* (also called nodes) — things — together with a set
of *edges* — connections between pairs of those things. It is the natural model
whenever data is a web of relationships rather than a single line of items: a road
map (cities joined by roads), a social network (people joined by friendships), a
set of tasks joined by "must finish before" dependencies. To store a graph in a
program, the most common form is the *adjacency list*: a [[hash-map]] whose key is
a vertex and whose value is the list of that vertex's immediate neighbours (the
vertices one edge away). This costs space in proportion to the number of vertices
plus the number of edges — written `O(V + E)` — which for most real graphs, where
each vertex touches only a few others, is far less than storing a full table of
every possible vertex pair. From it you can list any vertex's neighbours instantly,
and walk the whole graph — visiting every vertex reachable from a start — in
`O(V + E)` time by either of the two standard traversals, breadth-first search
(BFS) or depth-first search (DFS).

## Grounded explanation

**The object: vertices and edges.** A graph is two sets. The first is a set of
*vertices* (singular *vertex*), the things being related — call them `A`, `B`, `C`,
`D`. The second is a set of *edges*, each edge being a pair of vertices that are
directly connected. Writing an edge `A–B` means "`A` and `B` are joined." Nothing
else is part of the definition: a graph is purely *which things exist* and *which
pairs are connected*. That spare definition is exactly why graphs are so general —
cities and roads, people and friendships, web pages and links, university courses
and their prerequisites all fit it, because all of them are "some things, and which
pairs of them are tied together."

**Two distinctions that the model must capture.** First, *directed vs.
undirected*. In an *undirected* graph an edge `A–B` is a two-way connection: if
`A` is joined to `B`, then `B` is joined to `A` (a friendship, a two-way road). In
a *directed* graph an edge has a direction, written `A→B` ("`A` points to `B`"),
and that does **not** imply `B→A` (a one-way street; "follows" on a social network,
which need not be returned; "task `A` must finish before task `B`"). Second,
*weighted vs. unweighted*. In an *unweighted* graph an edge is just present or
absent — all connections count the same. In a *weighted* graph each edge also
carries a number, its *weight*, meaning a cost, distance, or capacity (the length
of a road, the price of a flight). The plain graph here is undirected and
unweighted; the representation below extends to the other cases by storing a
direction or a number alongside each neighbour.

**A vertex's neighbours and its degree.** The vertices directly joined to a vertex
`v` by an edge are its *neighbours*. The count of them is `v`'s *degree*. In the
edge set `A–B`, `A–C`, `C–D`, vertex `A` has neighbours `B` and `C`, so its degree
is `2`; vertex `D` has the single neighbour `C`, degree `1`. Almost everything a
program asks of a graph reduces to one repeated question — *given a vertex, who are
its neighbours?* — so the way we store the graph should make that question cheap.

**The representation: an adjacency list built on a [[hash-map]].** The *adjacency
list* answers that question directly. It is a [[hash-map]] — a structure that, given
a key, fetches its associated value in constant average time, `O(1)` — keyed by
vertex, whose value for each vertex is the list of that vertex's neighbours. (In
the source's phrasing it is a "dict of lists," the Python built-in [[hash-map]]
holding a list per key.) To find every neighbour of `v`, you do a single
[[hash-map]] lookup on the key `v` — `O(1)` average — and read off the stored list;
walking that list to touch each neighbour then costs work proportional to `v`'s
degree, written `O(degree)`. This is the central payoff: the structure spends no
effort *searching* for `v`'s connections, because the [[hash-map]] *computes* where
`v`'s neighbour-list lives straight from `v` itself, just as it does for any key.

**Why `O(V + E)` space — the key accounting.** Let `V` be the number of vertices
and `E` the number of edges. The adjacency list stores one [[hash-map]] entry per
vertex (that is the `V` part) and, inside those entries, one list slot per edge-end.
Each undirected edge `A–B` contributes two slots — `B` appears in `A`'s list and
`A` appears in `B`'s list — so all the edges together occupy work proportional to
`E`. Add them: total space is `O(V + E)`. The contrast worth seeing is the
alternative representation, the *adjacency matrix*: a full `V` × `V` table with a
mark in row `i`, column `j` whenever vertex `i` connects to vertex `j`. That table
has `V × V` cells regardless of how many edges actually exist, i.e. `O(V²)` space.
For a *sparse* graph — one where each vertex has only a few neighbours, so `E` is
far smaller than `V²` (true of most real networks) — the adjacency list's `O(V + E)`
is dramatically smaller than the matrix's `O(V²)`: a million-vertex social graph
where each person has a few hundred friends needs a few hundred million list slots,
not the million-times-a-million cells the matrix would demand. The adjacency list
pays only for the edges that exist; the matrix pays for every pair that *could*
exist. (The matrix's one advantage — checking whether one specific pair `i,j` is
connected in `O(1)` — rarely outweighs that cost, which is why the adjacency list is
the default.)

**Walking the whole graph: the two traversals.** Storing the graph is half the
job; the other half is *visiting* vertices — starting at some vertex and reaching
every other vertex connected to it, doing something at each. The two standard ways
are *breadth-first search (BFS)* and *depth-first search (DFS)*. They differ only in
the order they visit and the bookkeeping they use.

BFS explores in rings of increasing distance from the start. It keeps a *queue* — a
waiting line where vertices leave in the same order they arrived (first in, first
out) — plus a record of which vertices have already been seen, so none is processed
twice. It starts by putting the start vertex in the queue and marking it seen. Then
it repeatedly takes the front vertex off the queue, looks up its neighbour-list in
the adjacency [[hash-map]], and for each neighbour not yet seen marks it seen and
adds it to the back of the queue. Because the queue serves vertices in arrival
order, every vertex one edge from the start is handled before any vertex two edges
away, and so on outward — BFS visits vertices in *level order*, by edge-count
distance. That ordering is what makes BFS find the *shortest path by number of
edges* in an unweighted graph: the first time it reaches a vertex is necessarily
along a path with the fewest edges.

DFS instead plunges as far as it can along one chain of edges before backing up. It
uses a *stack* — a pile where the most recently added vertex is the next one taken
(last in, first out) — or, equivalently, the call stack of a function that calls
itself (recursion). From a vertex it walks to an unseen neighbour, then *that*
vertex's unseen neighbour, deepening until it hits a vertex whose neighbours are all
already seen, then retreats to the last vertex that still had an unexplored
neighbour and continues. (The choice between BFS and DFS is just the choice of which
waiting structure — queue vs. stack — orders the pending vertices.)

**Why both run in `O(V + E)` time.** In either traversal the "seen" record ensures
each vertex is processed exactly once. Processing a vertex means doing constant work
for the vertex itself plus reading its neighbour-list — and the total length of all
the neighbour-lists across every vertex is proportional to `E` (each edge appears in
the lists at its two ends). So the visiting work sums to "once per vertex" plus
"once per edge": `O(V + E)`. Each vertex and each edge is touched a constant number
of times, no more — the same accounting that gave the storage its size now gives the
traversal its running time.

**Worked instance.** Take four vertices `A`, `B`, `C`, `D` and three undirected
edges `A–B`, `A–C`, `C–D`. Build the adjacency [[hash-map]] by adding each edge's
two ends to each other's list:

- `A–B`: put `B` in `A`'s list and `A` in `B`'s list.
- `A–C`: put `C` in `A`'s list and `A` in `C`'s list.
- `C–D`: put `D` in `C`'s list and `C` in `D`'s list.

The finished map is `{A: [B, C], B: [A], C: [A, D], D: [C]}`. Here `V = 4` and
`E = 3`, and the lists hold `2 + 1 + 2 + 1 = 6` slots — exactly `2E`, the two ends
of each of the three edges — confirming the `O(V + E)` count. To *enumerate `A`'s
neighbours*, do one [[hash-map]] lookup on key `A`, get the list `[B, C]`, and read
its two entries: work proportional to `A`'s degree `2`, i.e. `O(2)` — the map never
inspects `B`, `C`, or `D`'s entries to answer this.

Now run a BFS from `A`. Queue starts `[A]`, seen `= {A}`. Take `A` off the front;
its neighbour-list is `[B, C]`; neither is seen, so mark both seen and enqueue them
— queue `[B, C]`, seen `{A, B, C}`. Take `B`; its only neighbour `A` is already
seen, so nothing is added — queue `[C]`. Take `C`; its neighbours are `A` (seen) and
`D` (new), so mark `D` seen and enqueue it — queue `[D]`, seen `{A, B, C, D}`. Take
`D`; its only neighbour `C` is seen; nothing added — queue empty, traversal done.
The visit order was `A`, then `B` and `C`, then `D` — exactly level order by edge
distance: `A` is at distance `0`, `B` and `C` at distance `1` (one edge from `A`),
`D` at distance `2` (reached via `A→C→D`). Across the whole run each of the `4`
vertices was dequeued once and each of the `3` edges was examined from both ends,
matching the `O(V + E)` bound.

**Where this shows up.** The source lists the adjacency-list graph for
"relationships, paths, grids," with BFS/DFS at `O(V + E)`, and notes the build idiom
`adj = defaultdict(list); adj[u].append(v)` — a [[hash-map]] that hands back a fresh
empty list the first time a new vertex key is touched, so each edge is recorded by
appending a neighbour without first checking whether the key exists. Its
problem-signal is "shortest path on an unweighted graph or grid, by levels → queue +
BFS" — the level-order property derived above. A grid (a maze, a pixel image) is just
a graph in disguise: each cell is a vertex and each edge joins horizontally or
vertically adjacent cells, so the same adjacency-list traversals apply.

## Prerequisites

- [[hash-map]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the "Graph (adjacency
  list)" row (`dict of lists`, `BFS / DFS O(V+E)`, "relationships, paths, grids"),
  the queue/`deque` row ("BFS, level-order") and stack/`list` row ("DFS"), the
  "Essential Python idioms" block (`adj = defaultdict(list); adj[u].append(v)` —
  "graph / multimap"), and the "Problem signal → structure" panel ("Shortest path on
  unweighted graph or grid / by levels" → "queue + BFS").
