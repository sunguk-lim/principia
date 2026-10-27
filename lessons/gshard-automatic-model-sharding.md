# GShard Automatic Model Sharding

## Meaning

GShard is a model-scaling approach that couples conditional expert computation with compiler-supported tensor partitioning. Its distinctive contribution is not merely distributing experts: a model describes global operations and selected placement annotations, then a compiler constructs local computations and communication. This separates the model's mathematical structure from much of its distributed implementation.

## Mechanism

A [[computation-graph]] describes global tensor operations. Placement annotations mark tensors or dimensions as replicated or divided across devices. The [[spmd-tensor-partitioning]] transformation translates this annotated global program into a per-device executable while preserving the operation semantics, not changing the learning objective.

The paper uses single-program-multiple-data partitioning: devices run the same generated program on different tensor slices. When layouts disagree or an operation needs remote values, the compiler inserts data movement or combination. Its sparse transformer example alternates replicated non-expert work and partitioned expert work. [[expert-parallelism]] supplies the dispatch and return of routed tokens; GShard adds the broader annotation-and-compilation organization. Top-2 routing with finite expert capacity still needs load controls and overflow handling. Annotation does not make communication disappear or ensure that every tensor layout is efficient.

## Worked example

Consider a hypothetical layer with eight experts on four devices, two experts per device. A token on device 0 selects experts 1 and 6. Dispatch sends a copy to each owning device; two outputs must return and be combined with their gate weights. The global layer still describes selection and combination, while the generated distributed program realizes those transfers. If a following operation expects the token batch partitioned by its original owner, the layout transition must restore that organization. Counting only two expert evaluations misses these movement and layout costs.

## Check your understanding

Does knowing where expert weights live fully explain GShard? No. Its additional objective is expressing global computation and placement separately so compiler transformations generate local execution and required communication.
