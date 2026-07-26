---
id: first-class-function
title: First-Class Function
summary: A function is first-class when it is an ordinary value — it can be stored in a variable, passed as an argument, returned from another function, and created on the fly — so a program can manipulate functions exactly as it manipulates numbers or strings.
type: concept
tags: [languages/semantics]
prereqs: []
sources: [sicp]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# First-Class Function

## Summary

Something is a *first-class citizen* of a language when the language lets you do with it everything you can do with a basic value: bind it to a name, pass it into a routine, return it as a result, and store it in a data structure. A **first-class function** is a function that enjoys exactly this status — it is just another value, on equal footing with numbers and strings, rather than a fixed, named thing you can only call. This one property is what makes *higher-order functions* possible (functions that take or return other functions), and it is the enabler behind callbacks, parameterized behavior, and — together with the rule for how names are resolved — closures. The payoff is that *behavior itself* becomes something the program can pass around and build at runtime, not just data.

## Grounded explanation

**The central object.** In many older languages a function is a second-class thing: you can define it and call it, but you cannot hold one in a variable or hand one to another function. Making functions *first-class* removes that restriction — a function value can be used anywhere any other value can. Concretely, four abilities together define first-classness: you can **name** a function (assign it to a variable), **pass** it as an argument, **return** it from another function, and **construct** a new one anonymously in the middle of an expression. A language with all four treats `the function that adds one` as a value no different in kind from `the number 41`.

**Why it matters.** Once behavior is a value, it can be *abstracted over*. A sort routine need not hard-code how to compare elements; it takes a comparison *function* as an argument and works for any ordering. An event system stores functions (callbacks) to run later. A routine can *manufacture* a specialized function on demand and return it. All of this is "higher-order" programming, and it exists only because functions are first-class. This is also half of what a closure needs: to return a freshly built function that still remembers data, the function must first be something you are *allowed* to build and return — first-classness — and then it must retain access to the surrounding names, which is the job of the scoping rule.

**A concrete worked instance.** Two abilities, shown together. First, *passing* a function in:

```
function applyTwice(f, x)   -- f is a function value, an ordinary parameter
  return f(f(x))
end

function inc(n) return n + 1 end
applyTwice(inc, 5)          -- inc(inc(5)) = inc(6) = 7
```

Here `inc` is handed to `applyTwice` as data and called inside it. Second, *building and returning* a function:

```
function adder(n)
  return function(x) return x + n end   -- construct a new function, return it
end

add5 = adder(5)   -- add5 is now a function value
add5(3)           -- 8
add10 = adder(10)
add10(3)          -- 13
```

`adder` does not compute a number — it *produces a function* and returns it, and the returned function is stored in `add5` and later called. That a function can be both an argument (`applyTwice`) and a fabricated return value (`adder`) is the non-degenerate demonstration: it exercises all four abilities — name, pass, return, construct — that being first-class provides.

## Prerequisites

_none yet_

## Sources

- sicp
