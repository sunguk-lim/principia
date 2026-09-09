---
id: typed-dict
title: Python TypedDict
summary: TypedDict gives an ordinary Python dictionary a statically checked schema whose literal string keys can have different value types and independently required or optional presence.
type: concept
tags: [languages/python]
prereqs: [static-type-checking, hash-map]
sources: [https://peps.python.org/pep-0589/, https://docs.python.org/3/library/typing.html#typing.TypedDict]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Python TypedDict

## Summary

A **TypedDict** describes the expected shape of a Python dictionary to a [[static-type-checking|static type checker]]: each permitted string key has its own value type, and each key is required or optional. At runtime, the value remains an ordinary `dict`; the declaration adds no automatic input validation or new storage object.

## Grounded explanation

A uniform annotation such as `dict[str, str | int]` says every string key is allowed and every value may be either a string or integer. It cannot express the relationship “the `name` key has a string, while `year` has an integer.” `TypedDict` records that key-dependent relationship:

```python
from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int

def release_age(movie: Movie, current_year: int) -> int:
    return current_year - movie["year"]
```

A checker can infer that `movie["year"]` is an integer, reject `{"name": 1982, "year": "Blade Runner"}`, and report a missing required key. The runtime object is still the same [[hash-map]] used by an ordinary Python `dict`: `Movie(name="Arrival", year=2016)` returns a `dict`, and `isinstance(value, Movie)` is not supported as schema validation.

Required presence and value type are separate constraints. With `total=False`, keys declared in that body may be absent; modern declarations can mark individual keys `Required` or `NotRequired`. Optional presence does not mean the value itself may be `None`. For example, an absent `subtitle` and a present `subtitle: None` are different states and require different annotations.

TypedDict compatibility is structural: a value can satisfy an interface because it has the required keys with compatible types, not because its runtime class inherits from that declaration. Mutability limits otherwise tempting substitutions. If one interface permits deleting a key or writing a wider value type, passing a dictionary whose contract requires that key or a narrower type would be unsafe.

Use TypedDict when data must remain dictionary-shaped—for example, a JSON-like payload—and static checks are valuable. Use runtime parsing or validation at untrusted boundaries, because annotations alone do not inspect incoming values. Use a class when behavior, runtime identity, invariants, or controlled construction are the central requirement.

## Prerequisites

- [[static-type-checking]]
- [[hash-map]]

## Sources

- [PEP 589](https://peps.python.org/pep-0589/): fixed-key dictionary typing, structural compatibility, required keys, and ordinary-dictionary runtime behavior.
- [Python `typing.TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict): current standard-library interface and runtime limitations.
