# Agent Harness Interoperability

## Meaning

One client can use multiple agent runtimes only when their shared task interface preserves the behavior the client relies on.

## Mechanism

A common API needs more than a request and a final answer. It must define session identity, event ordering, file and workspace references, cancellation, errors, and authorization. An adapter may translate between runtimes, but any lost capability or weaker guarantee must be visible to the caller. Model behavior may also differ across harnesses even when the API shape matches.

## One example

A client cancels a coding task after a partial file write. One runtime reports cancellation only after effects settle; another reports immediately while a tool continues. Treating those as equivalent can corrupt the workspace. Conformance tests should capture the difference.

## Check your understanding

**Question:** Does an OpenAI-compatible response shape prove two agent harnesses are interchangeable? **Answer:** No; session, streaming, cancellation, file, error, and permission semantics also need testing.
