# Linformer Attention

## Meaning

Ordinary attention compares every query position with every key position. Linformer replaces the full key and value sequence axes with learned, shorter projections. It asks whether a compact representation retains enough information for the task.

## Mechanism

With `n` tokens and projected length `k`, the attention scores have shape `n × k` rather than `n × n`. If `k` is kept fixed while `n` grows, the attention portion scales linearly with `n` under fixed head width. This is an approximation: a small `k` can erase distinctions between positions.

## One example

A document classifier sees sequences of 4,000 tokens. Try several projected lengths, then compare task accuracy, memory, and latency with exact attention on the same hardware. A lower score-matrix size is useful only if the quality and realized performance trade-off is acceptable.

## Check your understanding

**Question:** Does linear scaling prove Linformer matches exact attention? **Answer:** No. The projected representation can lose task-relevant interactions; evaluate quality and system performance separately.
