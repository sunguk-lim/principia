# Model Weight Streaming

## Meaning

An allocated accelerator is not ready to serve until the correct model weights have been read and placed. Model weight streaming exposes tensors progressively and overlaps storage activity with transfer rather than requiring a completely serialized load pipeline.

## Mechanism

Storage reads, decoding or metadata handling, host buffers, and device transfers form a pipeline. [[python-concurrency-model-selection]] explains why several outstanding I/O operations can hide waiting, while [[gpu-data-flow]] provides the transfer boundary. Bounded buffers keep concurrency from exhausting host RAM or amplifying storage contention. The slowest sustained stage limits steady-state throughput; the first and last chunks add pipeline fill/drain time. Streaming tensors is not automatically a direct storage-to-device path, zero-copy transfer, or on-demand layer execution. The model may still require all weights and runtime initialization before its first successful request.

## One example

A model has four equal chunks. Suppose each read takes two seconds and each transfer one second, with separate resources and sufficient bandwidth. A serialized load takes 4×(2+1)=12 seconds. With one read overlapping one transfer, the first chunk reads during seconds 0–2 and transfers during 2–3 while the next chunk reads during 2–4. The final read ends at second eight and its transfer at nine: idealized loading is nine seconds, not four or six. Shared network contention or transfer serialization may erase the gain. Measure cold and warm allocation-to-ready time, first inference, concurrent replica starts, host/device memory peaks, bytes transferred, and weight integrity. Compare local caching and prewarming without assuming published speedups apply to another store or device.

## Check your understanding

Can increasing reader threads improve loading forever? No: bandwidth, request throttling, buffer memory, and transfer throughput eventually dominate.
