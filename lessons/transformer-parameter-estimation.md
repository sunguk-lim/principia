# Transformer Parameter Estimation

## Meaning

A parameter estimate counts stored trainable tensor entries. Architecture shapes and weight sharing determine the answer; model size cannot be read from layer count alone.

## Mechanism

For width $d$, each of Q, K, V, and output projections is approximately $d^2$ weights. Two feed-forward matrices of dimensions $d\times f$ and $f\times d$ add $2df$. Multiply this per-block count by the number of matching blocks, then add embeddings, normalization, biases, and an output head as appropriate. Tied input/output embeddings count once. Multiple attention heads partition width; they do not multiply the count a second time.

## One example

With $d=1024$ and $f=4096$, the leading attention and feed-forward weights per block are about $4.19$ million and $8.39$ million. Actual implementations can differ because of gated MLPs or grouped attention.

## Check your understanding

**Question:** Why can a model have many parameters but relatively few active weights per token? **Answer:** A mixture-of-experts model stores several experts while routing each token to only a subset.
