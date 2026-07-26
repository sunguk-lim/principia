---
id: stack
title: Stack
summary: A stack is a collection of items that you can only touch at one end, called the top.
type: concept
tags: [algorithms]
prereqs: [dynamic-array]
sources: [study-notes.html#9]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Stack

## Summary

A stack is a collection of items that you can only touch at one end, called the top. You add an item by *pushing* it onto the top, and you remove an item by *popping* the one currently on top — so the item you get back is always the most recently added one still present. This last-in, first-out discipline is the whole point: a stack remembers things in the reverse of the order they arrived, which is exactly what you want when the most recent unfinished task is the one you must deal with next. A stack is naturally built on top of a [[dynamic-array]]: pushing is appending to the end of the array, popping is removing the last element, and both are the array's cheap end-operations, so both run in amortized constant time. Stacks underlie matching nested brackets, undo, the chain of unfinished function calls, depth-first exploration, and the monotonic stack.

## Grounded explanation

**The central object and its one rule.** A stack is a collection of items with a single point of access, the **top**. Only two operations change it. **Push** takes an item and places it on the top, on top of whatever was already there. **Pop** removes the item currently on the top and hands it back. (A third, peek, just looks at the top item without removing it.) Crucially, you cannot reach in and touch any item below the top — the only item you can ever read or remove is the most recent one you pushed that has not yet been popped. The defining rule that follows is **LIFO**, short for *last-in, first-out*: the last item pushed in is the first item popped out. This is the invariant the structure always maintains, and everything else about a stack is a consequence of it.

**Why this one rule is useful.** LIFO is not an arbitrary restriction; it captures a recurring situation — *the most recent unfinished thing must be handled first*. When you are partway through some task and a sub-task interrupts you, you must finish the sub-task before you can resume the original; if that sub-task spawns its own sub-task, that innermost one comes first of all. The order in which you *return* to the suspended tasks is the exact reverse of the order in which you *suspended* them, which is precisely LIFO. A stack is the data structure that records suspended work and always gives back the most-recently-suspended piece. That single shape explains every use below.

**Why a [[dynamic-array]] is the natural home.** A [[dynamic-array]] is an ordered sequence stored in one unbroken run of memory; its cheap operations are at the **end** — appending one element past the current last one, and removing the last element, both amortized O(1) (constant cost on average, even though an append that fills the block triggers a doubling-and-copy). Its *expensive* operations are inserting or removing in the middle or at the front, because every later element must slide over, which is O(n) (cost growing with the number of elements). A stack asks for only end-operations, so it maps onto the array's cheap end perfectly: declare the **end of the array to be the top of the stack**. Then **push = append** (write past the last element) and **pop = remove-last** (drop the final element). Neither operation ever touches the middle or front, so neither ever shifts elements — both inherit the array's amortized-O(1) end cost. This is why the cheat sheet lists a stack as a `list` with "push / pop O(1)": the stack is just a [[dynamic-array]] disciplined to use only its fast end. Choosing the *front* of the array as the top would have been a disaster — every push would shift all elements right and every pop shift them left, turning O(1) into O(n) — so the choice of which end is the top is the one design decision that makes a stack cheap.

**First worked instance — LIFO reverses order.** Start with an empty stack and push the numbers `1`, `2`, `3` in that order. Tracking the array underneath, with the rightmost element being the top:

- Push `1`: array `[1]`, top is `1`.
- Push `2`: append to the end → `[1, 2]`, top is `2`.
- Push `3`: append to the end → `[1, 2, 3]`, top is `3`.

Now pop three times. Each pop removes the current last element:

- Pop: removes `3` (the most recent push) → array `[1, 2]`. Returned: `3`.
- Pop: removes `2` → array `[1]`. Returned: `2`.
- Pop: removes `1` → array `[]`. Returned: `1`.

The items came back `3, 2, 1` — the exact reverse of the order they went in. That reversal is LIFO made visible, and it is the simplest demonstration of why a stack is the tool whenever you need to undo or unwind a sequence of actions in reverse: the undo history is a stack, and "undo" is a pop of the most recent action.

**Second worked instance — matching nested brackets.** A classic use is checking whether a string of brackets is correctly nested and balanced — for example whether every opener has a matching closer in the right order. The algorithm uses one stack: scan the string left to right; when you meet an **opener** (`(` or `[`) push it; when you meet a **closer** (`)` or `]`) pop the top opener and check it is the matching kind; the string is valid only if every closer found a correct match and the stack is empty at the end (nothing left unclosed). LIFO is exactly right here because the *innermost* open bracket — the most recent opener pushed — is the one that must close *first*. Run it on `([])`:

- `(` is an opener: push it. Stack: `[ ( ]`.
- `[` is an opener: push it. Stack: `[ (, [ ]`. The `[` is now on top, sitting inside the `(`.
- `]` is a closer: pop the top, which is `[`. It matches `]` (square with square) — good. Stack: `[ ( ]`.
- `)` is a closer: pop the top, which is `(`. It matches `)` (round with round) — good. Stack: `[ ]` (empty).

End of string with an empty stack and every match correct → **valid**. Now contrast `([)]`, which has the same characters but crossed instead of nested:

- `(` opener: push. Stack: `[ ( ]`.
- `[` opener: push. Stack: `[ (, [ ]`, top is `[`.
- `)` closer: pop the top, which is `[`. But `)` is round and `[` was square — **mismatch**. The check fails immediately.

The two strings differ only in arrangement, yet the stack catches the second: because `[` was pushed most recently it must be closed before `(`, so a `)` arriving while `[` is still open is provably wrong. This is the non-degenerate case — it exercises both a successful nested match and a crossing failure, which a single pair like `()` would not.

**The family of uses, in plain terms.** Every common stack application is the "most-recent-unfinished-first" shape in disguise. The **call stack** is the chain of function calls that have started but not yet returned: calling a function pushes its frame, returning pops it, and a function always returns to whichever caller most recently invoked it — LIFO. **Undo** is a stack of past actions; the most recent action is undone first. **Depth-first search**, an exploration strategy that walks as deep as possible down one path before backtracking, uses a stack to remember the branch points still to revisit: you dive down pushing each step, and when you hit a dead end you pop back to the most recently deferred branch and continue — the deferred work is consumed newest-first. (This contrasts with a breadth-first, level-by-level exploration, which instead processes its pending items oldest-first.) Finally the **monotonic stack** is a stack kept deliberately sorted — you pop away elements that violate the order before pushing a new one — used to answer "for each element, what is the next greater element to its right?" in a single pass; the popping discards candidates that the newest element has made obsolete, again most-recent-first. All of these are one structure, and the reason they all reach for a stack is the single LIFO rule.

**Putting it together.** A stack is a [[dynamic-array]] restricted to its fast end and renamed: push appends, pop removes-last, both amortized O(1), and the resulting last-in-first-out order is the structure's entire contribution — it makes "deal with the most recent unfinished thing first" a constant-cost operation, which is why nesting, unwinding, and depth-first work all rest on it.

## Prerequisites

- [[dynamic-array]]

## Sources

- `study-notes.html` §9 "Data structures cheat sheet" — the Stack (LIFO) row (`list`; push / pop O(1); "reach for it when: matching, undo, DFS, monotonic stack") and the "Problem signal → structure" line ("Most recent / matching pairs / nesting → stack"; "Next greater / window maximum → monotonic stack or deque").
