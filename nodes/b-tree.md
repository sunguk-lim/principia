---
id: b-tree
title: B-Tree / B+-Tree
summary: A balanced search tree generalized from binary to high fan-out — each node holds dozens-to-hundreds of keys and is sized to one disk block, so the tree is only 3-4 levels deep and a lookup costs 3-4 disk reads instead of the ~20+ a binary search tree would; the B+-tree variant keeps all data in leaves linked in a chain so range scans walk the chain without re-descending.
type: concept
tags: [databases/storage]
prereqs: [binary-search-tree, page, block-layer]
sources: ["Comer 1979, \"The Ubiquitous B-Tree\", ACM Computing Surveys 11(2); PostgreSQL docs — Index Types / B-tree (https://www.postgresql.org/docs/current/indexes-types.html)"]
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# B-Tree / B+-Tree

## Summary

A **B-tree** is a [[binary-search-tree]] taken to its logical extreme for data that lives on disk. A binary search tree keeps ordered data fast to look up and update by branching: each node holds **one** key and has at most **two** children, and a lookup costs about `log2(n)` comparisons. That is the right cost model when the data is in memory and the expense is *comparisons*. But when the tree lives on **disk**, the expense is not comparisons — it is **disk reads**, and the [[block-layer]] makes one disk read enormously more costly than one comparison while delivering a whole fixed-size block ([[page]]) at a time. A B-tree answers that cost model by making each node **high fan-out**: instead of one key and two children, a node holds *dozens to hundreds* of keys and has that many children, and the node is sized to exactly **one [[page]]/disk block** so that one node = one disk read. Because each block read now discriminates among hundreds of keys rather than two, the tree is extremely **shallow** — height ≈ `log_fanout(n)`, typically **3–4 levels** for millions of keys, so a lookup is **3–4 disk reads** instead of the ~20+ a binary tree of the same size would need. The **B+-tree** refinement puts *all* the actual data in the **leaves**, uses internal nodes only as a routing index of separator keys, and **links the leaves in a sequential chain** — so a *range scan* ("all keys between X and Y") descends once to the start and then walks the leaf chain, without ever climbing back up. That is why B+-trees are the standard on-disk index in databases and filesystems.

## Grounded explanation

### Why a binary search tree is the wrong shape for disk

[[binary-search-tree]] already solves the in-memory problem: store ordered data as branching linked nodes — one key per node, two children, the BST property (everything left is smaller, everything right is larger) — and you get `O(log n)` lookup *and* `O(log n)` insertion/deletion, the splice-don't-shift win over a sorted array. The cost it counts is **comparisons**, and each step down the tree is one comparison that discards a whole branch.

The trouble is *where the tree lives*. When `n` is large the tree does not fit in RAM; its nodes live on disk, and you reach a node by reading it from storage. As [[block-layer]] establishes, a disk read is not like a memory read: it carries a **large fixed per-request cost** (the head seek on a spinning disk, the command round-trip on an SSD), and it transfers a **whole block at once** — the device's natural unit, the same fixed-size [[page]] the OS manages memory in (commonly 4 KB). The block layer's whole reason for queueing and merging is that the *number of requests* is what hurts.

Now count a binary search tree's behaviour under *that* cost model. Each node holds one key. To descend one level you must read the node — one disk request — and a single comparison decides whether you go left or right. A balanced binary tree over `n = 1,000,000` keys has height ≈ `log2(1,000,000) ≈ 20`. So a lookup is **~20 disk reads**, and *each read drags in a whole 4 KB block to extract a single key and then throw the other ~4088 bytes away.* Twenty seek-cost disk trips to find one record. The binary tree is profligate with exactly the resource that is scarce: it makes one expensive block fetch yield only **one bit** of routing information (left or right).

### The fix: make one block fetch decide among hundreds of keys

The insight is to **match the node to the cost unit**. Since the disk hands you a whole block anyway, fill that block with keys: store not one key per node but as many keys as fit in one [[page]]. A 4 KB block holding, say, 16-byte (key + child-pointer) entries fits on the order of **~250 keys** per node, hence ~250 children — the node's **fan-out** `b`. A node with `b` children and `b−1` separator keys partitions the keyspace into `b` ranges in a single block read, exactly as a binary node partitioned it into 2. So one disk fetch now buys `log2(b) ≈ 8` bits of routing instead of 1.

This is the **B-tree**: a balanced search tree where every node holds up to `b−1` ordered keys `k1 < k2 < … < k(b-1)` and up to `b` child pointers, with the BST property generalized — the subtree between `k_i` and `k_(i+1)` holds exactly the keys that fall in that interval. The whole node is laid out to occupy **one disk block / [[page]]**, so *reading a node is exactly one disk read*. The defining contrast with [[binary-search-tree]] is fan-out: **binary = 2 children, one key, count comparisons; B-tree = hundreds of children, hundreds of keys, count disk reads.**

The payoff is height. Height ≈ `log_b(n)`. For `n = 1,000,000` and `b ≈ 250`, that is `log_250(1,000,000) ≈ 2.5`, i.e. **3 levels**. Even a *billion* keys is `log_250(10^9) ≈ 3.7`, still **4 levels**. So a lookup touches 3–4 nodes = **3–4 disk reads**, against the binary tree's ~20 for a million and ~30 for a billion — a 5–8× reduction in the scarce resource, achieved purely by changing the tree's shape to fit the substrate. (Comparisons *inside* a node — a binary search across its few hundred keys — are free by comparison: they happen in RAM once the block is fetched.)

### Staying balanced: split on overflow

A B-tree must stay shallow as keys arrive, and like a balanced [[binary-search-tree]] it does this by local restructuring — but the rule is simpler than rotations. The invariant is that **every node stays at least half-full and at most full** (`b−1` keys), and **all leaves sit at the same depth** (this is what keeps the height uniformly `log_b(n)`). Insertion walks down to the correct leaf and adds the key there. If that overfills the node (a `b`-th key would make `b` keys), the node **splits**: its keys divide into two half-full nodes, and the **median key is pushed up** into the parent as a new separator. If pushing up overfills the parent, the parent splits too, and so on; if the split reaches the root, the root splits and a new root is created above it — **which is the only way a B-tree grows taller, and it grows from the top, so all leaves stay level.** Deletion is the mirror: a node that falls below half-full **borrows** a key from a sibling, or **merges** with one, pulling a separator back down. Keep this at altitude — the point is the *split-on-overflow / merge-on-underflow* idea that preserves "half-full, all leaves level," not the full case analysis.

### B+-tree: data in the leaves, leaves in a chain

The variant databases actually use is the **B+-tree**, which adds one decisive twist. In a plain B-tree, keys (and their associated data/records) can sit at *any* level, including internal nodes. In a B+-tree:

1. **All data lives in the leaves.** Every actual key-plus-record sits in a leaf node. Internal nodes hold **only separator keys** — they are a pure *routing index*, signposts that say "keys below this value go left." A separator key may be a *copy* of a key that also appears in a leaf; internal nodes carry no records, only routing.
2. **The leaves are linked in a sequential chain.** Each leaf has a pointer to the next leaf in key order, so the leaves form a sorted linked list spanning the whole keyspace.

Why this matters: it makes **range scans** cheap, which is the query databases run constantly ("all orders between two dates," "all rows where id BETWEEN 100 AND 200"). To scan a range, descend the index *once* to the leaf containing the low end of the range, then **walk the leaf chain** reading consecutive leaves until you pass the high end. You never climb back up into the internal nodes to find the next key — the chain hands them to you in order. In a plain BST or B-tree you would have to repeatedly compute the in-order successor, re-descending from higher nodes again and again; the leaf chain replaces all of that with a straight-line walk over already-sorted blocks. (As a bonus, because internal nodes carry no records, they pack *more* separator keys per block, raising fan-out and shaving height further.)

### Worked instance: a small B+-tree, one lookup, one range scan

Take **order 4**: each node holds up to **3 keys** and up to **4 children** (so a leaf holds up to 3 keys; an internal node up to 3 separators). Store these **12 keys**: `5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60`. A B+-tree over them, with **2 keys per leaf** (deliberately not packed full, so the structure genuinely branches rather than collapsing to one node):

```
                         Root  [ 35 ]
                        /            \
          Internal A [15 | 25]     Internal B [45 | 55]
           /     |      \            /      |      \
        L1      L2      L3         L4      L5      L6
       [5,10]→[15,20]→[25,30]→ [35,40]→[45,50]→[55,60]
        └──────── leaf chain, linked left-to-right ────────┘
```

Read the routing rule: at the **Root**, separator `35` means "keys `< 35` go left to Internal A, keys `≥ 35` go right to Internal B." At **Internal A**, separators `15, 25` split its three children: `<15` → L1, `[15,25)` → L2, `≥25` → L3. Note `35`, `15`, `25`, `45`, `55` appear as *separators above* and *also as real keys in the leaves* — internal nodes only route; the data is all in the leaves, which are chained `L1→L2→L3→L4→L5→L6`.

This tree is **3 levels** (root, internal, leaf), so it occupies 3 blocks on any root-to-leaf path. Assume each node is one [[page]], so **reading one node = one disk read** via the [[block-layer]].

**Point lookup — find key `40`.**

1. Read the **Root** block (disk read #1). Binary-search its keys in RAM: `40 ≥ 35`, so follow the right pointer to Internal B.
2. Read **Internal B** `[45 | 55]` (disk read #2). In RAM: `40 < 45`, so follow the leftmost pointer to leaf **L4**.
3. Read leaf **L4** `[35, 40]` (disk read #3). Scan it: `40` is present — found.

**Total: 3 disk reads.** Now contrast a [[binary-search-tree]] holding the *same* 12 keys, one key per node. Even perfectly balanced its height is `log2(12) ≈ 3.6`, i.e. 4 levels, so a lookup is up to **4 reads**, *each fetching a whole block to use a single key.* The gap is modest at `n = 12` but it is the *shape* that matters: scale to a million keys and the B+-tree stays at 3 reads while the binary tree climbs to ~20. The B+-tree spends each expensive block read to discriminate among 4 keys (here) or hundreds (in practice); the binary tree spends each one to discriminate among 2.

**Range scan — every key in `[20, 50]`.** This is where the leaf chain earns its place.

1. Descend *once* to the low end. Read Root (`20 < 35` → left), read Internal A (`20 ≥ 15` and `< 25` → middle child L2), read leaf **L2** `[15, 20]` — **3 disk reads** to arrive. Emit the keys in L2 that are `≥ 20`: that gives **`20`**.
2. Now **walk the leaf chain**, no re-descending. Follow L2's next-pointer to **L3** `[25, 30]` (read #4): both `25, 30` are `≤ 50`, emit them. Follow to **L4** `[35, 40]` (read #5): emit `35, 40`. Follow to **L5** `[45, 50]` (read #6): emit `45, 50`; the high bound `50` is reached.
3. Stop. Output, already in sorted order: **`20, 25, 30, 35, 40, 45, 50`.**

The scan cost is "one descent (3 reads) + one read per leaf in the range," a straight sequential walk over consecutive, already-sorted blocks. Crucially, after the initial descent it **never touched an internal node again** — the chain pointer supplied each next leaf directly. A plain [[binary-search-tree]] doing the same range query would, for each successive key, have to walk back up to a common ancestor and down again to find the in-order successor — re-reading internal nodes repeatedly. The leaf chain is exactly what removes that re-descent, and it is why the B+-tree is the on-disk index of choice for the range queries databases run all day.

## Prerequisites

- [[binary-search-tree]] — the B-tree is *this* structure generalized: a B-tree IS a balanced search tree, but with high fan-out (many keys/children per node) instead of binary (one key, two children). The BST property, the `O(log n)` height argument, the splice-don't-shift insertion, and the degenerate-chain failure mode are all the baseline this node departs from. The node is unintelligible without it — and only makes sense *as a contrast* to it.
- [[page]] — a B-tree node is sized to exactly one page (the fixed-size unit, ~4 KB), which is what makes "one node = one disk read" true and fixes the fan-out: how many keys fit in a page is the fan-out `b` that sets the height.
- [[block-layer]] — supplies the cost model that justifies the whole design: a disk trip is slow, has a large fixed per-request cost, and moves a whole block at a time. High fan-out exists precisely to make each expensive block read discriminate among many keys, minimizing the number of disk requests.

## Sources

- Comer, D. (1979). "The Ubiquitous B-Tree." *ACM Computing Surveys* 11(2): 121–137 — the canonical survey of the B-tree and its B+-tree variant, including the disk-I/O cost rationale for high fan-out and the leaf-linked range-scan structure.
- PostgreSQL documentation — Index Types (B-tree): https://www.postgresql.org/docs/current/indexes-types.html — a real-world B+-tree index used for equality and range queries, the default index in a production database.
