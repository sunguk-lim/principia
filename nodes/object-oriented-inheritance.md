---
id: object-oriented-inheritance
title: Object-Oriented Inheritance
summary: Object-oriented inheritance defines a derived class from one or more base classes so method lookup and subtype behavior can be reused or overridden.
type: concept
tags: [languages/semantics]
prereqs: [namespace, python-descriptor]
sources: [https://docs.python.org/3/tutorial/classes.html#inheritance]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Object-Oriented Inheritance

## Summary

**Inheritance** creates a derived class whose instances use behavior from one or more base classes unless the derived class overrides it.

## Grounded explanation

In Python, `class Child(Base): ...` records `Base` in the class hierarchy. Attribute lookup searches the derived class and then its method resolution order. A method call binds the selected function through the [[python-descriptor]] protocol. An override replaces lookup at the derived class, while `super()` continues lookup after the current class according to the method resolution order rather than simply naming “the parent.”

Multiple inheritance combines several bases. Python uses a consistent method resolution order that supports cooperative calls through `super()`. Every participating method must follow compatible signatures and call conventions; directly naming one base can skip other classes in a cooperative hierarchy.

Inheritance is appropriate for a genuine substitutable “is-a” relationship and a stable shared protocol. Reusing a few lines of implementation is not sufficient. Deep hierarchies couple subclasses to base-class behavior and can make state, initialization, and method lookup difficult to reason about.

Composition is often simpler: store a collaborator and delegate work to it. Prefer composition when behavior must vary independently, when objects are not substitutable, or when several unrelated behaviors would otherwise create a fragile hierarchy. Abstract interfaces or structural protocols can express required behavior without inheriting implementation.

Test inherited behavior through the base contract, overrides, `super()` chains, initialization order, and multiple-inheritance diamonds. Inspect the actual method resolution order when behavior is ambiguous, and avoid relying on undocumented base-class internals or nominally non-public names in its [[namespace]].

## Prerequisites

- [[namespace]]
- [[python-descriptor]]

## Sources

- [Python Tutorial, “Inheritance”](https://docs.python.org/3/tutorial/classes.html#inheritance): documents derived classes, overriding, `isinstance`, `issubclass`, multiple inheritance, and method resolution order.
