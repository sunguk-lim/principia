# Transformer Encoder–Decoder

## Meaning

The original Transformer has an encoder that reads a source sequence and a decoder that writes a target sequence. It replaces recurrence with attention but still needs order information and separate rules for what each position may see.

## Mechanism

Encoder self-attention relates source tokens to other source tokens. Decoder masked self-attention relates a target prefix only to its past. Cross-attention lets each target position read the encoder's source representations. Feed-forward blocks, residual paths, [[layer-normalization]], and [[positional-encoding]] complete the stacked architecture. The mask permits parallel target training without revealing future target words; generation remains autoregressive.

Encoder-only and decoder-only models remove parts of this architecture for different tasks. They should not be mistaken for the original full source-to-target model or for a newer asymmetric causal encoder–decoder serving design.

## One example

For translation, the encoder reads “the cat sleeps”; the decoder predicts the first target word and then the next, attending to both the generated prefix and the source representation.

## Check your understanding

**Question:** What does decoder cross-attention read? **Answer:** Encoder outputs for the source sequence, using decoder states as queries.
