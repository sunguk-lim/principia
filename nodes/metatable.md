---
id: metatable
title: Metatable
summary: A metatable is an ordinary table attached to another table to customize how it behaves — when an operation such as indexing a missing key or applying an operator would otherwise be undefined, the language looks the operation up as a key-value entry in the metatable and runs the handler found there.
type: concept
tags: [languages/semantics]
prereqs: [hash-map, key-value]
sources: [lua-manual-5.4]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Metatable

## Summary

In a language whose one data structure is the table — a [[hash-map]] holding [[key-value]] pairs — a **metatable** is a second table hung off a first one to *change what operations on the first table mean*. Its entries are keyed by special event names (like `__index` for "a key was missing" or `__add` for "the `+` operator was applied") and their values are handler functions or fallback tables. When a triggering operation happens on the main table, the runtime consults its metatable for a matching entry and, if it finds one, uses it instead of the default behavior. Because a metatable is just a table and its contents are ordinary [[key-value]] entries looked up by [[hash-map]], this single mechanism delivers operator overloading, default values, read/write interception, and — via `__index` pointing at another table — prototype-style inheritance, all without any separate class system.

## Grounded explanation

**The central object.** Start from the setting: the table is a [[hash-map]] that stores [[key-value]] pairs and serves as the language's universal structure (arrays, records, objects, and modules are all tables). By default, operations on a table have fixed meanings — `t[k]` looks `k` up and returns its value or `nil`; `a + b` is only defined for numbers. A **metatable** is a table you attach to another table to *override or extend* those meanings. The trick is uniformity: the metatable's own contents are just [[key-value]] pairs, where each key is a specific *event* name the runtime knows about and each value is what to do when that event fires. So "customize behavior" reduces to "put an entry in a table," and dispatching that customization reduces to a [[hash-map]] lookup in the metatable.

**Why it works — one mechanism, many features.** The most important event is `__index`, which fires on a *missing-key read*. Reading `t[k]` first does a normal [[hash-map]] lookup in `t`; on a hit it returns the value as usual. On a **miss**, instead of simply yielding `nil`, the runtime looks up the `__index` entry in `t`'s metatable: if it is a table, the lookup is retried *there* (delegation); if it is a function, that function is called to compute the result. This one fallback is what turns a [[key-value]] miss into *inheritance* — an object table with few of its own entries can delegate to a shared "parent" table for the rest. Other events generalize the same idea to operators and more: `__add` fires when `+` is applied to a table (giving *operator overloading*), `__newindex` intercepts writes, `__call` makes a table callable, and so on. Every one is resolved the same way — the runtime, upon hitting an operation it cannot handle by default, performs a [[hash-map]] lookup of the event name in the metatable and defers to what it finds.

**A concrete worked instance.** Use a metatable both for method inheritance (`__index`) and for an overloaded operator (`__add`):

```
Account = {}                    -- a "class" table holding shared methods
Account.__index = Account       -- misses on an instance delegate to Account
function Account.deposit(self, x) self.balance = self.balance + x end

obj = {balance = 100}           -- an instance: its own table
setmetatable(obj, Account)      -- attach Account as obj's metatable

obj.deposit(obj, 50)            -- obj has no "deposit" key → __index → found in Account
print(obj.balance)              -- 150
```

Reading `obj.deposit` first does a [[hash-map]] lookup in `obj` and *misses* (obj only has `balance`). The runtime then reads the `__index` [[key-value]] entry in obj's metatable, finds the `Account` table, and retries the lookup there — where `deposit` lives. So `obj` "inherited" the method with no copying: pure [[key-value]] delegation. Now overload an operator:

```
Vec = {}
Vec.__add = function(a, b) return setmetatable({a[1]+b[1], a[2]+b[2]}, Vec) end

v1 = setmetatable({1, 2}, Vec)
v2 = setmetatable({3, 4}, Vec)
v3 = v1 + v2                    -- '+' on tables is undefined by default → __add fires
print(v3[1], v3[2])            -- 4  6
```

`v1 + v2` has no built-in meaning for tables, so the runtime looks up `__add` in the metatable and calls it. The example is non-degenerate because it exercises *both* directions the mechanism serves — a missing-key lookup routed to another table (`__index` inheritance) and an operator with no default meaning routed to a handler (`__add` overloading) — showing that both are the same "look the event up in the metatable" rule over ordinary [[key-value]] entries.

## Prerequisites

- [[hash-map]]
- [[key-value]]

## Sources

- lua-manual-5.4
