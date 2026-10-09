# Causal Language-Model Training

## Meaning

A causal language model predicts the next token from the tokens before it. During training, the target for each position is the following token. It is not allowed to inspect that target in its input.

## Mechanism

Tokenize text, shift the target labels by one position, and apply a triangular attention mask. A row at position $t$ can read positions at or before $t$, never later positions. All rows can be computed together during teacher-forced training because the mask preserves this information rule. At generation time, the model must repeatedly sample one token, append it, and run another step. Check padding and document boundaries separately.

## One example

For “red fox runs,” the position after “red” predicts “fox.” If its attention mask accidentally includes “fox,” the apparent training loss improves by leakage rather than learning.

## Check your understanding

**Question:** Why does parallel training not imply parallel generation? **Answer:** Training knows the ground-truth prefix at every position; generation must first produce the preceding token.
