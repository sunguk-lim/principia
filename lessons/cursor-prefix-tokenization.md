# Cursor-Prefix Tokenization

## Meaning

A code-completion system receives whatever appears before the cursor, even if the last identifier or line is unfinished. [[cursor-prefix-tokenization]] asks whether the tokenizer and model can continue from those arbitrary prefixes. A tokenizer can compress completed files well yet make this interaction worse.

## Mechanism

Encoding `import num` is not necessarily the first part of encoding `import numpy`. Additional characters can create a different [[byte-pair-encoding-tokenization]] merge or word-piece match. Therefore the terminal tokens seen by the model at a cursor may be uncommon in full-file training. This is a distribution question to measure, not an automatic failure.

Build an evaluation set by cutting real files at sampled character offsets: inside names, just after indentation, before newline, and at ordinary statement boundaries. Keep training data, model capacity, and compute comparable. Record exact-match and edit quality, syntax, accepted suggestions, latency, and line-stop correctness. A per-token loss number changes meaning with the vocabulary; divide total negative log probability by a common byte count when comparing models.

One mitigation, token healing, constrains initial generation to account for the already typed suffix. It may help, but adds alignment logic and runtime cost. Another is training on random prefixes. Stopping at a line is also an application contract: a token that contains newline plus more text cannot simply be assumed to stop at the newline cleanly.

## One example

A user pauses after `user_na`. The model must suggest the rest without duplicating the typed bytes. Test that exact cursor state, not only a benchmark on the finished `user_name` file.

## Check your understanding

**Question:** What is the evaluation unit? **Answer:** A source-text cursor offset. Token-boundary-only tests exclude the hard cases this concept addresses.
