# Query-Key Normalization

## Meaning

**Goal:** explain why normalizing projected queries and keys can control attention-logit growth.

Very large attention logits can produce nearly one-hot weights and contribute to unstable training. The usual square-root-of-width scaling does not directly constrain learned vector magnitudes. Query-key normalization changes queries and keys before their dot products, rather than merely normalizing the input before projection.

## Mechanism

In the ViT-22B formulation, project states $X$ and apply [[layer-normalization]] to obtain $Q=\operatorname{LN}(XW_Q)$ and $K=\operatorname{LN}(XW_K)$. Use these in [[transformer-attention]]. The normalization axis, learned gain and offset, and numerical stabilizer belong to the specification. Values are not automatically normalized by this rule.

Centering removes a common coordinate offset and rescaling controls spread. It reduces one way for projected vector magnitudes to drive uncontrolled score growth. The learned parameters and other transformations still affect scores; this does not impose a universal bound or make all attention weights uniform.

## One example

Ignoring epsilon, with unit gain and zero offset, vector $[10,20]$ normalizes to $[-1,1]$. Multiplying the original vector by ten produces the same result. A score cannot grow tenfold solely from that positive rescaling of this query direction. Changing the key or learned gains can still change the score.

## Check your understanding

Are two implementations with an option named `qk_norm` necessarily equivalent?

**Answer:** no. They may normalize different axes, use different normalizers, or order normalization differently around position transformations. Specify the variant, inspect maximum logits and attention concentration, and compare matched training runs. Peaky attention is not inherently a failure; the concern is uncontrolled instability. This mechanism is also distinct from calibration of a classifier's correctness scores.

Reference: [Scaling Vision Transformers to 22 Billion Parameters](https://arxiv.org/html/2302.05442).
