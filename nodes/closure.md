---
id: closure
title: Closure
summary: A closure is a first-class function bundled with the environment of variables captured from the lexical scope where it was defined, so the function keeps access to those outer variables even after the enclosing scope has returned.
type: concept
tags: [languages/semantics]
prereqs: [first-class-function, lexical-scoping]
sources: [sicp]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Closure

## Summary

A closure is what you get when a language combines two features: functions that are values ([[first-class-function]]) and names that are resolved by where they are written ([[lexical-scoping]]). A closure is a function packaged together with a snapshot of the surrounding variables it uses — its *captured environment* — so that when the function is later called, possibly long after the code that created it has finished, it still sees those variables. In other words, a closure is **code plus the environment it closed over**. This is what lets a function returned from another function keep working: the outer function's locals, which would normally disappear when it returns, are kept alive because the returned function captured them. Closures give you private, persistent state attached to a function — counters, configured callbacks, generators — without needing objects or classes.

## Grounded explanation

**Why the two prerequisites combine into something new.** Take [[first-class-function]] alone: you can create a function inside another function and return it as a value. Take [[lexical-scoping]] alone: a function's free names (names it uses but does not declare) refer to the bindings in the enclosing text where the function is *written*. Put them together and a tension appears. Suppose an outer function declares a local variable and returns an inner function that mentions it. By [[lexical-scoping]], the inner function's use of that name refers to the outer function's local. But by ordinary execution, when the outer function returns, its locals are gone. If we honored [[lexical-scoping]] literally, the returned function would refer to a variable that no longer exists.

**The resolution — capture.** A closure resolves the tension by **capturing** the referenced outer variables: the function value carries with it the bindings its free names need, keeping them alive for as long as the function itself lives. So a closure is not just the function's code — it is the code *and* a reference to the environment of captured variables (often called *upvalues*). Two facts follow, and they are the whole point. First, the captured variables *outlive* the scope that created them, because the closure holds them. Second, the captured variables are genuinely the *same* variables, not copies — if the closure mutates one, the change persists across calls, giving the function private state. If several closures capture the *same* environment, they share that state.

**A concrete worked instance.** A counter factory:

```
function makeCounter()
  local n = 0                       -- a local of makeCounter
  return function()                 -- a first-class function value, returned
    n = n + 1                       -- free name n → makeCounter's local (lexical)
    return n
  end
end

c = makeCounter()   -- makeCounter has RETURNED; its n survives inside the closure c
c()                 -- 1
c()                 -- 2
c()                 -- 3

c2 = makeCounter()  -- a fresh call → a fresh n, a separate captured environment
c2()                -- 1   (not 4!)
c()                 -- 4   (c's own n continued)
```

By [[lexical-scoping]], the inner function's `n` is `makeCounter`'s local; because the inner function is [[first-class-function|first-class]] it is returned and stored in `c`. The closure keeps `n` alive after `makeCounter` returned, so successive calls to `c` see the *same* `n` incrementing: `1, 2, 3`. The non-degenerate part is `c2`: a second call to `makeCounter` produces a closure over a *different* `n`, so `c2()` starts again at `1` while `c` independently continues at `4`. Two closures, two private environments — visible proof that a closure captures its own environment rather than sharing one global variable.

## Prerequisites

- [[first-class-function]]
- [[lexical-scoping]]

## Sources

- sicp
