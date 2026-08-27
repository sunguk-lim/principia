# Figure spec — `binary-search-tree` (Step 0)

> Derived from `nodes/binary-search-tree.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Visual teaching contract

**Audience:** A reader who understands binary search on arrays but not linked search trees.

**Single job:** Show that comparisons route a root-down walk and that insertion fills one empty link without moving existing keys.

**Visual thesis:** The left-smaller/right-larger invariant converts ordered lookup and update into short tree paths.

**Traced objects:** Lookup key `4` follows `5→3→4`; inserted key `6` follows `5→8→empty-left`.

**Subject visual vocabulary:** Linked nodes, parent-child edges, ordered branches, highlighted lookup path, dashed insertion path, and new-link node.

**Signature moment:** New node 6 attaches under 8 while 5, 3, 8, 1, and 4 remain stationary.

**Anti-template test:** The comparison labels, spatial left/right invariant, and empty-link splice specifically encode BST operations.

| channel | fact encoded | planned treatment |
|---|---|---|
| **Shape** | linked hierarchy | one readable three-level tree |
| **Space** | ordering invariant | smaller keys left, larger keys right |
| **Flow** | lookup versus insertion | directly labeled solid-gold and dashed-teal paths |
| **Change** | no-shift insertion | one teal new node at the empty link |
| **Order** | in-order traversal | final sorted strip |

**Progressive disclosure:** First view shows one ordered tree and two paths. Operation cards then spell out the comparisons, and the in-order strip confirms the invariant.

**Comprehension test:** The reader can reproduce both walks, identify why 6 becomes 8's left child, and explain why no array elements shift.

**First-view constraints:** 720 px canvas; essential labels at least 15 px; no animation, register table, or legend; every path directly labeled.

**Plan critique:** The former 940 px composition divided the canvas among a small tree, descend-loop register, legend, traversal strip, and cost footer. The mechanism became unreadable when scaled to a phone.

**Rendered critique:** Native-size inspection confirms a readable three-level tree, attached structural edges, and directly labeled lookup `5→3→4` and insertion `5→8→6` paths. The new-link state is distinct without a legend, operation cards fit, the in-order output is correct, and no text overlaps or clips.

**Reduced-motion result:** Static figure; no motion required.

## Genre & spine

Hierarchy with two flow overlays. The tree is the persistent spine; lookup and insertion reuse its existing links.

## Figure trigger

- **SHAPE:** parent-child hierarchy with ordered left/right subtrees.
- **FLOW:** comparisons choose one outgoing link per level.
- **CHANGE:** insertion materializes one formerly empty child.

## Dynamics

The final static state overlays the completed lookup and insertion traces. Solid versus dashed paths and direct operation labels distinguish them without animation.

## Worked instance

The base tree comes from `5,3,8,1,4`. Lookup 4 takes three comparisons. Insert 6 compares at 5 and 8, then fills 8's empty left link. Final in-order traversal is `[1,3,4,5,6,8]`.

## Caption/text

Keep the invariant above the tree and the height caveat below. Detailed balancing mechanics remain in prose.
