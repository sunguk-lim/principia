---
id: cuda-kernel
title: CUDA Kernel
summary: A CUDA kernel is a function you write once but that every thread of a GPU launch executes in parallel.
type: concept
tags: [gpu]
prereqs: [cuda-thread-hierarchy, streaming-multiprocessor]
sources:
  - etc/linux-internals-complete.html — "The launcher and the kernel function", "Function qualifiers", "The loop disappears"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# CUDA Kernel

## Summary

A CUDA kernel is a function you write **once** but that **every** thread of a GPU launch
executes **in parallel**. It comes in two coupled halves. The first is the *kernel function*:
a piece of GPU code (in CUDA C++, marked with the qualifier `__global__`) that describes what
**one** thread does, written in terms of that thread's index from the [[cuda-thread-hierarchy]].
The second is the *launch*: a line of CPU code, written `kernel<<<grid, block>>>(args)`, that
says **how many** threads to spawn — a grid of so many blocks, each block of so many threads —
and starts them all running that one function. The mental shift the kernel forces is this: you
do **not** write a loop over your data. You write the body for a *single* element, and you launch
*one thread per element*. Because each thread can compute its own index, each picks out its own
element, so the loop you would have written on a CPU simply disappears.

## Grounded explanation

**What the concept is.** On an ordinary CPU, to add two arrays of length `n` you write a loop:
one worker steps through `i = 0, 1, 2, …, n-1`, and at each step computes `out[i] = a[i] + b[i]`.
The loop is *explicit*: one worker, `n` iterations, done in sequence. A CUDA kernel replaces this
with a different arrangement entirely. From the [[cuda-thread-hierarchy]] we already know a GPU
launch produces a huge collection of threads, organized into blocks, organized into a grid, and
that **each thread carries an index it can read to know which slot in that collection it is**.
The kernel exploits exactly this: instead of one worker looping over all `n` elements, you spawn
`n` workers and give each one a single element to handle, selected by its own index. The kernel
*is* the pairing of (a) the function describing one worker's job and (b) the launch that says how
many workers to create.

**The two halves, named.** A CUDA program for the GPU has two pieces of code that run on two
different chips, and the kernel concept spans both:

- The **kernel function** is the GPU code — the body that runs on each thread. In CUDA C++ it is
  marked with the qualifier `__global__`, which tells the compiler "this function is *called from
  the CPU but runs on the GPU*." (Its sibling qualifier `__device__` marks a helper that is both
  called from and runs on the GPU; `__host__` marks ordinary CPU code, the default.) The crucial
  property: the kernel function is written for *one* thread. It does not contain a loop over the
  data, and it does not even know how many threads were launched alongside it — it knows only its
  own index.
- The **launch** is the CPU code that decides how many threads to create and starts them. The
  syntax is `kernel<<<grid, block>>>(args)`, where `block` is how many threads go in each block and
  `grid` is how many blocks make up the launch — exactly the two-level structure of the
  [[cuda-thread-hierarchy]]. `args` are the ordinary function arguments (pointers to the data, the
  length, and so on). All decisions about *distribution* — how many blocks, how many threads each —
  live here in the launch, never inside the kernel function.

**Why split it this way (the key insight).** The split cleanly separates **what one unit of work
is** from **how much of it to run**. The kernel function fixes the *what*: "given my element,
compute this." The launch fixes the *how much*: "make this many threads." This is powerful for two
reasons. First, you can change the amount of parallelism — run the same computation over a
thousand elements or a billion — purely by changing the launch numbers, never touching the kernel
function. Tuning a kernel usually means tuning the launch parameters, not rewriting the body.
Second, it matches the hardware. A GPU is built from many independent processing units (each is
called a [[streaming-multiprocessor]], or SM). The launch hands the GPU a grid of blocks, and the
hardware distributes those blocks across its SMs to run concurrently. Because the unit of
distribution is the *block*, and the launch is what produces blocks, the launch is precisely the
knob that controls how work spreads over the chip — while the kernel function stays a pure
description of one thread's arithmetic.

**The "loop disappears."** This is the single most disorienting and most important thing about
writing a kernel, so it deserves to be stated directly. On the CPU the iteration is written by
hand: `for (i = 0; i < n; i++) out[i] = a[i] + b[i];`. In the kernel function there is **no loop**.
The line that used to be `for (i = 0; …)` becomes a single assignment that *computes this thread's
own* `i` from its index, followed by the body run once. Where the CPU had "one worker, `n`
iterations," the GPU has "`n` workers, one iteration each." The grid of threads has *become* the
loop — the iteration count `n` now lives in the launch's grid size, and the loop variable `i` is
now each thread's index. You are no longer writing a sequence of operations; you are describing
what one thread does and then launching a vast number of them.

**Worked instance — vector add over 1,000,000 elements.** Suppose `a`, `b`, and `c` are arrays of
`n = 1,000,000` floating-point numbers in GPU memory, and we want `c[i] = a[i] + b[i]` for every
`i`. The kernel function (GPU code, marked `__global__`, returning nothing) is:

```
__global__ void add(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}
```

Read it as one thread's script. The first line is the standard 1D index computation from the
[[cuda-thread-hierarchy]]: `blockIdx.x` is which block this thread is in, `blockDim.x` is how many
threads per block, and `threadIdx.x` is this thread's position inside its block — so
`blockIdx.x * blockDim.x + threadIdx.x` is this thread's unique position across the whole grid.
That single number `i` is the element this thread owns. The second line does the work for *that one*
element. There is no loop in sight; the body runs exactly once per thread.

Now the launch (CPU code). We pick `256` threads per block — a common, hardware-friendly block
size. How many blocks do we need to cover 1,000,000 elements? We need at least
`1,000,000 / 256 = 3906.25` blocks, and since we cannot launch a fraction of a block we round
**up** to `3907` blocks. The launch is therefore:

```
add<<<3907, 256>>>(a, b, c, n);
```

This spawns `3907 × 256 = 1,000,192` threads, each running the `add` function on its own `i`. Note
the count: `1,000,192` threads for `1,000,000` elements — we created **192 extra** threads, because
`3907` blocks of `256` slightly overshoots the data. This is exactly why the kernel function has
the line `if (i < n)`. The `192` threads with indices `1,000,000` through `1,000,191` would, without
the guard, write past the end of the arrays — out of bounds, corrupting memory. The guard makes
those overshoot threads compute their `i`, find `i < n` is false, and quietly do nothing. The other
`1,000,000` threads each handle one valid element. Together, one launch of one tiny function
replaces a million-iteration CPU loop, and the GPU runs those million additions in parallel across
its SMs instead of one after another. The `if (i < n)` guard is not a special case to memorize — it
is the general consequence of the grid size being rounded up to a whole number of blocks, so the
launch almost never lands on an exact multiple of the data length.

## Prerequisites

- [[cuda-thread-hierarchy]]
- [[streaming-multiprocessor]]

## Sources

- `etc/linux-internals-complete.html` — "The launcher and the kernel function — two pieces of code,
  two devices", "Function qualifiers — where does this code run?", "Thread indexing", and "The
  'loop disappears' — central insight for kernel writing".
