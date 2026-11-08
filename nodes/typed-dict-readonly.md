---
id: typed-dict-readonly
title: "Read-Only TypedDict Items"
summary: "Read-only TypedDict items remove rebinding and deletion authority through a typed view without freezing the dictionary or objects stored inside it."
type: concept
tags: [languages/python]
prereqs: [typed-dict]
sources: [https://peps.python.org/pep-0705/]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Read-Only TypedDict Items

## Meaning

`ReadOnly[T]` qualifies a TypedDict item so a static type checker rejects adding, replacing or deleting that item through the qualified view. It does not turn the dictionary into an immutable runtime object. Read-only access is a restriction on an interface's authority, not a claim that no other reference can mutate the data.

## Mechanism

[[typed-dict]] normally exposes mutable dictionary operations. Mutability limits assignability: a function that may write a broader value type or delete an optional key cannot safely receive a dictionary promising a narrower required item. A read-only view removes those writes and can therefore accept otherwise safe narrower or required variants under the specification's compatibility rules.

PEP 705 adds `typing.ReadOnly` in Python 3.13. It can combine with requiredness qualifiers; whether a key must be present is separate from whether the current view may change it. Read-only is shallow. When an item holds a mutable list, preventing item replacement does not prevent appending to that list. Runtime enforcement and deep immutability require different mechanisms.

## One example

With supporting tooling:

```python
from typing import ReadOnly, TypedDict

class Team(TypedDict):
    name: str
    members: ReadOnly[list[str]]

team: Team = {'name': 'Orion', 'members': ['Ada']}
team['name'] = 'Lyra'               # permitted
team['members'] = ['Bo']            # static error
team['members'].append('Bo')        # permitted: list stays mutable
```

Deleting `members` is also rejected through this typed view. At runtime the assignment is ordinary dictionary mutation; Python does not automatically intercept it. Another suitably typed mutable alias may also change the underlying item, so callers cannot infer that the observed value is permanently constant.

## Check your understanding

Can read-only items replace validation at an external boundary? No. A checker constrains analyzed code, not arbitrary incoming dictionaries or untyped aliases. Check supported versions and checker behavior, required versus optional keys, attempted replacement/deletion and nested mutation. Choose a truly immutable representation when stable contents are part of the runtime contract rather than merely limiting one function's write authority.

## Prerequisites

- [[typed-dict]]

## Sources

- <https://peps.python.org/pep-0705/>
