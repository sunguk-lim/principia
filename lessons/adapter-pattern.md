# Adapter Pattern

## Meaning

An adapter connects a client to an existing object whose interface does not match what the client expects. It translates at the boundary rather than changing either component.

## Mechanism

A report exporter might call `write(text)`, while a legacy destination only offers `send(bytes, encoding)`. An adapter holds the destination and implements `write` by encoding and sending. [[composition-over-inheritance]] keeps the exporter independent of the legacy API. An [[abstract-base-class]] can state the expected method contract but is optional in Python.

## One example

Wrap a legacy queue in `QueueWriter.write(text)`. Check not only that it accepts a string, but that encoding, error handling, and shutdown behavior match what the exporter assumes.

## Check your understanding

**Question:** How is an adapter different from a decorator? **Answer:** An adapter changes the interface presented to the client; a decorator generally preserves it while adding behavior.
