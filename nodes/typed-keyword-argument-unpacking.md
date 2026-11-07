---
id: typed-keyword-argument-unpacking
title: "Typed Keyword-Argument Unpacking"
summary: "Typed keyword-argument unpacking uses Unpack with a TypedDict to statically check keyword names, per-key value types and required presence without changing Python runtime calling semantics."
type: concept
tags: [languages/python]
prereqs: [typed-dict]
sources: ["https://peps.python.org/pep-0692/"]
status: explained
created: 2026-11-06
updated: 2026-11-08
---

# Typed Keyword-Argument Unpacking

## Meaning

Python's `**kwargs` collects keyword arguments into a dictionary. Annotating it as `**kwargs: str` describes each value as a string; it does not specify a set of permitted keyword names. `Unpack[SomeTypedDict]` instead expands a [[typed-dict|TypedDict]] schema into the keyword interface checked by a static type checker.

## Mechanism

PEP 692 specifies this form for Python 3.12. Required schema keys correspond to required keyword arguments; `NotRequired` keys may be omitted. Optional presence is independent of accepting `None` as a value. The annotation does not create a runtime validator or change ordinary dictionary unpacking.

```python
from typing import NotRequired, TypedDict, Unpack

class Options(TypedDict):
    retries: int
    label: NotRequired[str | None]

def configure(**options: Unpack[Options]) -> None:
    print(options["retries"])
    if "label" in options:
        print(options["label"])
```

A checker can accept `configure(retries=2)`, reject omission of `retries`, and reject a string value for that integer field. Omitting `label` and passing `label=None` are both permitted here but remain distinct dictionary states. `**options: Options` would mean that every keyword's value is itself an `Options` dictionary, which is a different interface.

## One example

A value with a wider schema may be compatible with a narrower TypedDict view while retaining extra runtime keys. Blindly forwarding that dictionary to a function with only explicit `retries` can therefore send an unexpected `label` keyword. Static compatibility did not delete a key. Extract the intended fields explicitly or ensure the receiving function has a compatible keyword contract. PEP 692 describes these forwarding and callable-assignment restrictions in detail.

Keyword collisions also matter: a name already bound by an ordinary parameter cannot independently denote the same keyword in the unpacked schema. A positional-only parameter has different binding semantics. Keep these distinctions in conformance tests for the supported checker and language versions.

## Check your understanding

Does a passing type check validate untrusted JSON at runtime? No. Parse and validate external values separately, and test both checker diagnostics and actual call behavior. Typed unpacking improves a static interface; it is not authorization, conversion or runtime schema enforcement.

## Typed dependency passing

A typed keyword mapping can carry already-created dependencies to constructors. The application still owns construction, lifetime and teardown; a TypedDict is neither a dependency resolver nor a runtime access-control system. This is an application of the callable contract, not a reason to make every resource accept arbitrary keywords.

For an original example, let a dependency mapping contain `store` and `clock`, while `Report` accepts only `store` and `Audit` accepts both. Construct `Report(store=deps["store"])` and `Audit(store=deps["store"], clock=deps["clock"])`. Explicit projection preserves the receiving contracts. Blind `Report(**deps)` sends an unexpected `clock` and can fail at runtime even when a narrower static view hides that extra key. Adding `**ignored` can avoid the runtime exception but may also hide misspellings and unintended coupling; it is a deliberate broader interface, not automatic type safety.

A test can supply a fake store and deterministic clock without global lookup, while production construction supplies live objects. Static checking can catch a missing required dependency or wrong value type; it cannot prove that a database connection is open, correctly authorized or closed at the right time. Test both checker diagnostics and runtime construction, and keep object lifecycle explicit. PEP 692 grounds keyword names, value types and forwarding restrictions rather than endorsing a particular dependency-injection framework.

## Prerequisites

- [[typed-dict]]

## Sources

- <https://peps.python.org/pep-0692/>
