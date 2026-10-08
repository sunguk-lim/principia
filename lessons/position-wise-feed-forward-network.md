# Position-Wise Feed-Forward Network

## Meaning

A Transformer FFN transforms each token state with the same learned parameters, independently at each position. Attention mixes information across positions; the FFN mixes feature channels within one position.

## Mechanism

The original FFN expands the representation, applies a nonlinearity, and projects back to model width. It is usually wrapped by a residual path. Later gated variants change the internal formula, not the basic token-versus-channel distinction.

## One example

Given two different token states, the same FFN weights may produce different outputs. But changing one token cannot directly alter the other token through the FFN alone; an attention layer provides that cross-token path.

## Check your understanding

**Question:** If a model removes attention but retains FFNs, can one token read another? **Answer:** Not through those position-wise FFNs alone.
