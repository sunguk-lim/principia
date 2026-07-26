---
id: lua
title: Lua
summary: Lua is a small, fast, embeddable scripting language whose single data structure is the table (a hash map); it is dynamically typed and garbage-collected, treats functions as first-class values with closures, offers coroutines for cooperative multitasking, uses metatables for extensible behavior, and runs on a compact register-based bytecode virtual machine.
type: concept
tags: [languages/scripting]
prereqs: [bytecode-vm, garbage-collection, dynamic-typing, closure, coroutine, metatable, hash-map]
sources: [lua-manual-5.4, programming-in-lua, lua-5.0-impl]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Lua

## Summary

Lua is a small, fast scripting language designed above all to be **embedded** inside a larger host program — game engines, web servers, and text editors — as its configuration and scripting layer. Everything about it serves that goal: a tiny implementation, and a handful of concepts reused everywhere instead of many special-case features. Its *one* data structure is the **table**, a [[hash-map]] that doubles as array, record, object, and module. It is **[[dynamic-typing|dynamically typed]]** (values carry their type, variables hold anything) and **[[garbage-collection|garbage-collected]]** (no manual memory management). Functions are first-class values that form **[[closure]]s**, giving it functional and object idioms without built-in classes. **[[coroutine]]s** provide cooperative multitasking as a core feature. **[[metatable]]s** let tables customize their own behavior, so operator overloading and inheritance fall out of the table mechanism rather than a separate object system. And the reference implementation compiles source to bytecode run on a register-based **[[bytecode-vm]]** — famously compact and quick, which is why Lua is the scripting language of choice where a small, fast, portable runtime matters.

## Grounded explanation

**What Lua *is*, and the design goal that shapes it.** Lua is a lightweight, portable scripting language whose defining purpose is *embeddability*: it is meant to be dropped into a host application written in another language and used to script it. That single goal explains its character — the implementation is small and self-contained, and rather than piling on features, Lua reuses a few powerful concepts everywhere. The identity of Lua is best understood as the particular *combination* of the traits below, each a general language idea it commits to wholesale.

**One data structure — the table.** Lua's sole built-in data structure is the table: a [[hash-map]] of keys to values. A table with consecutive integer keys is an array; with string keys, a record or module; with a [[metatable]], an object. This "one structure" decision is why the language stays small — there is no separate array, struct, or class construct to learn, just the table used in different ways.

**Extensible behavior — metatables.** A table's behavior is customizable by attaching a [[metatable]]. Because operator overloading, default values, and prototype-style inheritance (through the metatable's `__index` fallback) are all provided by this one mechanism, Lua needs no dedicated class system: object-orientation is a *convention* built on tables and [[metatable]]s, not a language keyword.

**Values and memory — dynamic typing and garbage collection.** Lua is [[dynamic-typing|dynamically typed]]: the type (nil, boolean, number, string, function, table, and a few more) travels with the value, and any variable can hold any of them. Memory is managed automatically by an incremental mark-and-sweep [[garbage-collection|garbage collector]] — crucial for an embedded scripting layer whose users are often not systems programmers and should not be reclaiming memory by hand.

**Functions and control — closures and coroutines.** Functions in Lua are first-class values, and combined with its scoping they form [[closure]]s — functions that capture surrounding local variables (*upvalues*), which underpins callbacks and the table-and-closure style of objects. For control flow beyond ordinary calls, Lua builds in [[coroutine]]s: cooperative, yield/resume routines that make generators, iterators, and cooperative schedulers straightforward.

**How it runs, and how it embeds.** The reference implementation does not interpret source text directly; it compiles each chunk to bytecode and executes it on a **register-based** [[bytecode-vm]]. The register-based design (rather than a stack-based one) is a widely cited reason for Lua's speed. Embeddability — the raison d'être — is done through a small C API by which the host program and Lua exchange values and call each other's functions; that API is what lets Lua serve as the scripting layer inside a C or C++ application. (The mechanics of that C boundary are beyond this node's scope.)

**A concrete worked instance.** A short program exercising the traits together — a table used as an object via a [[metatable]], with automatic memory and a [[coroutine]]:

```lua
Account = {}
Account.__index = Account                       -- misses delegate here (metatable)
function Account.new(b) return setmetatable({balance = b}, Account) end
function Account:deposit(x) self.balance = self.balance + x end

a = Account.new(100)   -- a is a table; when it becomes unreachable, GC frees it
a:deposit(50)          -- 'deposit' missing on a → __index → found in Account
print(a.balance)       -- 150   (balance is a dynamically typed number)

-- a coroutine as a generator
gen = coroutine.wrap(function() for i = 1, 3 do coroutine.yield(i) end end)
print(gen(), gen(), gen())   -- 1  2  3
```

Trace how each trait appears: `a` is a table, i.e. a [[hash-map]]; `setmetatable` attaches a [[metatable]] so the missing `deposit` key is resolved by `__index` delegation to `Account`; `balance` holds a number under [[dynamic-typing]], and the same field could later hold a value of another type; `Account.new` and `deposit` are functions stored *in a table as values*, and each could form a [[closure]] over surrounding locals; once `a` is no longer reachable, [[garbage-collection]] reclaims it with no explicit free; `gen` is a [[coroutine]] that yields `1, 2, 3` across three calls, remembering its loop position between them; and the whole chunk is compiled to bytecode and executed by the register-based [[bytecode-vm]]. The example is non-degenerate because it touches every declared prerequisite at once — table, metatable, dynamic value, first-class value, garbage collection, coroutine, and the VM — which is exactly what "Lua" *is*: their coherent combination in one small language.

## Prerequisites

- [[bytecode-vm]]
- [[garbage-collection]]
- [[dynamic-typing]]
- [[closure]]
- [[coroutine]]
- [[metatable]]
- [[hash-map]]

## Sources

- lua-manual-5.4
- programming-in-lua
- lua-5.0-impl
