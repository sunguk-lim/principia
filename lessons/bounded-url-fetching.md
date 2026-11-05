# Bounded URL Fetching

## Meaning

A fetcher can contact a permitted destination and still exhaust its own resources. Bounded fetching defines the maximum work accepted from one request and from concurrent requests. Destination authorization answers where a request may go; resource budgets answer how much work it may consume.

## Mechanism

Start with [[http]] limits on connection establishment, pool wait, response progress, redirect count and total elapsed time. A per-chunk read timeout is not an end-to-end deadline: a peer sending a small chunk just before each timeout can keep a transfer alive. HTTPX documents these timeout categories separately; an application must deliberately enforce its broader budget.

Read responses incrementally and stop before the byte budget is exceeded. Do not trust a declared Content-Length as the only check: the header may be absent or inaccurate, and compressed data can expand after transfer. Bound both transferred and decoded bytes, then apply limits to parsing depth, document expansion and extraction work. Avoid first buffering the entire response and only afterward truncating the returned text.

Per-request limits also compose. Bound active fetches, queued requests and retries, and propagate cancellation into the stream and parser so abandoned work releases resources. A large number of individually legal requests can exceed aggregate memory or connection capacity. Use [[measurement]] to observe peaks and rejection behavior, not only average request time.

## One example

An invented service allows eight simultaneous responses and at most 2 MiB of decoded content each. The accepted content buffers alone can approach 16 MiB, before compressed buffers, parser state and runtime overhead. A 20-second read-inactivity timeout does not cap a response that emits a byte every 19 seconds; a separate total deadline is needed. The numbers illustrate separate dimensions, not recommended production defaults.

## Check your understanding

Does limiting returned summary length bound download memory? No. The limit must operate while receiving and decoding, before unbounded buffering. Test slow chunks, oversized streams, compression expansion, redirect loops and cancellation using isolated fixtures; verify early stop, released resources and useful explicit failure status.
