# Minimum Spanning Tree

## Meaning

A minimum spanning tree connects every vertex of a connected, undirected weighted graph without cycles while minimizing total chosen edge weight. It is not the set of individually shortest paths from a source, and a low total does not mean every pair has a short tree path.

## Mechanism

A [[graph]] supplies vertices and connections. Attach a numeric weight to each undirected edge. A spanning tree connects all vertices with exactly one path between any pair and uses V-1 edges for V vertices. Minimize the sum of their weights using [[arithmetic]]. A disconnected graph has no spanning tree; the corresponding problem is a minimum spanning forest, one tree per component.

Kruskal's construction sorts edges from low to high weight, then adds an edge only when its endpoints are in different current connected components. Merging those components preserves the no-cycle condition. For a connected graph, stop after V-1 accepted edges. A cheapest edge crossing a split between components can be included in some optimum: if a proposed optimum omits it, exchanging it with an at-least-as-heavy crossing edge preserves connectivity without increasing cost. This exchange property explains why local choices can be safe here, not for arbitrary greedy problems.

## One example

A triangle has weights A-B=1, B-C=2 and A-C=4. Accept A-B and B-C, giving total weight 3. Adding A-C would create a cycle. Replacing B-C with A-C gives a valid tree but costs 5, so it is not minimal. These invented values also show why a tree can omit a real direct connection without disconnecting the graph.

## Threshold connectivity

For a threshold r, keep edges of weight at most r. An MST preserves the connected components of this thresholded full graph. If an MST path crossed a heavier edge while the full graph offered a path entirely at or below r, replacing that heavier edge across its cut would reduce the tree's total, contradicting minimality. This makes an MST useful for a connectivity hierarchy: sort or remove tree edges instead of retaining every pairwise edge.

## Boundaries and check your understanding

Tied weights can produce several equally optimal trees. Compare total weight and connectivity rather than demanding identical edge lists. Check disconnected inputs, duplicate edges, self loops, negative weights and ties. A naive dense distance graph can still require quadratic storage to construct; storing only the final tree does not erase upstream work.

**Check:** Does an MST minimize every pair's path length? No. It minimizes the sum of selected edge weights; shortest-path and spanning-tree objectives differ.
