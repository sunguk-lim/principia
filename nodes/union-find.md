---
id: union-find
title: Union-Find
summary: Union-Find (also called a disjoint-set structure, or DSU) keeps a collection of items split into separate groups, where every item belongs to exactly one group and the groups…
type: concept
tags: [algorithms]
prereqs: [arithmetic]
sources: ["etc/study-notes.html — Data structures cheat sheet (Union-Find / DSU)"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Union-Find

## Summary

Union-Find (also called a disjoint-set structure, or DSU) keeps a collection of items split into separate groups, where every item belongs to exactly one group and the groups never overlap. It answers two questions quickly: *which group is this item in?* and *please merge these two groups into one*. It does this by giving each group a single chosen member, called the group's **root**, that names the whole group — so two items are in the same group exactly when looking up their roots gives the same answer. With two small tricks (flattening lookup paths, and always hanging the smaller group under the larger one) each operation costs almost nothing, far cheaper than recomputing all the connections from scratch every time something changes.

## Grounded explanation

**The objects.** Suppose we have items numbered `0, 1, 2, …, n−1`. At any moment they are split into **groups** — a "group" being a set of items we currently treat as belonging together, with the rule that every item is in exactly one group and no two groups share an item. This split is called a **partition**. As the program runs we want to do two things over and over: **find** — given an item, identify which group it is in; and **union** — take two items and fuse their two groups into a single group.

**How the groups are stored.** We do not store each group as an explicit list. Instead we store one number per item, in an array called `parent`. The rule is: `parent[x]` is the item that `x` "points to". Following these pointers — go from `x` to `parent[x]`, then to `parent[parent[x]]`, and so on — must always lead, after finitely many steps, to one special item in each group that points to *itself*: an item `r` with `parent[r] = r`. That self-pointing item is the group's **root**. Because every item leads to exactly one root, the root acts as the group's name. This arrangement of "each item points to a parent, every chain ends at a root" is a **forest**: a set of separate upside-down trees, one tree per group, the root at the top.

**The two operations on this storage.** `find(x)` walks the parent pointers starting at `x` until it reaches the root (the item that points to itself) and returns that root. `union(a, b)` first computes `root_a = find(a)` and `root_b = find(b)`; if they are already equal, `a` and `b` are in the same group and there is nothing to do; otherwise we make one root point to the other — say `parent[root_a] = root_b` — which hangs `a`'s entire tree under `b`'s root, so the two trees become one tree, i.e. the two groups become one group.

**Why the root trick is the whole point.** The key insight is the test for "same group". Two items `x` and `y` are in the same group **if and only if** `find(x) == find(y)`. We never have to compare the group memberships directly; we just compare two root numbers. And a `union` is cheap because we do not relabel every member of a group — we only re-point one root at another, and *all* of that group's members instantly inherit the new root, because the next time we follow their chains the chains run a little further up to the new common root. This is why Union-Find beats the obvious alternative. The naive way to answer "are `x` and `y` connected, given a pile of connections that keeps growing?" is to re-scan the connections each time. Union-Find instead maintains the answer incrementally: each new connection is one `union`, each query is one `find`, and neither rescans anything.

**Why naive storage can get slow, and the first fix.** Nothing above prevents the trees from growing tall. If we keep doing `union` and always hang the result the same way, we can build a long chain like `0 → 1 → 2 → 3 → 4`, where `parent[0]=1`, `parent[1]=2`, and so on up to a root `4`. Then `find(0)` must take four steps up the chain. With `n` items a chain can be `n` long, so a single `find` can cost on the order of `n` steps — slow if we do many of them. The first fix is **path compression**: while `find(x)` is walking up to the root, it also *re-points the items it passes directly at the root* (or at their grandparent, which over repeated calls flattens the tree just as well). After the walk, those items sit one hop below the root, so the next `find` on any of them is nearly immediate. The walk we had to do anyway pays to flatten the tree for the future — that is why it is almost free.

**The second fix.** The other fix is **union by size** (the rank variant is the same idea by height): when fusing two trees, attach the root of the *smaller* tree under the root of the *larger* one, rather than choosing arbitrarily. To do this we keep a second array `size`, where `size[r]` for a root `r` counts how many items are in that tree; on a `union` we compare the two sizes (a comparison of two numbers), point the smaller root at the larger, and add the smaller size into the larger. Hanging the small tree under the big one keeps trees shallow, because an item's depth only grows when its whole tree is the smaller side of a merge, which cannot happen too often. **Why combine both fixes:** with path compression *and* union by size together, the amortized cost of each operation is nearly constant — formally proportional to the inverse Ackermann function `α(n)`, a quantity that grows so slowly it is below `5` for any `n` that could ever arise in practice. So `find` and `union` are, for all practical purposes, constant-time. (This near-constant cost is exactly what makes Union-Find the engine inside algorithms such as Kruskal's minimum-spanning-tree method, finding connected components of a graph, and cycle detection — but those are uses, not part of the structure itself.)

**Worked instance.** Take items `0,1,2,3,4,5`. Start with everyone alone, so `parent = [0,1,2,3,4,5]` — every item is its own root, six singleton groups.

- `union(0,1)`: `find(0)=0`, `find(1)=1`, different. By size both trees hold `1` item (a tie; attach the first under the second), so `parent[0]=1`. Now `parent = [1,1,2,3,4,5]`; sizes: tree rooted at `1` has `2`. Groups: `{0,1}, {2}, {3}, {4}, {5}`.
- `union(2,3)`: roots `2` and `3`, sizes `1` and `1`, set `parent[2]=3`. Now `parent = [1,1,3,3,4,5]`. Groups: `{0,1}, {2,3}, {4}, {5}`.
- `union(3,4)`: `find(3)=3` (size `2`), `find(4)=4` (size `1`); attach the smaller (`4`'s tree) under the larger (`3`'s tree): `parent[4]=3`. Now `parent = [1,1,3,3,3,5]`; tree at `3` has size `3`. Groups: `{0,1}, {2,3,4}, {5}`.

Check connectivity: `find(2)` reads `parent[2]=3`, then `parent[3]=3` → root `3`. `find(4)` reads `parent[4]=3`, then `parent[3]=3` → root `3`. Both return `3`, so `2` and `4` are in the same group — connected. By contrast `find(0)` gives `parent[0]=1`, `parent[1]=1` → root `1`, while `find(4)` gives root `3`; `1 ≠ 3`, so `0` and `4` are **not** connected.

Now `union(1,4)`: `find(1)=1` (tree `{0,1}`, size `2`), `find(4)=3` (tree `{2,3,4}`, size `3`). The smaller tree is `1`'s, so attach it under the larger root `3`: `parent[1]=3`. Now `parent = [1,3,3,3,3,5]`; tree at `3` has size `5`. Groups: `{0,1,2,3,4}, {5}`.

**Watching path compression flatten a chain.** Notice item `0` is now two hops from the root: `parent[0]=1`, `parent[1]=3`, `parent[3]=3` (root `3`) — a little chain `0 → 1 → 3`. Call `find(0)`. Without compression it walks `0 → 1 → 3` every time. *With* compression, as the walk passes `0` it re-points `0` at its grandparent: `parent[0]` becomes `3`. So after this single `find`, `parent = [3,3,3,3,3,5]` — items `0,1,2,4` now all point straight at root `3`, and every future `find` on any of them is one hop. The lookup we needed anyway did the flattening for free.

## Prerequisites

- [[arithmetic]]

## Sources

- `etc/study-notes.html` — "Data structures cheat sheet": Union-Find (DSU) row (`parent array`; `union`/`find ≈ O(α(n))`; connectivity, components, cycle detection) and the path-compression skeleton.
