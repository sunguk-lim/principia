# Performer Attention

## Meaning

Performer approximates the softmax attention kernel using positive random features. It uses the same associative trick as other linear-attention methods, but tries to stay close to softmax similarity rather than choosing a wholly different one.

## Mechanism

Transform queries and keys into a fixed number of random features. Sum key-feature and value products first; each query then reads the accumulated summary. This avoids a square score matrix. More features cost more but can improve approximation. Causal decoding must update the summary only with past tokens.

## One example

Compare a Performer model with exact attention on a long document task. Vary feature count and inspect both task accuracy and actual memory/latency. On a short sequence, compare approximate and exact outputs to expose numerical or feature-map errors.

## Check your understanding

**Question:** Is Performer the same as Linformer? **Answer:** No. Performer approximates the softmax kernel with random features; Linformer compresses the key and value sequence axes with learned projections.
