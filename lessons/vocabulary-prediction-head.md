# Vocabulary Prediction Head

## Meaning

A vocabulary prediction head converts one contextual hidden state into a distribution over the next token. The hidden vector describes the current context; it is not already a vector of token probabilities. The head supplies a learned coordinate change into the vocabulary, followed by normalization.

## Mechanism

Let $d$ be hidden width and $v$ the number of vocabulary tokens. A hidden state $h$ is a column vector with $d$ entries. A learned matrix $W$ has shape $v\times d$, and an optional bias vector $b$ has $v$ entries. The head computes logits $z=Wh+b$. The matrix operation is a [[linear-transformation]]; adding a nonzero bias makes the complete map affine. [[softmax]] converts the $v$ logits to probabilities $p_i=\exp(z_i)/\sum_{j=1}^{v}\exp(z_j)$ for token index $i$.

The Transformer paper describes a learned linear transformation and softmax, with shared weights between embeddings and the pre-softmax projection in that model. Weight tying reuses parameter storage under compatible dimensions; it is not a requirement of every vocabulary head. The output projection and the attention block's output projection are different operations with different target coordinates.

## One example

For an invented two-dimensional state $h=[2,1]^\top$, use three vocabulary rows $[1,0]$, $[0,1]$ and $[1,-1]$, with zero bias. Their dot products give logits $[2,1,1]$. The exponential sum is $e^2+2e$, so probabilities are approximately $[0.576,0.212,0.212]$. The first token is most likely under this head, but it is not certain. Selecting the largest probability and sampling from the distribution are different downstream decisions.

The three-token vocabulary is an explanatory miniature. Real vocabulary size affects projection parameters and computation. Test dimensions, token-ID ordering, padding and special-token treatment, and the distribution's normalization. A normalized distribution is not proof of factual correctness, calibration or safe behavior; changing the vocabulary or candidate mask also changes the normalization problem.

## Check your understanding

Can you apply softmax directly to a hidden state and call the entries token probabilities? Only if those coordinates already are the intended vocabulary logits. In the ordinary head, the learned vocabulary projection is the essential missing step.
