# RAG Latency Budget

## Meaning

A RAG latency budget attributes delay to the path a request actually follows. Time to first usable output and time to full completion are different objectives. Neither retrieval nor prompt processing is automatically the bottleneck for every request.

## Mechanism

A retrieve-once request can wait for capacity, encode a query, search, rerank evidence, assemble context, process that context in model prefill, then decode an answer. A controller can add more retrieval and model rounds. Instrument the request as a root span and its operations as child spans. Keep timestamps for first and final output, and account for queueing, failures and retries.

Only sequential intervals add directly. If two searches start together and both are needed, the elapsed search interval is their maximum, not their sum. A parent span already contains its child work. Adding all span durations therefore measures accumulated operation time, not necessarily user-visible elapsed time.

## One example

Suppose queueing is 20 ms and query encoding is 10 ms. Concurrent searches take 30 and 50 ms, followed by 40 ms reranking, 10 ms context assembly and 120 ms until first output. The request takes 20+10+50+40+10+120=250 ms to first output. Another 600 ms of decoding makes completion 850 ms. Removing search entirely saves at most the observed 50 ms in this example; it does not remove the 600 ms response tail. These are hypothetical timings with unchanged answer quality.

## Check your understanding

**Question:** Can the p95 of each stage be added to obtain the request p95? **Answer:** Not generally. Slow events can occur on different requests, and some stages overlap. Compute percentiles from complete request observations, then use the stage traces to explain them. Evaluate matched task/evidence conditions so deleting necessary context is not mislabeled as an equivalent speedup.
