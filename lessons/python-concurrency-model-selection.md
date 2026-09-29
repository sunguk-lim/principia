# Python Concurrency Model Selection

## Meaning

[[python-concurrency-model-selection]] is the decision about how to overlap or parallelize work in a real program. The key diagnostic is whether the program mostly waits for I/O or spends time computing. “Concurrency” alone does not imply a speedup, and no Python mechanism wins for every workload.

## Mechanism

A [[thread]] can overlap blocking file or network operations while sharing memory with other threads. That makes it convenient with synchronous libraries, but shared state and failures need care. In conventional CPython, the [[gil]] limits simultaneous Python-bytecode execution; I/O waits still allow another thread to run. A [[coroutine]] using `asyncio` cooperatively yields at `await`, allowing many I/O operations on an event loop. It works best when the whole call path is async; a blocking function can stall everyone.

A [[parallel-process]] has independent interpreter state and can run CPU-bound Python work on multiple cores. It pays for startup, serialization, copies or shared-memory coordination, and recovery. Native libraries may already release the GIL or parallelize internally, so measure before adding processes. Free-threaded interpreter builds also change some assumptions; use the actual runtime as the test environment.

## One example

A service downloads files and then computes a costly Python feature for each file. A bounded thread pool might improve download overlap. Processes might improve the feature stage, but only if each feature task is large enough to exceed transfer overhead. Profile both stages, test output equivalence, and compare memory, tail latency, throughput, cancellation, and failures against a synchronous baseline.

## Check your understanding

**Question:** Why might `asyncio` fail to improve a CPU-heavy loop? **Answer:** Coroutines yield at awaits. A loop that never awaits occupies the event loop; CPU parallelism needs a different mechanism or native implementation.
