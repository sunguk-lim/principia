# Relative-Position Shift

## Meaning

A relative-position shift aligns an attention matrix's distance-indexed columns with its ordinary key-indexed columns. It changes where already computed scores are placed, not the mathematical attention rule. The useful invariant is that every valid output entry equals the direct score for that query–key distance.

## Mechanism

In [[transformer-xl-relative-attention]], define g_i=q_i+v and z_d=W_R r_d. The positional contribution is g_i^T z_(i-j). Many token pairs share a distance, so project each distinct r_d once. A matrix product then computes each query against the projected distance table; its columns still refer to distances, not key positions.

Let L be current-segment length, M retained-memory length, and K=M+L the combined key length. Current query row i, with 0≤i<L, occupies combined position M+i. Key column j has distance d=M+i−j. If the table stores distances in descending order K−1,...,0, its column index is c=K−1−d=L−1−i+j. Therefore the desired output selects row i, column c, for each causally allowed j≤M+i. A shift or padding/reshape routine implements this alignment. Future-key entries remain masked; reindexing alone is not causality.

## Worked example

Choose L=2, M=1 and K=3. The distance table columns are [2,1,0]. For query row i=0, allowed keys j=0,1 need distances [1,0], so select columns [1,2]. For row i=1, keys j=0,1,2 need distances [2,1,0], so select [0,1,2].

If the two pre-alignment score rows are [10,20,30] and [40,50,60], the valid output is [20,30,masked] and [40,50,60]. The number 10 is not needed for any allowed pair in the first row. A reshape implementation may put an arbitrary value into its future-key slot; the causal mask must remove it before [[softmax]].

Projecting K relative vectors costs O(Kpd) rather than O(LKpd) if projection were redundantly repeated for each pair, with input width p and head width d. Query–distance products still cost O(LKd), and the attention score array remains O(LK). This is reuse of projection work, not linear-time attention. Test direct-versus-shift equality for multiple memory/segment lengths, singleton boundaries, masks, batches and heads; physical copies versus views depend on layout and implementation.

## Check your understanding

**Question:** Does the relative shift make the attention matrix linear in sequence length? **Answer:** No. It removes redundant relative-vector projection, while pairwise scores and masking remain.
