# Prebound Method Pattern

## Meaning

A prebound method is a callable that remembers the object it belongs to. Code receiving the callable supplies only its remaining arguments.

## Mechanism

When code reads `worker.handle`, Python's [[python-descriptor]] binding pairs the underlying function with `worker`. The method is a [[first-class-function]] value, so an event dispatcher can store it and later call `callback(event)`. That call reaches `worker.handle(event)`.

## One example

Register `worker.handle` as a callback for a message queue. When a message arrives, the queue invokes the callback with only the message. Unregister it during shutdown; retaining the bound method also retains the worker object.

## Check your understanding

**Question:** Why can a callback registry cause an unexpected memory leak? **Answer:** Keeping a bound method alive keeps its receiver alive too, even if other code no longer needs that object.
