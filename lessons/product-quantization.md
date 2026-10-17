# Product Quantization

## Meaning

**Goal:** explain how several small codebooks can represent many approximate vectors.

Product quantization splits a vector into coordinate groups and replaces each group with a representative subvector's index. Unlike coordinate-by-coordinate [[quantization]], each code describes several coordinates together. The vector is a one-dimensional [[tensor]], and the representatives are commonly learned using [[k-means-clustering]] separately in each group.

## Mechanism

With $M$ groups and $K$ representatives per group, a stored vector needs $M$ indices. Reconstruction joins the selected representatives in group order. There are $K^M$ possible reconstructed combinations, but only $MK$ representatives need to be stored. The exponential number of combinations comes from independently choosing one entry from each small codebook, not from storing all complete vectors.

Squared Euclidean distance decomposes into a sum over disjoint coordinate groups. For a query, precompute its distance to each representative. Distance to an encoded database vector then becomes one table lookup per group followed by a sum. The result is approximate because the database vector was replaced by representatives; neighbor order can change.

## One example

Split $[1,2,8,9]$ into two two-coordinate groups. Suppose its selected representatives are $[1,1]$ and $[8,10]$. The approximation is $[1,1,8,10]$, with squared error $2$. If each codebook has two entries, the vector uses two index bits, excluding shared codebooks and other metadata.

## Check your understanding

Does minimizing reconstruction error guarantee perfect nearest-neighbor search?

**Answer:** no. Small distance changes can reorder close neighbors. Measure recall against exact search, actual memory including codebooks, query latency, and sensitivity to new data. A squared-distance-trained codebook need not be equally good for another similarity metric.

Reference: [Faiss ProductQuantizer](https://faiss.ai/cpp_api/struct/structfaiss_1_1ProductQuantizer.html).
