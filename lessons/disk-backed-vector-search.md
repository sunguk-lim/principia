# Disk-Backed Vector Search

## Meaning

Disk-backed vector search places parts of the search representation on slower storage and controls candidate expansion and caching to bound memory without hiding IO cost.

## Mechanism

The mechanisms in [[vector-ann-index-families]] select a small candidate set or score compact codes before visiting expensive representations. A disk-oriented design chooses which graph links, vectors, codes and navigation data remain resident and which are read on demand. Layout should make a useful expansion require few storage reads. Batching independent candidate reads can overlap latency, while every next hop that depends on a prior result remains on a sequential path.

The [[page-cache]] can make repeated file reads appear memory-fast until the working set exceeds resident capacity. An application may also cache hot navigation data explicitly. These are real resource choices: cache size belongs in the memory budget, and popular-query benchmarks can conceal cold behavior. Compression can reduce reads but changes approximate ranking and may require fetching original vectors for final scores.

DiskANN provides a concrete graph-search implementation family with pluggable storage providers and choices of memory tiers. Its current repository includes in-memory as well as disk providers. Therefore neither its name nor a package import proves that a particular deployment is actually disk-backed, durable or faster than another index.

## One example

Imagine ten million 128-coordinate float32 vectors. Their raw coordinate payload is 10,000,000×128×4=5.12 billion bytes. A hypothetical 16-byte code per vector uses 160 million bytes, excluding graph links, IDs and metadata. Keeping those codes in RAM while reading original vectors only for 100 shortlisted candidates requests 51,200 payload bytes per query. It does not imply one 51,200-byte sequential read: the candidates may occupy scattered storage pages and each miss can add latency. A warmed cache can remove some reads; a larger candidate budget can improve recall while increasing IO.

## Validation and check

Measure exact-reference recall, p50 and tail latency, throughput, storage bytes read and peak RAM with stated hardware and concurrency. Compare cold, warm and deliberately memory-limited runs; include cache churn, updates, deletions and restrictive filters. A good mean on repeated queries does not predict an unseen-query tail. Does storing original vectors on disk reduce total storage to just the compact code payload? No. The originals remain a separate storage term and become an IO term when fetched.
