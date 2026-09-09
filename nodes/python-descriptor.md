---
id: python-descriptor
title: Python Descriptor
summary: A Python descriptor is a class attribute whose protocol methods intercept attribute reads, writes, or deletion so one reusable object can manage those operations across instances.
type: concept
tags: [languages/python]
prereqs: [dynamic-typing, hash-map]
sources: [https://docs.python.org/3/howto/descriptor.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Python Descriptor

## Summary

A **descriptor** is an object stored on a Python class that defines `__get__`, `__set__`, or `__delete__`. When normal dotted attribute access finds it, Python delegates the operation to that method, allowing validation, computed values, logging, and method binding to be implemented once and reused by many attributes.

## Grounded explanation

Ordinary instance state lives in a dictionary-like mapping from attribute names to values. A descriptor changes the lookup path: instead of simply returning or replacing an entry, the class-level object participates in the operation. This is a protocol of [[dynamic-typing]]—behavior is selected from methods present on the runtime object—not a special declaration syntax.

```python
class Positive:
    def __set_name__(self, owner, name):
        self.storage_name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("must be positive")
        setattr(instance, self.storage_name, value)

class Rectangle:
    width = Positive()
    height = Positive()

    def __init__(self, width, height):
        self.width = width
        self.height = height
```

When Python creates `Rectangle`, `__set_name__` tells each descriptor which class attribute owns it, so `width` and `height` choose distinct private names. Constructing `Rectangle(3, 4)` routes both assignments through `__set__`; constructing `Rectangle(3, -1)` raises before the invalid height is stored. Reading `r.width` invokes `__get__` and retrieves `_width` from the instance's attribute [[hash-map]].

Descriptors must be class attributes to participate in this lookup protocol. A descriptor placed directly in an instance dictionary is merely another value. Defining `__set__` or `__delete__` makes a data descriptor, which takes precedence over an instance entry of the same public name; a descriptor with only `__get__` is non-data and can be shadowed by an instance entry. That precedence is why managed writes cannot be bypassed accidentally by an ordinary assignment.

The mechanism is broader than validation. Python functions implement descriptor behavior to produce bound methods, and `property`, `classmethod`, `staticmethod`, and `cached_property` are descriptor-based tools. Prefer a descriptor when the same attribute policy belongs on several fields or classes; prefer a property when one class has one small managed attribute. In both cases, test class-level access, initialization, reassignment, deletion if supported, and storage-name collisions.

## Prerequisites

- [[dynamic-typing]]
- [[hash-map]]

## Sources

- [Python Descriptor Guide](https://docs.python.org/3/howto/descriptor.html): protocol definition, lookup precedence, automatic name notification, managed attributes, and validator examples.
