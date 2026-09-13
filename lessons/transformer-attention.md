# Scaled dot-product attention

## Meaning

**Goal:** explain how a query selects a weighted combination of value vectors.

Each position has a query describing what it seeks. Keys provide matching information; values provide the information to combine. These vectors are learned representations, not literal database fields.

## Mechanism

Let $Q$ contain $n_q$ query rows, $K$ contain $n_k$ key rows, and $V$ contain $n_k$ value rows. Queries and keys have width $d_k$; values have width $d_v$.

$$
O=\mathrm{softmax}(QK^\top/\sqrt{d_k})V.
$$

Each [[vector-dot-product]] produces a query-key score. [[matrix-multiplication]] computes the whole $n_q\times n_k$ score table. Scaling moderates score growth with key dimension; row-wise [[softmax]] converts scores into weights. Multiplying by $V$ produces $n_q\times d_v$ output values.

## One example

Suppose one query assigns weights $[0.25,0.75]$ to value vectors $[2,0]$ and $[0,4]$. Its output is $[0.5,3]$. It combines information rather than copying the highest-scoring value alone.

## Check your understanding

Must the number of queries equal the number of keys?

**Answer:** no. Self-attention commonly uses equal counts; cross-attention can use different counts. Each key must still have a corresponding value. A mask can exclude forbidden positions before normalization, such as future tokens in causal attention; implementations must handle rows with no allowed keys separately.

Reference: [Attention Is All You Need](https://arxiv.org/abs/1706.03762).
