---
id: jit-vs-aot-compilation
title: JIT vs AOT Compilation
summary: A cuda-kernel is written by a human, but the GPU cannot run that source text — it can only run machine code for the exact chip in front of it.
type: concept
tags: [gpu]
prereqs: [cuda-kernel, ptx, cubin]
sources: ['etc/linux-internals-complete.html — Cubin lifecycle cases 1-5 (library AOT, custom-extension AOT, torch.compile JIT, PTX forward-compat)']
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# JIT vs AOT Compilation

## Summary

A [[cuda-kernel]] is written by a human, but the GPU cannot run that source text — it can only
run *machine code* for the exact chip in front of it. Somewhere between writing the kernel and the
GPU executing it, a compiler must turn the source into that machine code. **JIT vs AOT is the axis
of *when* that translation happens.** **AOT** (Ahead-Of-Time) means the compile happens at *build /
ship time*: the program you download already contains finished machine code, so it starts instantly
and never pauses to compile — but whoever built it had to guess, in advance, every GPU and every
situation the code might face. **JIT** (Just-In-Time) means the compile is deferred to *runtime*,
typically the *first time* the kernel actually runs: the program ships as source or a half-way
intermediate form and is compiled on the spot for the GPU that is genuinely present and the inputs
genuinely seen. JIT pays a one-time *compile pause* on that first call (then usually caches the
result to disk so every later run is fast), and buys, in return, the freedom to target the exact
hardware and specialize to the actual data. The two are not rivals to choose between once and for
all; a single program routinely uses both — shipping finished machine code for the cases it could
anticipate, and carrying a compile-on-demand fallback for the cases it could not.

## Grounded explanation

**What the concept is — the gap a compiler must close.** Recall from [[cuda-kernel]] that a kernel
is a function written in source (CUDA C++, marked `__global__`) describing what one thread does,
plus a launch that says how many threads to spawn. That source is text. The streaming
multiprocessors on the GPU do not execute text; they execute *machine code* — a stream of bytes
encoding the exact instructions for one specific GPU architecture (one generation of chip design).
Crucially, machine code is **not portable across architectures**: code built for one generation of
GPU will not run on a different generation, the same way a program built for one kind of processor
will not run on an unrelated one. So between the kernel source a person wrote and the SMs that run
it, *something must compile the source down to machine code for the architecture actually present*.
JIT vs AOT is the single question: **does that compile happen before the program is shipped, or
after it has started running?** Everything else in this node is the consequence of that one choice
of timing.

**AOT — compile at build time, ship finished machine code.** In the Ahead-Of-Time arrangement, the
person who builds the program runs the compiler on their own machine, *before* anyone downloads it.
The compiler turns each [[cuda-kernel]] into machine code and the program that ships already
contains that machine code. When the user runs it, there is nothing left to compile: the launch
hands the GPU code that is already there. The decisive consequences:

- **Fast, predictable startup, no warm-up.** Because the machine code already exists, the very
  first launch is as fast as the thousandth. There is no compile pause anywhere — the cost was paid
  once, long ago, by the builder, and never reappears for the user.
- **You must pre-target the architectures.** The builder cannot compile for a GPU they did not
  anticipate. They must decide, in advance, *which* GPU generations to support, and run the compiler
  once per generation. A program built only for last year's chips simply has no machine code for a
  chip released next year — there is nothing to run. This is why the same kernel is often built many
  times over, once per supported architecture, and all of those finished copies (each a [[cubin]] —
  machine code for exactly one GPU generation) are bundled together and shipped together (so the
  program can pick the matching one for whatever GPU it finds). That bundle can be enormous — a
  single vendor math library can carry hundreds of megabytes of machine code purely because it
  pre-built every kernel for every architecture it promises to support.
- **It cannot specialize to runtime facts.** Because the compile happened before the program ran,
  the compiler never saw the actual input sizes, the actual constants, or the actual GPU. It had to
  produce code that works for *any* of them, which means it cannot bake in a value it does not yet
  know. A kernel that could have been faster *if* the compiler had known "this dimension is always
  4096" cannot get that speedup under AOT, because at build time nobody knew it would be 4096.

**JIT — compile at runtime, on first use.** In the Just-In-Time arrangement, the program ships
*without* finished machine code (or with only a partial, not-yet-final form of it). The compile is
deferred until the program is already running, and triggered the **first time** a given
[[cuda-kernel]] is actually needed. At that moment the system knows things the AOT builder never
could: it can ask the GPU sitting in the machine "which architecture are you?" and compile for
*exactly* that chip, and it can read the *actual* input shapes and constants and bake them straight
into the kernel as fixed numbers. The decisive consequences mirror AOT's, inverted:

- **A one-time compile pause on the first call.** The first time the kernel runs, the program stops
  and compiles — a visible delay, often seconds, while source becomes machine code. This is the
  price of deferring. Every kernel that is JIT-compiled has a "slow first call, fast afterward"
  signature; if a workload is mysteriously slow only on its very first iteration and then snaps to
  full speed, that first-call cost is almost always a JIT compile happening behind the scenes.
- **A caching story makes the pause one-time, not per-call.** A compiler that recompiled on *every*
  call would be unusable. So the JIT writes its finished machine code to disk, filed under a key
  built from what it compiled *for* — the kernel's source, the specialization constants, and the GPU
  architecture. The next time the same kernel is needed with the same key, the system finds the
  cached machine code on disk and loads it instead of recompiling. So the pause is paid once *per
  distinct situation*, not once per launch — and across separate runs of the program, because the
  cache lives on disk and outlives the process.
- **The cache key is also the specialization story.** Because the key includes the specialization
  constants, *changing one of those facts is a different key*, which misses the cache and triggers a
  fresh compile. This is the flip side of JIT's adaptivity: a kernel specialized to one input shape
  is genuinely a different piece of machine code from the same kernel specialized to another shape,
  so feeding it a new shape it has never seen makes it pay the compile pause again for that shape.
  The adaptivity (specialize to the exact shape) and the recompile cost (a new shape is a new
  compile) are two faces of one mechanism.

**The why — the tradeoff stated plainly.** Neither timing is better in the abstract; they trade the
*same* compile cost for opposite virtues. AOT moves the cost to build time, so it buys **predictable
behavior and zero warm-up** at the price of **rigidity** — you must anticipate every target and
every situation in advance, and you can never specialize to a fact you did not know when you built.
JIT keeps the cost at runtime, so it buys **flexibility and self-optimization** — it targets the GPU
that is genuinely present and specializes to the data genuinely seen — at the price of a **first-call
pause and a caching story** you must manage. The deep reason both exist is that "which GPU?" and
"what shape?" are answerable either early (guess them at build time, pay nothing later, accept being
wrong sometimes) or late (read them at runtime, pay a pause once, always be right).

**They coexist — AOT with a JIT fallback.** The cleanest demonstration that this is an axis, not a
binary choice, is that one shipped program commonly does *both at once*. A program can pre-build
finished machine code for the GPU generations it expects (AOT, instant for those) **and** carry
along a portable, architecture-independent intermediate form ([[ptx]]) of the very same kernels as a fallback.
When such a program lands on a GPU generation the builder *did* anticipate, it runs the matching
pre-built machine code immediately — pure AOT, no pause. When it lands on a generation the builder
did *not* anticipate — a chip released after the program shipped — it finds no matching pre-built
code, falls back to the [[ptx]], and **JIT-compiles that into fresh machine code
for the new chip on the first launch**, caching the result so later runs skip it. This is how a
binary built today can still run on a GPU released years from now: AOT covers the known cases for
speed, and a JIT fallback covers the unknown future for survival.

**Worked instance — three kernels, three timings, in one workload.** Picture a single program that
calls three different [[cuda-kernel]]s, and watch *when* each one's machine code comes into being:

- **(a) A precompiled library kernel — pure AOT, zero runtime compile.** The program calls a
  standard matrix-multiply provided by a vendor library. That kernel was compiled to machine code by
  the vendor at *their* build time, months ago, for every architecture they support, and shipped as
  finished bytes inside the library file. At runtime the library merely *selects* which precompiled
  copy matches the present GPU and the given shape and hands it to the launch — selection happens,
  *compilation does not*. The first call is exactly as fast as every later call: there is no pause,
  because there is nothing left to compile.

- **(b) A `torch.compile`d kernel — JIT on the first forward pass, then disk-cached.** The program
  also runs a model wrapped so its operations are *fused* into a custom [[cuda-kernel]] generated on
  the fly. The *first* forward pass triggers the JIT: the system traces the operations, emits kernel
  source, and compiles it down to machine code for the present GPU — the multi-second pause you can
  watch on that first iteration. The finished machine code is then written to an on-disk cache,
  filed under the kernel's source, its shape constants, and the GPU architecture. The *second*
  forward pass with the same shapes finds that cache entry and loads it: no pause, full speed. Feed
  the model a genuinely new input shape later, though, and that new shape is a new cache key — a
  miss — so it pays one more compile pause to produce a kernel specialized to *that* shape. This is
  JIT showing both faces in one workload: a first-call cost, erased by caching, re-incurred only
  when a truly new situation appears.

- **(c) A kernel shipped as portable intermediate only — JIT'd by the driver on first launch.** The
  third [[cuda-kernel]] was *not* pre-built for the user's particular GPU generation — no matching
  [[cubin]] exists for this chip, only the portable, architecture-independent [[ptx]] rode along.
  The very first time the launch tries to run it, the system notices there is no machine code for
  this chip, takes the [[ptx]], and compiles it into fresh machine code for *this exact* architecture
  right then. It caches that result on disk, so
  the cost is paid once at process startup, not once per launch, and every subsequent run of the
  program reuses it.

Three kernels, three answers to the single question this node is about — *when did the source become
machine code?* For (a), before the program ever shipped. For (b), at the first call, and again at
each genuinely new shape. For (c), at the first launch on this particular chip. The kernels are
identical in kind — each is a function-plus-launch from [[cuda-kernel]] — and differ only in the
*timing* of their compile. That timing, and the tradeoff it forces between predictable-but-rigid and
flexible-but-warming-up, is the whole of JIT vs AOT.

## Prerequisites

- [[cuda-kernel]]
- [[ptx]]
- [[cubin]]

## Sources

- `etc/linux-internals-complete.html` — "Cubin lifecycle — when does compilation actually happen?"
  (the AOT vs runtime-JIT vs library-shipped split, and the startup-cost / cache-invalidation /
  first-call-tax framing); "Case 1 — Library kernels: precompiled, no work at runtime" (selection
  at runtime, compilation not); "Case 2 — Custom CUDA extensions: AOT, baked into the wheel" (built
  per target architecture; the PTX-JIT fallback on an unanticipated architecture, cached, once per
  process startup); "Case 3 — torch.compile: JIT-compiled on first call, disk-cached" (the
  multi-second first-call pause; on-disk cache keyed by source + shape constants + architecture;
  new shape → recompile); and the forward-compatibility note that a binary carrying the portable
  intermediate form can JIT onto GPU architectures released years later.
