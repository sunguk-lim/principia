# Linear Transformer Attention

## Meaning

Linear Transformer attention replaces all-pairs attention scores with a factorized similarity. It can summarize past keys and values in a running state, then answer each new query from that state.

## Mechanism

Write similarity as a dot product between feature maps of the query and key. Matrix multiplication can be reordered: sum transformed key–value products once, then multiply by each transformed query. For causal decoding, update the summary only from visible past positions. The result avoids storing a square attention matrix when feature width is fixed.

The similarity is not automatically the same as softmax. Feature choice, normalization, and numerical stability affect quality.

## One example

For a long autoregressive sequence, compare an optimized full-attention model with a model using the factorized rule. Measure whether memory and decoding latency improve without losing accuracy on tasks requiring a precise distant token.

## Check your understanding

**Question:** Why does reordering help? **Answer:** It aggregates the keys and values once instead of recomputing every query–key pair.
