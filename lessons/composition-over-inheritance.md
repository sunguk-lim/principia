# Composition over Inheritance

## Meaning

Composition connects small objects that each perform one role, instead of encoding every combination of roles in a subclass. It is a preference for the case where features vary independently, not a rule that inheritance is always wrong.

## Mechanism

Imagine a logger with two output destinations, two formats, and an optional filter. An inheritance-only design can accumulate subclasses for combinations. A compositional logger stores a destination, formatter, and filter and delegates each step. The collaborator implementations may themselves use [[object-oriented-inheritance]], but the logger does not need a subclass for each configuration.

## One example

Add an HTML formatter to a file-or-network logger. If it implements the formatter contract, both destinations can use it without adding two more logger subclasses. Test both combinations and test what happens when the output fails.

## Check your understanding

**Question:** When might inheritance still be better? **Answer:** When there is a stable substitutable subtype relationship with shared behavior, and composition would add needless wiring.
