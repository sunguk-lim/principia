# Iterator Pattern

## Meaning

An iterator exposes sequential access to elements without requiring callers to know a container’s internal representation.

## Mechanism

An **iterator** yields elements one at a time through a stable traversal interface. In Python, `iter(container)` obtains an iterator and `next(iterator)` advances it until `StopIteration`; a `for` loop drives that protocol automatically. The container can change its internal storage without changing the consumer's loop.

## One example

A log reader yields records one at a time without loading the whole log into memory.

## Check your understanding

**Question:** Can the same iterator always be traversed twice? **Answer:** No; most iterators are single-pass, even if their container is re-iterable.
