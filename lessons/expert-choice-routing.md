# Expert-Choice MoE Routing

## Meaning

Token-choice routing asks which experts a token prefers. Expert choice reverses the selection axis: each expert chooses its highest-scoring tokens from a group. This balances the number of accepted assignments per expert when the group and capacities permit it, but does not fix how many experts process each token.

## Mechanism

Start with the token-to-expert affinity scores of [[mixture-of-experts]]. For each expert, rank the tokens in the available group and keep the highest-scoring c tokens, where c is the expert's capacity. Gather those representations, run that expert, and scatter weighted outputs back to the originating tokens. A token selected by several experts receives several contributions; an unselected token receives no contribution from this expert branch. A surrounding residual path, when present, is a separate model operation.

The Expert Choice paper defines capacity from token count, expert count and a factor controlling average expert assignments per token. Equal assignment counts need not mean equal elapsed time when experts, placement or kernels differ. Optional constraints on per-token coverage change the assignment problem and should not be assumed present in the simplest independent expert-selection rule.

## One example

Three tokens A, B and C have two expert-affinity columns. Expert one scores them [.9,.8,.1], and expert two scores them [.7,.6,.5]. With capacity two, each expert selects A and B. Expert loads are [2,2], but token coverage is [2,2,0]. The average is four assignments divided by three tokens, or 1.333; no individual token receives exactly that average. A policy requiring at least one expert per token must change this selection, not merely declare the loads balanced.

## Check your understanding

Does expert balance imply every token is processed equally? No. Inspect uncovered and multiply selected tokens as well as expert load. The primary paper's limitations explicitly note that its top-token selection uses past and future tokens, complicating autoregressive generation, and that very small serving batches need a different treatment. Do not apply a training-time token-group selector unchanged to a causal decoder or silently let one request influence another's computation. Compare quality, capacity, latency and coverage under an explicit grouping and causal contract.
