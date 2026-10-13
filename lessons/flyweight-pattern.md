# Flyweight Pattern

## Meaning

A flyweight shares immutable intrinsic state among many logical objects while keeping context-specific state outside the shared object.

## Mechanism

A **flyweight** reuses one object for many equal intrinsic values. A cache keyed by value, conceptually a [[hash-map]], can return a shared immutable object while callers keep per-use position or ownership outside it. Python's `sys.intern()` illustrates identity reuse for equal strings, but interning is an optimization rather than a semantic requirement for ordinary string equality.

## One example

Many displayed labels share one immutable style object while each label keeps its own position.

## Check your understanding

**Question:** Why must per-use position stay outside the flyweight? **Answer:** Shared mutable context would let one use affect another.
