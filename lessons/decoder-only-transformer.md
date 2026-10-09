# Decoder-Only Transformer

## Meaning

A decoder-only Transformer takes prompts and completions in one sequence. Its causal attention mask lets each position use its prefix, not future positions.

## Mechanism

Remove the separate source encoder and cross-attention from the original encoder–decoder design. Train on next-token prediction. During generation, produce one token at a time and keep prior key/value states in a KV cache so previous layers' work need not be entirely repeated.

## One example

Put an instruction and a document before a question in the same prompt. The next output token may attend to all earlier prompt tokens, but there is no separate document encoder. Longer prompts increase prefill work and cache occupancy.

## Check your understanding

**Question:** Why is a decoder-only model not automatically truthful? **Answer:** Its architecture enforces prefix visibility; it does not validate claims, sources, or instructions.
