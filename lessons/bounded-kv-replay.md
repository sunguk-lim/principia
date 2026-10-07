# Bounded KV Replay

## Meaning

Bounded KV replay saves persistent memory by rebuilding a short recent window's keys and values when needed.

## Mechanism

The ordinary [[kv-cache]] avoids recomputation by retaining past attention state. Replay deliberately gives back some of that compute saving: it keeps a suitable starting state and enough recent tokens to reconstruct a window of at most $W$ positions. The storage saving is useful only if replay is infrequent or cheap enough for the serving latency target. The implementation must specify when replay happens and what state is retained; otherwise reconstruction can silently grow with context length.

Compare with keeping the cache, compressing it, offloading it, and reducing the window. Check numerical results within tolerance and measure peak as well as persistent memory.

## One example

A model needs local attention to the last 128 positions but retains a much longer global history. It may rebuild the local cache from those 128 positions instead of storing a second persistent local cache.

## Check your understanding

**Question:** Does replay reduce total work? **Answer:** No; it exchanges additional work for less long-lived storage.
