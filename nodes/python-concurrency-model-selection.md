---
id: python-concurrency-model-selection
title: Python Concurrency Model Selection
summary: Python concurrency model selection matches I/O waits, CPU work, data sharing, and failure boundaries to threads, coroutines, or processes using measured end-to-end behavior.
type: concept
tags: [languages/python]
prereqs: [thread, coroutine, parallel-process, gil, measurement]
sources: [https://docs.python.org/3/library/asyncio.html, https://docs.python.org/3/library/threading.html, https://docs.python.org/3/library/multiprocessing.html]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Python Concurrency Model Selection

## Summary

Python offers multiple ways to overlap work, and none is the default answer to “make it faster.” **Concurrency model selection** begins by separating time spent waiting on external I/O from time spent executing Python code or native compute. It then chooses threads, async coroutines, or processes according to workload shape, state sharing, library support, and measured results.

## Grounded explanation

A [[thread]] is useful when several blocking calls can wait concurrently while sharing one process's memory. This often fits existing synchronous I/O libraries, but shared mutable state needs synchronization and a failure can affect the whole process. In a conventional GIL-enabled CPython build, the [[gil]] limits simultaneous execution of Python bytecode; it does not prevent threads from overlapping many I/O waits. Native extensions and free-threaded builds change the CPU story, so measure the actual interpreter and libraries.

A [[coroutine]] with `asyncio` yields cooperatively at awaited operations. Many I/O tasks can be managed with fewer OS threads, but one accidental blocking call stalls the event loop. Async is most attractive when the network/database libraries and the entire call path support it. It does not automatically parallelize CPU-bound Python loops.

A [[parallel-process]] gives CPU tasks separate interpreter state and can bypass the conventional GIL, at the cost of process startup, memory duplication, serialization or shared-memory coordination, and more complex failure handling. Small tasks may spend more time crossing process boundaries than computing. Threads or processes are not substitutes for vectorized/native operations that already release the GIL or use internal parallelism.

For an image-and-API pipeline, profile API wait, image decode, Python transforms, and serialization separately. Try a synchronous baseline, a bounded thread pool for blocking fetches, an async path if the client supports it, and processes only for a measured CPU bottleneck. Keep the same inputs and outputs; compare throughput, p95 latency, memory, error propagation, cancellation, and shutdown behavior using [[measurement]]. Limit concurrency so a faster client does not overload the downstream service.

## Prerequisites

- [[thread]]
- [[coroutine]]
- [[parallel-process]]
- [[gil]]
- [[measurement]]

## Sources

- [Python `asyncio` documentation](https://docs.python.org/3/library/asyncio.html): cooperative asynchronous I/O.
- [Python `threading` documentation](https://docs.python.org/3/library/threading.html): thread-based concurrency and its constraints.
- [Python `multiprocessing` documentation](https://docs.python.org/3/library/multiprocessing.html): process-based concurrency and GIL separation.
