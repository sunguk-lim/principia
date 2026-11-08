---
id: typed-dict-extra-items
title: "TypedDict Extra-Item Contracts"
summary: "TypedDict extra-item contracts distinguish open structural schemas, closed key sets and explicitly typed additional keys without adding runtime data validation."
type: concept
tags: [languages/python]
prereqs: [typed-dict]
sources: [https://peps.python.org/pep-0728/]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# TypedDict Extra-Item Contracts

## Meaning

A TypedDict names known keys and their value types. Its extra-item contract states what other keys may exist in values assignable to that schema. PEP 728 distinguishes the traditional open behavior, a closed key set and additional keys with a declared value type.

## Mechanism

Start with [[typed-dict]] and its distinction between required presence and value type. With `closed=True`, no undeclared keys are permitted by the static schema; this is equivalent to `extra_items=Never`. With `extra_items=int`, undeclared string keys may hold integers. Known keys need not have that same value type. Extra items are non-required regardless of `total`; do not use `Required` or `NotRequired` to qualify the extra-items parameter.

Traditional open TypedDict behavior permits hidden extra items under structural assignability, but still rejects unexpected keys in checked literal construction. It does not mean every arbitrary key access or write is valid. `closed` and `extra_items` cannot be supplied together. PEP 728 targets Python 3.15; verify runtime, backport and checker support rather than assuming every older typing implementation accepts the parameters. These annotations do not inspect incoming JSON at runtime.

## One example

Under supporting tooling, define `class Metrics(TypedDict, extra_items=int): label: str`. The conceptual value `{'label': 'run-a', 'tokens': 12, 'errors': 2}` has a string at the known `label` key and integers at the extra keys. Setting `tokens` to `'twelve'` violates the extra-item type. Defining a separate closed schema containing only `label: str` rejects `tokens` altogether. With `total=False`, the known label may be absent, but any present extra value must still be an integer.

## Check your understanding

Does rejecting an extra key statically reject hostile input at runtime? No. Values remain ordinary dictionaries. Parse and validate untrusted input separately. Test literal construction, structural assignment, inherited contracts and permitted key operations with the actual checker. Closing a schema is a key-set constraint, not object immutability or a ban on changing declared mutable items.

## Prerequisites

- [[typed-dict]]

## Sources

- <https://peps.python.org/pep-0728/>
