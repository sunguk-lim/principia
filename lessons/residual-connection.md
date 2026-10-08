# Residual Connection

## Meaning

A residual block adds its input to a learned transformation: output equals input plus a correction. The skip route can carry information and gradient directly through a deep network.

## Mechanism

The transformation and input must have compatible shapes. In Transformers, attention and feed-forward sublayers each use residual paths; pre-normalization and post-normalization arrangements differ. The identity term helps optimization but does not by itself guarantee stable training.

## One example

If a block initially computes nearly zero, its residual output is nearly its input. A non-residual block would instead pass nearly zero forward. This makes it easier to preserve a useful representation while learning refinements.

## Check your understanding

**Question:** What must happen if the input and transformed output have different widths? **Answer:** Use a documented projection or another shape adjustment before adding them.
