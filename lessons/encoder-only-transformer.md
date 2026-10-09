# Encoder-Only Transformer

## Meaning

An encoder-only Transformer builds representations for an input sequence while each token may use information on both sides. It is suited to tasks where the whole input is available.

## Mechanism

Use stacked self-attention and feed-forward blocks with position information, but without the original Transformer's separate decoder and cross-attention. A masked-token training objective can hide selected input tokens and ask the model to infer them from surrounding context. That is a training choice, not a requirement of every encoder-only architecture.

## One example

In “the bank flooded,” the word “flooded” can help the encoder represent “bank” as a riverbank. This right-context access is beneficial for understanding. The same access would leak a future target in ordinary next-token generation.

## Check your understanding

**Question:** Does encoder-only mean the model cannot produce any text? **Answer:** No. It can score or fill selected positions, but its native bidirectional architecture is not a left-to-right autoregressive generator.
