# Prototype Pattern

## Meaning

A prototype creates a new object by copying a configured exemplar instead of selecting and invoking a concrete constructor.

## Mechanism

A **prototype** is an exemplar object used to create another object by copying. A registry can hold configured exemplars and clone the selected one on demand, avoiding a hard-coded constructor choice. The key decision is copy semantics: shallow copies share nested objects, while deep copies attempt to duplicate reachable state and can fail on resources such as locks or sockets.

## One example

A registry stores a configured parser prototype; each request receives a clone with independent mutable buffers.

## Check your understanding

**Question:** What is the main copying risk? **Answer:** A shallow copy can share nested mutable state or external resources.
