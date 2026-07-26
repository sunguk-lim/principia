---
id: ptx
title: PTX (Parallel Thread Execution)
summary: PTX (Parallel Thread Execution) is the intermediate, virtual instruction set that a cuda-kernel's GPU code is first compiled into, on its way from high-level source to the actual…
type: concept
tags: [gpu]
prereqs: [cuda-kernel]
sources:
  - etc/linux-internals-complete.html — "nvcc, PTX, SASS — the compilation pipeline", "Cubin lifecycle", "Axis 3 — PTX forward compatibility", glossary "PTX"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# PTX (Parallel Thread Execution)

## Summary

PTX (Parallel Thread Execution) is the **intermediate, virtual instruction set** that a
[[cuda-kernel]]'s GPU code is first compiled into, on its way from high-level source to the
actual machine code a GPU executes. It is an assembly-like text representation, but it is not
the real machine code of any particular chip: it targets an *idealized* GPU rather than a
specific one. That is what "virtual" means here — PTX is portable across GPU generations
because it is not tied to the exact silicon. Its defining payoff is **forward compatibility**:
because PTX is architecture-independent, the GPU driver can translate it — at the moment the
program loads, on whatever GPU happens to be present — into that chip's real machine code,
*including GPUs that did not exist when the program was built*. PTX is therefore the stable
"bytecode" layer that lets a compiled CUDA program keep running on new hardware without being
recompiled from source.

## Grounded explanation

**What the concept is.** A [[cuda-kernel]] is the GPU function you write once and launch across
many threads. To actually run, that function must end up as binary machine instructions the
GPU's processing units can execute. But "the GPU's instructions" is not a single fixed target:
NVIDIA redesigns the instruction set with nearly every hardware generation, so the real machine
code for one generation is not the real machine code for the next. PTX is the layer that absorbs
this churn. When the CUDA compiler (NVIDIA's `nvcc`) processes a kernel, it does **not** go
straight to a chip's machine code. It first lowers the kernel into PTX — an architecture-*neutral*
intermediate form — and only then, in a second step, turns that PTX into the machine code of one
or more specific GPU generations. PTX is precisely this middle representation: the concept *is*
the portable, virtual instruction set that sits between the source you wrote and the silicon you
run on.

**Defining the two terms it rests on.** Two pieces of vocabulary carry the whole idea, so define
them before using them.

An **instruction set architecture (ISA)** is the contract describing what instructions a processor
understands — add, load, store, branch, and so on — and how they are encoded. A *virtual* ISA is
an instruction set defined for an *idealized* machine that no physical chip implements directly.
PTX is a virtual ISA: it specifies a clean, generic GPU's instructions, abstracted away from the
quirks of any real generation. Because nothing physical is committed to, PTX written for the
idealized GPU is portable — the same PTX is meaningful regardless of which actual GPU you later
run on. (The contrasting term, used in plain prose throughout, is **SASS**: the *actual*
per-generation machine code that physically runs on the GPU's processing units. SASS is real,
binary, and specific to one hardware generation; PTX is virtual, textual, and shared across
generations.)

**Just-in-time (JIT) compilation** is the act of compiling code *at the moment the program runs*,
rather than ahead of time when the program was built. The opposite, ahead-of-time compilation,
finishes all translation before shipping. PTX enables a JIT step: the GPU driver — the system
software that talks to the installed GPU — can take PTX and compile it down to that GPU's SASS at
program load time, on the machine where the program is actually running.

**Why it works (the key insight).** Put the two definitions together and forward compatibility
follows directly. Because PTX is a virtual ISA, it is not committed to any one generation's
machine code; because the driver can JIT-compile PTX, the binding from "portable PTX" to "this
specific chip's SASS" can be deferred all the way to load time, on the very machine that has the
chip. So a program can carry its kernels as PTX, and when it lands on a GPU the driver has never
seen before — a model released *after* the program was built — the driver simply JIT-compiles the
embedded PTX into fresh SASS for that new chip and runs it. The invariant being maintained is:
*the shipped artifact never has to know the exact target chip in advance.* That is the entire
reason a virtual intermediate ISA exists. GPU instruction sets change every generation, and an
architecture-independent layer **decouples shipping software from the exact hardware it will meet**.
Without PTX, a kernel compiled today could only ever run on the specific generations its machine
code was built for; with PTX embedded, it can also run on generations that did not yet exist at
build time, paying only a one-time translation cost on first launch.

**The trade-off, stated plainly.** JIT-compiling PTX is not free: the driver must do real
compilation work the first time a kernel runs on an unfamiliar chip, which makes that first launch
noticeably slow. The result is cached on disk afterward, so later runs skip the work. This is the
deliberate price of forward compatibility — a slow first launch on new hardware in exchange for
running at all on hardware that did not exist at build time. For chips that *were* known at build
time, the compiler can also emit their SASS directly ahead of time, and the driver just uses that
prebuilt machine code with no JIT cost; PTX is the fallback for everything else.

**Worked instance — one kernel, three GPUs, one of them from the future.** Suppose you compile a
[[cuda-kernel]] today, on a toolchain that knows about two GPU generations — call them generation A
and generation B. You ask `nvcc` to produce machine code for both, plus to embed the PTX. The
resulting program now bundles three things: a block of generation-A SASS, a block of generation-B
SASS, and the architecture-independent PTX. Note this is *not* a degenerate case where everything
funnels through one path — there are genuinely three distinct outcomes, and which one fires depends
on the GPU you deploy onto:

1. **Deploy on a generation-A GPU.** At load time the driver inspects the chip, finds it is
   generation A, finds a matching prebuilt SASS block, and runs it directly. No PTX is touched; no
   JIT happens. Fast start.
2. **Deploy on a generation-B GPU.** Same story with the generation-B block. Again the PTX sits
   unused, because a prebuilt match exists.
3. **Deploy on a generation-C GPU that did not exist when you built the program.** The driver
   inspects the chip, finds it is generation C, and discovers there is **no** matching prebuilt
   SASS block — neither A nor B fits. Now the embedded PTX earns its place: the driver JIT-compiles
   the PTX into fresh generation-C SASS at load time, caches that compiled result on disk, and runs
   it. The first launch is slow because of the compile; every launch afterward reuses the cached
   SASS and is fast.

Trace the difference between cases 1–2 and case 3 and you have the whole concept. In the first two,
PTX is dead weight, never executed. In the third — the case the entire mechanism exists for — PTX
is the *only* thing that lets the program run, because it is the one ingredient that was not pinned
to a known generation. The same compiled program, unchanged, runs on a chip its author never
targeted, precisely because it carried a portable virtual-ISA copy of its kernels that the driver
could lower to real machine code on demand.

## Prerequisites

- [[cuda-kernel]]

## Sources

- `etc/linux-internals-complete.html` — "nvcc, PTX, SASS — the compilation pipeline" (PTX as the
  pivot: source → PTX → SASS; PTX described as "architecture-independent intermediate text,
  human-readable, stable across years, JIT-able by the driver"); "Cubin lifecycle" (the driver
  picks a matching prebuilt machine-code block, or JIT-compiles the embedded PTX for an arch with
  no match, caching the result); "Axis 3 — PTX forward compatibility" ("a binary compiled today
  can run on a GPU released years later"); and the glossary entry for PTX ("NVIDIA's virtual ISA …
  forward-compatible across GPU architectures").
