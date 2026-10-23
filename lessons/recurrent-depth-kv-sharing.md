# Recurrent-Depth KV Sharing

## Meaning

A [[looped-transformer]] can apply the same attention parameters at several hidden-state refinement steps. Each step can still produce different keys and values. Recurrent-depth KV sharing explicitly bounds how many iteration-specific cache slots are retained. It is a cache policy, not an automatic consequence of tied weights.

## Mechanism

An ordinary [[kv-cache]] avoids recomputing historical attention keys and values during autoregressive generation. In a recurrent-depth model, identify not only token position and block layer but also the recurrence step that produced a cached representation. Equal projection weights applied to different hidden states need not yield equal keys or values.

The Huginn primary report describes a fixed iteration-cache budget: read and write slots using an iteration index modulo the budget. For a positive budget $B$ and zero-based iteration $i$, the slot is $i\bmod B$. Once the budget is exhausted, a later iteration overwrites an earlier slot. This reuses storage and can let a current iteration attend to representations from different refinement depths for past tokens. The model's exact read/write order and attention masks determine the computation.

## One example

With $B=3$, iterations $0,1,2$ write slots $0,1,2$. Iteration $3$ returns to slot $0$, replacing iteration $0$'s retained entry; iteration $4$ replaces slot $1$. Five logical iteration representations do not remain separately addressable. If one full per-iteration cache would occupy $M$ bytes at the given sequence length, storing all five costs about $5M$ while three equal-capacity slots cost about $3M$, excluding other allocations. Additional refinement still performs attention and projection work.

This is not exact memoization of an identical function input, and it does not imply caches from an ordinary untied model can be aliased safely. The primary report evaluates this sharing on its particular trained recurrent model. Treat broader quality preservation as a hypothesis. Compare unshared and bounded-cache outputs, task accuracy, long-range retrieval, memory, iteration count, context length, and prefill/decode latency. Include variable-depth tokens and partial batches; verify that inactive requests cannot read another request's state.

Memory savings do not establish lower end-to-end latency: more recurrent computation, cache writes, masking, or irregular execution can dominate. State the architecture and cache contract alongside any result rather than describing parameter sharing itself as a free cache reduction.

## Check your understanding

Do identical key-projection weights imply identical cached keys at different recurrence steps? No. Different hidden-state inputs generally produce different projections.
