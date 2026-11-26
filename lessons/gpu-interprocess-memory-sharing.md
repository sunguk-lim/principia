# GPU Interprocess Memory Sharing

## Meaning

GPU interprocess sharing exposes one allocation to another process through an exported handle. It is not sending the producer's raw pointer and hoping that address works elsewhere. Separate processes can map the same storage at different local addresses.

## Mechanism

The producer allocates supported device memory, exports a handle and communicates it with layout metadata. The consumer imports the handle and obtains its own valid mapping. A data message can therefore remain small even when the backing tensor is large.

Three questions remain separate: which storage is mapped, when its contents are ready, and how long it stays alive. GPU operations are asynchronous. A received handle does not establish completion of the producer's write. Use the runtime's supported completion ordering, prevent conflicting writes, and keep the backing allocation alive until consumers finish. The consumer closes its imported view before the producer reclaims storage.

CUDA documents handle export, import and close operations. PyTorch's sharing contract also requires the producer to remain alive while the consumer retains the CUDA tensor and specifies compatible process start methods. Another allocator or platform may have different restrictions. Abnormal exits can leave cleanup work; process separation is not a lifetime protocol.

## One example

A producer owns 16 MiB divided into four 4 MiB blocks. A consumer imports its handle, waits for the completed write and reads block 3. The two views refer to the same underlying 4 MiB region. After reading, the consumer acknowledges completion and closes its view; only then may the producer reclaim the buffer. Sending the handle and immediately freeing the buffer is incorrect.

## Check your understanding

Does this eliminate every cache transfer? No. A cache service may share access to device buffers while still copying data between GPU and host tiers. Cross-device access also needs compatible runtime and topology support. Verify actual transfers, ordering, lifetime and outputs against an explicit-copy baseline rather than interpreting “shared” as “free.”
