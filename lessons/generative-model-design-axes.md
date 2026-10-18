# Generative Model Design Axes

## Meaning

A network architecture describes how inputs and parameters produce predictions. A generative system additionally specifies a distribution over outputs, an objective for learning, and an algorithm for obtaining samples. Calling all four “the model” can hide which component changed.

## Mechanism

A [[neural-network]] may predict next-token scores or a noise-related quantity at a specified corruption level. [[conditional-probability]] determines how those predictions define an output distribution; a [[loss-function]] determines what training rewards. At generation time, greedy selection, sampling, or iterative transitions turn predictions into outputs. These axes are not arbitrary plug-compatible slots: masks, conditioning inputs, output heads, and objective targets must agree. Transformer blocks can parameterize autoregressive conditionals or diffusion predictions, but replacing one whole system with the other usually changes more than the blocks.

## One example

Keep a two-token vocabulary and fixed logits (2, 1). Greedy selection always chooses the first token. Sampling after normalization chooses it with probability exp(2)/(exp(2)+exp(1)), about 0.731, and the second with probability 0.269. The architecture and weights did not change; the generation policy did. Conversely, swapping convolutional blocks for attention under an otherwise compatible diffusion objective changes parameterization, not the corruption/reversal definition. To attribute gains, pin data and budgets, vary one compatible axis, and report unavoidable coupled changes, quality uncertainty, training cost, and inference cost separately.

## Check your understanding

Does a different sampled answer prove the architecture changed? No: decoding policy, inputs, runtime numerics, or randomness may change outputs with identical weights. Replacing a backbone and a training objective together is not a backbone-only ablation.
