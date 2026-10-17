# Cross-Attention

## Meaning

**Goal:** identify which sequence receives the output when attention reads a separate context.

Cross-attention uses queries from a target sequence and keys and values from a different context sequence. It applies [[transformer-attention]] with different input provenance. The defining change is directional information flow, not a new softmax formula. The two sequences can have different numbers of positions.

## Mechanism

Let there be $n$ target positions and $m$ context positions. Project target states into queries $Q$ of shape $n\times d$. Project context states into keys $K$ of shape $m\times d$ and values $V$ of shape $m\times v$. Attention scores have shape $n\times m$; multiplying normalized scores by $V$ produces $n\times v$ output states.

Each target position chooses a weighted combination of context values. The context stream does not automatically receive a reverse update. In encoder-decoder translation, decoder positions read encoded source positions. In image generation, image states can read text representations. A joint or additional reverse operation is required if both streams must update through that interaction.

## One example

There are two target states and three context states. Suppose attention weights are $[0.8,0.1,0.1]$ for the first target and $[0.1,0.2,0.7]$ for the second. There are two outputs, each a different weighted combination of the same three context values. There are not three outputs simply because three context values were read.

## Check your understanding

Does masking context padding guarantee less attention computation?

**Answer:** no. A dense implementation can still compute masked entries. Verify mask semantics, unequal lengths, all-masked behavior, quality, and actual memory/runtime costs. Projections of unchanged context may be cached, but caching benefits depend on workload and implementation.

Reference: [Attention Is All You Need](https://arxiv.org/html/1706.03762).
