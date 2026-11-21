# HDBSCAN

## Meaning

HDBSCAN examines density connectivity at multiple scales. It can retain groups with different density levels instead of forcing all of them through one DBSCAN radius. It still makes modeling and parameter choices; hierarchy construction is not evidence that every returned group is meaningful.

## Mechanism

Use [[dbscan]] to understand core neighborhoods and noise. For a fixed neighbor-count parameter, let core(x) be x's distance to the specified ranked neighbor under the implementation's self-counting convention. Define mutual reachability between x and y as max(core(x),core(y),distance(x,y)). A sparse point's large core distance thus raises its connection cost even when it sits close to another observation.

Consider the complete weighted [[graph]] with these distances. A [[minimum-spanning-tree]] connects all points without cycles with minimum total edge weight. It preserves the threshold-connectivity hierarchy: remove large-weight edges to expose components at progressively denser scales. Condense the hierarchy with a minimum cluster size and choose clusters using a declared selection rule, such as excess of mass. Cluster selection and the hierarchy are distinct stages.

## One example

Suppose two invented points are .1 apart but have core distances .2 and 1.0. Their mutual-reachability distance is max(.2,1.0,.1)=1.0, not .1. The sparse point does not become a strong dense connection merely by being physically near one neighbor. A dense small group and a looser large group may appear on different branches; whether both survive depends on minimum size and selection policy.

## Boundaries and check your understanding

Check parameter sensitivity, hierarchy stability, selected groups and noise, not only the final group count. Different packages may count self differently in min_samples, so transfer values only after checking the convention. High-dimensional or badly scaled distances can undermine the representation before clustering begins. Hierarchy construction and neighbor search also have implementation-dependent resource costs. Compare with a radius sweep and labeled or domain-specific checks without asserting universal superiority on variable-density data.

**Check:** Does removing the global eps choice remove all hyperparameters? No. Neighbor count, minimum cluster size, metric and cluster-selection decisions remain.
