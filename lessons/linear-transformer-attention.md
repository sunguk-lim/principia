# Linear Transformer Attention

## Meaning

Linear Transformer attention replaces all-pairs attention scores with a factorized similarity. It can summarize past keys and values in a running state, then answer each new query from that state.

## Mechanism

Write similarity as a dot product between feature maps of the query and key. Matrix multiplication can be reordered: sum transformed key–value products once, then multiply by each transformed query. For causal decoding, update the summary only from visible past positions. The result avoids storing a square attention matrix when feature width is fixed.

The similarity is not automatically the same as softmax. Feature choice, normalization, and numerical stability affect quality. By contrast, FlashAttention tiles the same softmax operator to avoid storing the full score matrix; it does not generally remove quadratic pairwise arithmetic.

## One example

For N=4 positions, dense bidirectional attention considers 16 ordered pairs; N=8 gives 64. Tiling can avoid storing all 64 scores simultaneously without removing their contributions. A fixed-width factorized rule instead aggregates through a bounded-width state, trading a changed or approximated similarity for different sequence scaling. First compare dense and tiled versions of the same softmax operator for numerical agreement. Then separately compare the factorized operator for quality, sharp distant-token retrieval, memory, and end-to-end latency. Lower memory use, lower arithmetic and equivalent output are not interchangeable claims.

## Check your understanding

**Question:** Why does reordering help? **Answer:** It aggregates the keys and values once instead of recomputing every query–key pair.
