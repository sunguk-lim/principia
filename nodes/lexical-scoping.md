---
id: lexical-scoping
title: Lexical Scoping
summary: Lexical (static) scoping resolves a variable name by the textual structure of the program — a name refers to the binding in the nearest enclosing block of source where it is written — so what every name means can be determined by reading the code, without running it.
type: concept
tags: [languages/semantics]
prereqs: []
sources: [sicp]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Lexical Scoping

## Summary

The *scope* of a name is the region of a program where that name is valid and refers to a particular binding. **Lexical scoping** (also called static scoping) fixes that meaning by the program's *written structure*: a use of a name refers to the declaration in the nearest enclosing block or function in the source text, and if it is not found there, the search proceeds outward through the enclosing blocks to the global level. Because the answer depends only on *where the name appears in the code*, you can determine what every name means just by reading the program — you never have to run it or know who called what. This predictability is the reason lexical scoping is nearly universal in modern languages, and it is precisely the rule a closure relies on when it captures the variables surrounding a function.

## Grounded explanation

**The central object.** A program is full of names — variables, parameters, functions — and the same name can be declared in more than one place. A *scoping rule* is the language's method for deciding, at each *use* of a name, which *declaration* it refers to. Lexical scoping answers by the **static nesting of the source**: blocks and functions nest inside one another textually, and a name resolves to the innermost enclosing block that declares it, searching from the point of use outward — inner block, then the block around it, and so on out to the global scope. The word *lexical* means exactly this: the resolution is a property of the text (the lexis), settled before anything runs.

**Why it works — and the contrast that makes it meaningful.** The alternative is *dynamic scoping*, where a name resolves to the most recent binding in the *runtime call chain* — that is, it depends on *who called you*, which can differ from call to call. Lexical scoping instead guarantees that a function's free names (names it uses but does not itself declare) mean whatever they meant *at the place the function was written*, regardless of where it is later called from. That guarantee is what enables *local reasoning*: you can understand a function by reading it and its surrounding text, without tracing every possible caller. It is also the foundation a closure builds on — "capture the surrounding variables" is only well-defined because lexical scoping says precisely which surrounding variables a function's names refer to.

**A concrete worked instance.** Consider nested definitions with a deliberately reused name:

```
x = 1                     -- a global x

function outer()
  x = 2                   -- a new, local x, shadowing the global inside outer
  function inner()
    return x              -- which x?
  end
  return inner
end

f = outer()
result = f()
```

Resolve `inner`'s `x` by the written nesting: `inner` declares no `x` of its own, so look one level out — `outer`, which declares a local `x = 2`. Found. So `inner` returns `2`, and it returns `2` *even though `f()` is called at the top level, where the visible `x` is the global `1`*. The runtime location of the call is irrelevant; only the textual home of `inner` matters. The reused name (a local `x` inside `outer` *shadowing* the global `x`) is the non-degenerate ingredient: it forces the outward search to stop at the inner declaration and makes the lexical-vs-dynamic distinction visible — under dynamic scoping, `f()` called at top level would instead have seen the global `x = 1` and returned `1`.

## Prerequisites

_none yet_

## Sources

- sicp
