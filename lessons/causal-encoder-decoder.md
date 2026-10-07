# Causal Encoder–Decoder for Autoregressive Serving

## Meaning

A causal encoder–decoder lets supplied context and generated tokens take different computational paths. Its purpose is to avoid spending full decoder compute on every input token when the workload contains far more input than output.

## Mechanism

The causal encoder reads earlier positions without peeking ahead. Its states form memory for a decoder that produces one token at a time. This differs from a conventional decoder-only stack where prompt and generated tokens pass through the same layers and keep layer-specific [[kv-cache]] entries. Shared memory may save work, but it can lose information that a later decoder layer would have used.

A model must be trained for the asymmetric path; changing an existing checkpoint's routing is not a bit-identical serving optimization. Compare quality at fixed hardware and prompt/output lengths before comparing prefill and decode speed. Ablate sparse indexing and cache compression separately.

## One example

An agent repeatedly receives long tool results and writes brief decisions. A shorter input path may help, but only if it preserves the evidence needed for those decisions.

## Check your understanding

**Question:** Why can a shorter prefill path hurt quality? **Answer:** It may compress away information the decoder needs later.
