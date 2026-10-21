# Attention with Linear Biases

## Meaning

Attention with Linear Biases (ALiBi) encodes order by adding a distance-dependent bias to attention scores. In its causal language-model form, farther past keys receive larger negative penalties. Heads use different fixed slopes, creating different strengths of recency preference without learning a positional embedding table.

## Mechanism

[[transformer-attention]] computes content scores; [[positional-encoding]] explains why content alone does not specify token order. Let i be query position, j≤i a permitted key position, h the head index, d the head width, and m_h>0 that head's fixed slope. For content vectors q_i and k_j, a common notation for the logit is

$$s_{ij}^{(h)}=q_i^T k_j/\sqrt d-m_h(i-j).$$

Apply the causal mask to future positions and then [[softmax]] over keys. The slope schedule is an initialization rule from the implementation, not a learned parameter or an arbitrary universal formula. No positional embedding table must be extended merely to compute the bias at a new distance; nevertheless, usable long-context accuracy still requires empirical evaluation.

The penalty does not ban distant evidence. A sufficiently larger content score can overcome it, and different slopes change how strong that content evidence must be. Thus a recency preference is not a hard sliding window or a proof that long-range dependencies cannot be represented.

## Worked example

At query i=4, consider keys j=3 and j=0 with scaled content scores 1 and 2. A slope m=0.5 produces logits 1−0.5×1=0.5 and 2−0.5×4=0. Despite the distant key's stronger content score, the nearer key receives probability exp(0.5)/(exp(0.5)+1)≈0.622 among these two keys.

For a second head with slope 0.1, the same content scores become 0.9 and 1.6; now the distant key receives exp(1.6)/(exp(0.9)+exp(1.6))≈0.668. This is an illustrative two-key calculation, not a measured model result. It shows why different slopes matter rather than assuming every head has the same effective range.

Validate score signs, head slope assignment, causal masks and cached-decoding offsets. Compare perplexity and evidence retrieval at increasing lengths, with matched training budget, model and attention layout. Being able to evaluate a distance formula beyond training length is not the same as retaining task accuracy there, and published benchmark gains are workload-specific.

## Check your understanding

**Question:** Does ALiBi remove content from attention? **Answer:** No. It adds a distance bias to the content score; content can still dominate.
