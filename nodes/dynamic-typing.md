---
id: dynamic-typing
title: Dynamic Typing
summary: Under dynamic typing a value carries its own type tag at runtime and type checks happen as the program runs, so a variable is just a name that can hold a value of any type — in contrast to static typing, where each variable's type is fixed and checked before the program runs.
type: concept
tags: [languages/semantics]
prereqs: []
sources: [pierce-tapl]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Dynamic Typing

## Summary

Dynamic typing is the discipline in which the *type* of data — is this a number, a string, a function? — is attached to the value itself and consulted while the program runs, not fixed to the variable and checked beforehand. A value at runtime is effectively a pair: a small **type tag** plus the actual payload. Each operation, at the moment it executes, reads the tags of its inputs and decides what to do (or raises an error if they don't fit). The consequence is that a single variable can hold a number now and a string later, and no type annotations are needed — which makes for flexible, concise, quick-to-write code — but the flip side is that a type mismatch is only discovered when the offending line actually runs, and every operation pays a small cost to check tags and every value a small cost to store one. This contrasts with **static typing**, where types belong to variables, are known before execution, and mismatches are rejected up front.

## Grounded explanation

**The central question: where does the type live?** Every language must answer "what type is this thing, and when do we find out?" Static typing binds a type to each *variable* and settles the answer *before* the program runs (a separate checking phase rejects `x + "hello"` if `x` is declared a number). Dynamic typing binds the type to each *value* and settles it *as the program runs*. In a dynamically typed language a variable is just a name with no type of its own — it can be re-bound to a value of any type — while each runtime value knows what it is, because it carries a tag alongside its data.

**Why this design — and what it costs.** Attaching the type to the value is what lets the *same* name or the *same* container hold anything: a list can mix numbers and strings, a function can accept an argument of whatever type shows up. There are no type declarations to write, so programs are shorter and faster to prototype, and generic code (a function that works on "anything with a length," say) comes for free. The cost is threefold and unavoidable: (1) *when* errors surface — a type error hides until control actually reaches that line, so a mistake down a rarely-taken branch can lurk unnoticed; (2) *time* — each operation must inspect its operands' tags before acting; (3) *space* — every value drags a tag around. The design trades guaranteed-before-you-run safety and raw speed for flexibility and brevity.

**A concrete worked instance.** Consider, in a dynamically typed language:

```
x = 10          -- x now holds a value tagged "number"
x = "ten"       -- perfectly legal: same name, now a value tagged "string"
```

Rebinding `x` from a number to a string is fine, because the type belongs to the value, not to `x`. Now:

```
y = x + 1
```

At the instant `+` runs, it inspects the tag of `x`'s current value. If `x` holds a number, it adds. If `x` holds `"ten"` (a string), the `+` sees a string tag where it expected a number and raises a **runtime** type error — right then, not before. The non-degenerate part: put that `+` inside a branch that never executes —

```
if false then y = x + 1 end     -- never runs
```

— and the program runs to completion with no error at all, even though `x` is a string. That is the defining behavior of dynamic typing: the check is bound to the *execution* of the operation. Under static typing the very same `x + 1` would be rejected before the program ever started, branch taken or not.

## Prerequisites

_none yet_

## Sources

- pierce-tapl
