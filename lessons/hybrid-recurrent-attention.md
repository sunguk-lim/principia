# Hybrid Recurrent–Attention Decoder

## Meaning

A hybrid decoder uses both compressed recurrent memory and token-addressable full attention. The point is to reduce the number of layers carrying a growing [[kv-cache]] while retaining some ability to look back at individual positions.

## Mechanism

A [[gated-delta-network]] layer updates a bounded-size state as each token arrives. A full-attention layer appends keys and values to its [[kv-cache]]. If only one in four layers is full attention, fewer layers pay the growing-cache cost than an all-attention model. The total cache still grows with the length of the sequence; the architecture changes its coefficient, not that fact.

The official Qwen3.5-27B configuration is one concrete example of a three-linear, one-full pattern. It specifies layer types, not a guarantee of better speed or recall. The result also depends on state dimensions, context length, batch size, hardware kernels, and model training.

## One example

A conversation has a current delivery instruction and an exact order ID mentioned 20,000 tokens earlier. A recurrent layer can maintain a compressed representation of the evolving instruction; a full-attention layer retains a token-level route to the ID. Test both tasks explicitly because neither is guaranteed by the pattern alone.

## Check your understanding

**Question:** Does adding recurrent layers make the whole model's context memory constant? **Answer:** No. Its full-attention layers still keep KV entries for past tokens.
