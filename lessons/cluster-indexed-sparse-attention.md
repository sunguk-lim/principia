# Cluster-Indexed Sparse Attention

## Meaning

Content-grouped attention selection searches representatives of similar key vectors rather than scoring every key independently. Selected groups expand into token positions; ordinary attention then runs on those keys and values. Exact computation on the selected subset does not make it equivalent to full-context attention.

## Mechanism

[[hierarchical-sparse-attention-index]] separates candidate selection from value access. [[vector-cluster-representative]] explains how a summary vector supplies a coarse group score without preserving every member score. The grouping algorithm is a separate choice. The LSA primary paper uses normalized index keys, pooled nearby keys, bounded bottom-up grouping within completed blocks and a cache of group representatives plus position lists. Its grouping algorithm is not K-means. Learned projections can make indexing space differ from the full attention-key space.

A flat query scores every representative. Fixed-size compression reduces constants but still leaves representative count growing with context. A tree can search a bounded beam of groups at each of several levels; its work and recall depend on branching, depth and search width. Expanding selected groups produces long-range keys, with causal filtering, local-window and sink retention applied separately. Original KV storage can still grow with context.

## One example

Suppose eight keys are grouped into four two-key buckets. A query scores four representatives and selects two buckets, expanding to four keys for attention. It avoided scoring all eight original keys in the index space, but paid grouping and expansion work. If the one relevant key belongs to an unselected bucket, exact attention over the four survivors cannot recover it. Doubling context with the same bucket size doubles the flat representative scan; compression alone did not change that asymptotic growth.

## Check your understanding

Does one layer’s large prefill speedup establish the same end-to-end improvement? No. Separate selector construction/search, gathering, attention, other layers and service overhead. Check causal masking, retrieval recall, shifted contexts, task accuracy and storage. LSA’s reported ratios are author experiments at specified models, lengths and devices, not independently reproduced performance here.
