---
id: bytecode-vm
title: Bytecode Virtual Machine
summary: A bytecode virtual machine runs a program in two stages — a compiler first translates the source into a compact, invented instruction set called bytecode, then a software machine interprets those instructions one at a time over a simple operand model (an operand stack or a bank of virtual registers), trading a little of native code's speed for portability.
type: concept
tags: [languages/runtime]
prereqs: [interpreter, stack]
sources: [crafting-interpreters, lua-5.0-impl]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Bytecode Virtual Machine

## Summary

A bytecode virtual machine (VM) is a two-stage way to run a program that sits between a slow tree-walking [[interpreter]] and a full native compiler. First a compiler translates the source once into **bytecode** — a made-up, compact instruction set with small fixed-format operations (an opcode plus a few operands). Then the VM, itself an [[interpreter]] whose "machine language" *is* that bytecode, runs a tight fetch–decode–execute loop over the flat instruction array. Because the instructions are uniform and pre-decoded from the messy source, dispatch is far faster than re-walking a syntax structure every time, yet the program stays portable: any platform with the VM can run the same bytecode. The VM needs somewhere to hold intermediate values, and there are two classic designs — a **stack-based** model that pushes and pops operands on an operand [[stack]], or a **register-based** model that names slots in a fixed array of virtual registers.

## Grounded explanation

**The central object and why bytecode exists.** A plain tree-walking [[interpreter]] runs a program by repeatedly walking its parsed structure, re-deciding at every step what each node means. That re-decoding is pure overhead, paid on every execution of every construct. A bytecode VM removes it by *compiling once*: it lowers the source into a linear sequence of small, uniform instructions — the bytecode — and from then on execution is a simple loop over an array. The VM is still an [[interpreter]] — it fetches, decodes, and executes — but its instructions are now flat and regular, so decoding is cheap and the loop is fast. "Virtual machine" names the idea that the bytecode targets an *invented* processor (with its own instruction set and operand model) that the VM emulates in software, instead of targeting a real CPU.

**The operand model — where intermediate values go.** Instructions like "add" need operands and a place to put results. Two designs dominate. A **stack-based** VM keeps an operand [[stack]]: most instructions push or pop it, so `ADD` pops the top two values and pushes their sum. Bytecode for a stack machine is very compact (operands are implicit — "the top of the [[stack]]") but a computation takes many small instructions. A **register-based** VM instead gives instructions explicit operands naming slots in a fixed array of virtual registers, so `ADD R3, R1, R2` means "R3 ← R1 + R2" in one instruction; this uses fewer, fatter instructions and tends to be faster, at the cost of larger instructions. (Lua's VM is a notable register-based design.) Separately, function calls and returns are tracked on a call [[stack]] of frames — a direct use of the last-in-first-out [[stack]] discipline, since the most recently called function is always the first to return.

**A concrete worked instance.** Compile the expression `3 + 4 * 2` (multiplication binds tighter than addition) for a **stack-based** VM:

```
PUSH 3      ; operand stack: [3]
PUSH 4      ; [3, 4]
PUSH 2      ; [3, 4, 2]
MUL         ; pop 4,2 → push 8   → [3, 8]
ADD         ; pop 3,8 → push 11  → [11]
```

Trace the operand [[stack]] right-to-left as the top: it grows to `[3, 4, 2]`, then `MUL` collapses the top two into `8`, then `ADD` collapses again into the final `11`, left alone on the [[stack]] as the result. The instruction *order* encodes the precedence — `MUL` is emitted before `ADD` so it consumes `4` and `2` first — which is why the example is non-degenerate: a flat `3 + 4` would never exercise the ordering that makes the [[stack]] discipline matter. The same computation on a **register-based** VM is shorter — `MUL R1, 4, 2` then `ADD R0, 3, R1` — two instructions instead of five, illustrating the compactness-versus-instruction-count trade between the two operand models.

## Prerequisites

- [[interpreter]]
- [[stack]]

## Sources

- crafting-interpreters
- lua-5.0-impl
