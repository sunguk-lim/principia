# Global Object Pattern

## Meaning

A global object is an object kept in a module and imported by clients that need shared process-local state. It can remove parameter plumbing, but it also hides a dependency.

## Mechanism

Python imports normally reuse the module object. If a module defines `metrics = Registry()`, importing code can refer to that same registry through its module-level name mapping, conceptually a [[hash-map]]. This does not create one registry across multiple processes or machines, and mutable access may need synchronization.

## One example

A command-line tool keeps a process-wide metrics registry. Two modules import it and record counts. Tests must reset it between cases; a web service with multiple worker processes must aggregate metrics somewhere else.

## Check your understanding

**Question:** Why is a module global a poor per-request configuration store? **Answer:** Concurrent requests share it, so one request may overwrite another's configuration; explicit request-scoped dependencies are safer.
