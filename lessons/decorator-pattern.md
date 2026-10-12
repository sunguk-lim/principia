# Decorator Pattern

## Meaning

An object decorator adds behavior by wrapping another object while keeping the interface that its client expects. Several decorators can be stacked without creating a subclass for each combination.

## Mechanism

A counting stream exposes `write(data)`, increments its counter, and forwards the call to an inner stream. A second wrapper might compress before forwarding. [[composition-over-inheritance]] assembles those behaviors at runtime; an [[abstract-base-class]] can specify the required interface.

## One example

Wrap a file writer with a counting writer and then with a tracing writer. Verify that both orders return the expected result and close the underlying file once. Be careful: a wrapper may not preserve concrete type identity or obscure special methods.

## Check your understanding

**Question:** What distinguishes an adapter from a decorator? **Answer:** The adapter changes the interface; the decorator preserves the interface and changes behavior.
