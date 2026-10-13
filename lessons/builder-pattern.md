# Builder Pattern

## Meaning

A builder accumulates construction steps so a client can create a complex product without assembling every internal part.

## Mechanism

A **builder** accepts a sequence of construction commands and creates a complex result behind a simpler interface. For example, a report builder can accept title, sections, and figures while assembling the internal document tree. This uses [[composition-over-inheritance]] when the builder delegates parts of construction to collaborators.

## One example

A report API accepts sections and figures, then validates and emits a document tree.

## Check your understanding

**Question:** When is a separate builder unnecessary? **Answer:** When a direct constructor with clear optional arguments captures the same contract.
