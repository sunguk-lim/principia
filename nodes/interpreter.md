---
id: interpreter
title: Interpreter
summary: An interpreter is a program that executes another program directly from its source (or an intermediate form), evaluating each construct as it goes, instead of first translating the whole program into the machine's native code and then running that.
type: concept
tags: [languages/runtime]
prereqs: []
sources: [crafting-interpreters, sicp]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Interpreter

## Summary

An interpreter is a program that *runs* another program directly, working through it construct by construct and carrying out each one's effect, rather than translating the whole thing ahead of time into the CPU's native machine code and handing that to the hardware. It is the alternative execution strategy to ahead-of-time compilation: a compiler produces a native executable and steps out of the way, whereas an interpreter stays resident and *is* the thing doing the work while the program runs. Its heart is a loop — read the next construct, decide what it means, do it, advance — the software echo of a CPU's own fetch–decode–execute cycle, but operating over a higher-level program form. This buys flexibility and portability (no separate build, runs anywhere the interpreter is ported, and program state can be inspected and changed at runtime) at the cost of speed (every construct pays its decoding overhead each time it executes).

## Grounded explanation

**The central object.** There are two broad ways to run a program written in a high-level language. One is to *compile ahead of time*: translate the entire program into the processor's native machine code once, producing an executable the hardware runs on its own. The other is to *interpret*: keep the program in a higher-level form and have a second program — the interpreter — read that form and perform its effects step by step. The interpreter is itself already-running code (native, or itself interpreted, recursing until you finally reach hardware). The concept *is* this second strategy: a program whose job is to execute programs.

**Why it works — the fetch–decode–execute loop.** An interpreter's core is a single loop. It holds a pointer to "the current construct," and each turn it (1) *fetches* that construct, (2) *decodes* it — decides which kind it is — and (3) *executes* the matching action, then advances the pointer. This is exactly what a CPU does in silicon for machine instructions; an interpreter reproduces the same cycle in software over a richer instruction form. Because the decision "what does this construct mean?" is made *while running*, the same program text can be inspected, halted, or modified mid-flight — the flexibility that makes interpreters the natural home of interactive prompts and dynamic language features. The price is that the decode step is paid on *every* execution of a construct: a loop body run a million times is re-decoded a million times, which is why interpreted code is slower than the equivalent compiled native code.

**A concrete worked instance — a tree-walking interpreter.** Take the expression `3 + 4 * 2`. Parsed by precedence it forms a small nested structure: a `+` whose left operand is `3` and whose right operand is a `*` of `4` and `2`. A *tree-walking* interpreter evaluates it by recursion — `eval` of a node asks for the value of its parts, then combines them:

- `eval(+)` needs its two operands, so it recurses.
  - `eval(3)` → the literal `3`.
  - `eval(*)` recurses again: `eval(4)` → `4`, `eval(2)` → `2`, then multiply → `8`.
- Back at the top, `+` combines `3` and `8` → `11`.

No native code for this expression was ever produced; the interpreter *directly performed* the additions and multiplications as it walked the structure. The nesting (`*` inside `+`) is what makes the example non-degenerate: it forces the recursion and shows precedence being honored by structure, not by any special rule in the loop. Run the same expression a second time and every one of those decode-and-recurse steps happens again — the overhead that ahead-of-time compilation would have paid just once.

## Prerequisites

_none yet_

## Sources

- crafting-interpreters
- sicp
