# Hardware-Group-Limited Expert Routing

## Meaning

Expert routing chooses transformations; expert placement determines where those transformations live. A hardware-group restriction couples the two: only experts in selected device or node groups are eligible for one token. Its objective is a communication boundary, not necessarily a reduction in every scoring operation.

## Mechanism

Use [[moe-routing]] to obtain affinities and associate experts with their actual hardware groups. Score or otherwise select a bounded number of groups, exclude experts outside them, then choose the permitted experts and combine their outputs under the model's rule. [[expert-parallelism]] supplies the dispatch and return path whose cross-group destinations are bounded. Logical groups help locality only when they correspond to deployment placement.

The DeepSeek-V3 report describes node-limited routing: choose nodes using sums of selected high expert affinities and restrict each token's destinations. That is not the same as hierarchical product gating, whose parent and child probabilities multiply, nor does it mean every group-limited model uses one universal group score. Changing placement or restrictions can change which learned experts a token reaches.

## One example

Suppose six experts live as pairs on nodes A, B and C. Their scores for one token are A:[.50,.10], B:[.30,.25], C:[.20,.15]. Use an invented rule selecting the node with greatest two-expert score sum, then choose two experts there. Node totals are .60, .55 and .35, so A wins and experts [.50,.10] run. Unrestricted top-two would choose .50 from A and .30 from B. The restricted token visits one node rather than two but gives up the .30 route. This example defines its own scoring convention; it is not an exact implementation of DeepSeek's full router.

## Check your understanding

Does a one-group limit prove lower end-to-end latency? No. It may worsen within-group skew, exclude useful experts or leave tiny expert batches. Profile routing, dispatch, local expert compute and combine under the real topology. Check model quality, destinations, network bytes and slowest-rank time. A training-time locality rule and a post-training serving retrofit are different interventions; a checkpoint is not guaranteed to tolerate arbitrary new group restrictions.

