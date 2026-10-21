# Transformer-XL Relative Attention

## Meaning

Transformer-XL's relative attention is a specific attention-score parameterization, not just a name for cached segments or any learned relative embedding. It replaces absolute-position interactions with content and relative-distance terms, including two trainable global biases. This lets an attention layer distinguish cached and current positions without restarting an absolute position table at every segment.

## Mechanism

[[transformer-attention]] supplies projected queries and keys and converts scores into normalized weights. [[positional-encoding]] supplies the reason order must enter those scores. Use column vectors and define the following symbols before forming one head's score.

| Symbol | Shape | Meaning |
|---|---|---|
| q_i, k_j | d-vector | projected content query and key |
| r_(i-j) | p-vector | fixed sinusoidal encoding of relative distance i−j |
| W_R | d×p matrix | learned projection of relative encodings |
| u, v | d-vectors | learned global content and position biases |
| s_ij | scalar | unscaled score from query position i to key j |

The score is

$$s_{ij}=q_i^T k_j+q_i^T W_R r_{i-j}+u^T k_j+v^T W_R r_{i-j}.$$

Equivalently, it is (q_i+u)^T k_j+(q_i+v)^T W_R r_(i-j). The first term addresses content; the second makes preferred distances content-dependent; the third supplies a shared content preference; the fourth supplies a shared distance preference. Apply the usual head-dimension scaling, causal mask and [[softmax]] afterward. The distance basis is fixed in this formulation; its projection and the biases are learned. A clipped learned relation table is a different design, not a requirement of Transformer-XL.

## Worked example

For a two-dimensional head, take q=(1,2), k=(2,1), u=(1,1), v=(2,1), and a projected relative vector W_R r=(1,3). The four terms are 4, 7, 3 and 5, respectively: the unscaled total is 19. Regrouping gives (2,3)·(2,1)+(3,3)·(1,3)=7+12=19. The scaled value is 19/√2 before masking and normalization. These are illustrative projected values, not a claim about a trained model's scores.

A cached token and a current token can have the same segment-local index yet different relative distances to the current query. Their relative terms differ accordingly. This avoids index-reset confusion but does not prove unlimited memory or correct long-range reasoning. Compare with a direct four-term implementation, check causal masks and memory offsets, and evaluate distance-dependent quality at matched resources.

## Check your understanding

**Question:** Is the sinusoidal relative basis itself a learned clipped lookup table? **Answer:** Not in this parameterization; distinguish the basis from its learned projection and global biases.
