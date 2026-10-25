# Text-Embedding API Contract

## Meaning

A text-embedding endpoint converts input text into numeric vectors. The useful contract includes input identity, encoder configuration and scoring compatibility, not merely a successful request or expected number of coordinates.

## Mechanism

Keep stable source IDs when batching inputs. Map each returned vector through its input index and verify count, dimension and finite values before indexing. A response received first need not represent the first submitted document. Retries must not duplicate or misassign rows.

Store the encoder revision, preprocessing, dimensions, normalization, metric and any query/document task settings with the corpus. Cosine compares vector directions. Dot product gives the same scores only when both vectors are unit-normalized. Neither score is inherently a probability that a document answers the question.

A new encoder can use a different geometry while returning the same shape. Re-embed the corpus or establish a documented compatible pair before changing the query side. Validate judged queries and hard negatives, not just array lengths.

## One example

Suppose two unit document vectors are (0.8,0.6) and (-0.8,0.6). Query (0.6,0.8) gives scores 0.96 and 0 by multiplying corresponding coordinates and summing. The first document wins. A replacement query encoder emitting (-0.8,0.6) instead gives -0.28 and 1 against the unchanged index: the second wins. Dimensions and norms remain valid, so shape checks cannot detect this mismatch. These vectors illustrate the contract; they are not measured representations of particular sentences.

## Check your understanding

**Question:** The replacement endpoint returns two vectors for two documents. Is the batch ready to store? **Answer:** Only after matching each vector to its input identity and validating the expected encoder/configuration and numeric shape. Then task evaluation must establish useful ranking. Correct transport is necessary but insufficient for semantic retrieval.
