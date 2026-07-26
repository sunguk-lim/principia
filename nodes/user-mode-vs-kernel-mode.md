---
id: user-mode-vs-kernel-mode
title: User Mode vs Kernel Mode
summary: A CPU executes instructions in one of two privilege levels — a piece of internal state, set in the processor's own circuitry, that decides how much a running instruction is…
type: concept
tags: [os/kernel]
prereqs: [kernel, interrupt]
sources: ["linux-internals-complete.html — 'Ring 0 vs Ring 3', 'The 4-floor building', 'Ring 3 vs Ring 0 — what changes'"]
status: explained
created: 2026-06-23
updated: 2026-06-29
---

# User Mode vs Kernel Mode

## Summary

A CPU executes instructions in one of two **privilege levels** — a piece of internal
state, set in the processor's own circuitry, that decides how much a running instruction
is allowed to do. **Kernel mode** (on x86 chips, called *Ring 0*) is the fully privileged
level: code there may run any instruction and touch any memory or hardware. This is where
the [[kernel]] runs. **User mode** (*Ring 3*) is the restricted level: ordinary application
code — your shell, a Python script, a browser — runs here, blocked by the hardware from
privileged instructions, from touching hardware directly, and from reading the memory of
the [[kernel]] or of other programs. The whole point of this split is *protection*: because
the boundary is enforced by the CPU itself, a buggy or malicious user program **physically
cannot** corrupt the [[kernel]] or another program. It can only ask the [[kernel]] to act
on its behalf, through narrow, controlled entry points.

## Grounded explanation

### The defining idea: a privilege bit the hardware obeys

The concept here is not the [[kernel]] and not any single instruction. It is the
**hardware-enforced privilege boundary** itself — the fact that the CPU carries a small
piece of state saying "the code running right now is trusted" or "the code running right
now is untrusted," and that the processor *physically refuses* dangerous operations when
the state says "untrusted."

Think of a government building with floors of increasing clearance, reachable only through
one guarded elevator:

- **Ring 0 — the vault.** Full hardware access. Only the [[kernel]] runs here. One mistake
  can crash the whole machine.
- **Ring 3 — the lobby.** Very restricted. *Every* ordinary program runs here.

(x86 chips actually define four rings, 0 through 3; rings 1 and 2 were meant for device
drivers but real systems like Linux leave them empty and use only 0 and 3. So in practice
the world is exactly two-valued: kernel mode or user mode.)

The crucial word is *enforced*. The privilege level is not a convention that software
agrees to honor — it is circuitry inside the CPU, present on every x86 chip since 1985.
Software running in Ring 3 **cannot lie about which ring it is in**, and it cannot promote
itself to Ring 0. The hardware decides.

### Why we need it: protection as a physical fact

Without this boundary, every program would have the keys to the whole machine. A single
bug in a text editor could overwrite the [[kernel]]'s code; a malicious program could read
your password out of another program's memory; a careless loop could turn off the timer
the system uses to switch between programs and freeze everything.

The two-level split removes those possibilities not by asking programs to behave, but by
making misbehavior *impossible to execute*. The justification is exactly this: a guarantee
that depends on every program being well-written is no guarantee at all, but a guarantee
wired into the CPU holds even against code that is actively hostile. Isolation becomes a
property of the silicon rather than a hope about the software.

### What each mode can and cannot do

The boundary is defined by drawing a line through the CPU's instruction set and its memory.
In **user mode (Ring 3)** a program *can*:

- read and write its **own** memory;
- run ordinary instructions — arithmetic, comparisons, branches, loops;
- make a **system call**, which is the one sanctioned way to ask for more.

In user mode a program *cannot*:

- talk to hardware directly (the instructions that read/write device ports are privileged);
- change the tables that map memory, or switch to another program's memory;
- turn the CPU's interrupts off (which would let it monopolize the machine);
- read another program's memory, or even *read* the [[kernel]]'s memory.

In **kernel mode (Ring 0)** code can do *everything* user mode can, **plus** all the
forbidden operations above: run privileged instructions, remap memory, enable/disable
interrupts, reach any address on the system, and drive hardware directly. That is why the
[[kernel]] — the one program trusted to manage all hardware for everyone — is the only
thing that runs there.

### The one non-obvious step: crossing the line is not free

If user mode can do so little, how does any real work — opening a file, sending a network
packet, getting more memory — ever happen? The answer is the part that looks like magic
until you see it: **a program does not promote itself; it asks, and the hardware switches
modes for it through a fixed door.**

There are exactly three ways control moves from user mode into kernel mode, and all of them
hand control to the [[kernel]] at an address the [[kernel]] chose in advance:

1. a **system call** — the program deliberately executes the special "enter the kernel"
   instruction, the elevator up;
2. an **[[interrupt]]** — a hardware device (a disk finishing, a key pressed) signals the CPU;
3. a **fault** — the running instruction did something illegal, so the CPU traps.

In every case the CPU flips the privilege level to Ring 0 and jumps to a handler that is
part of the [[kernel]]. The user program never gets to *choose* what runs in Ring 0; it can
only trigger one of these transitions, and the [[kernel]] decides what to do. This is why
the boundary stays safe even though it is crossed millions of times a second: the door is
fixed, and only the [[kernel]] is on the other side of it.

### A worked instance: a program reaches past the line

Let us trace one concrete attempt, deriving each step from the last. A small C program tries
to read a byte directly out of [[kernel]] memory — an address it has no business touching:

```c
int main() {
    char *k = (char *)0xffffffff81000000UL;  // an address inside kernel memory
    printf("Kernel byte: %c\n", *k);          // dereference it
    return 0;
}
```

Step by step, watching the privilege level:

1. **The program runs in Ring 3.** It was launched as an ordinary process, so the CPU's
   privilege state says *user mode* the entire time it executes `main`.
2. **It executes the dereference `*k`.** This is a normal memory-read instruction — nothing
   special about the instruction itself. But the address `0xffffffff81000000` lies in the
   region the [[kernel]] has marked as Ring-0-only.
3. **The CPU checks privilege before completing the read.** It compares the current level
   (Ring 3) against the level required for that address (Ring 0). Ring 3 is *not* allowed.
   So the read never happens.
4. **The CPU raises a fault.** Instead of returning a byte, the hardware traps: it switches
   the privilege level to Ring 0 and jumps to the [[kernel]]'s fault handler — transition
   type 3 from the list above.
5. **The [[kernel]], now in Ring 0, decides the program's fate.** It sees that a user-mode
   process tried to read an address it may not read. It does not crash the machine; it
   simply terminates that one process (on Linux, delivering the signal `SIGSEGV` — a
   "segmentation fault").
6. **The rest of the system is untouched.** The [[kernel]]'s memory was never read, other
   programs were never disturbed, and the machine keeps running. The attempt failed safely.

The illustrative case here is the *forbidden* branch — the program hit the line and was
stopped. Now contrast the *allowed* branch with the same shape, so the mechanism is shown
end to end. Suppose instead the program had wanted to read a byte from a **file**. It cannot
touch the disk directly (a privileged hardware operation), so it makes a **system call**:
it executes the "enter the kernel" instruction (transition type 1), the CPU switches to Ring
0, the [[kernel]] reads the disk on the program's behalf, copies the byte into the program's
*own* memory, switches back to Ring 3, and returns. Same boundary, same door — but this time
the program *asked* through the sanctioned entry point instead of reaching across the line,
so it gets its byte instead of a fault.

The two branches are the whole concept in miniature: **direct** privileged action from user
mode is physically refused; the **same action requested** through a controlled transition is
performed by the [[kernel]] and handed back. The line is never erased — it is only ever
crossed through the door.

## Prerequisites

- [[kernel]]

## Sources

- `linux-internals-complete.html` — sections "The hardware
  mechanism — Ring 0 vs Ring 3," "The 4-floor building," and "Ring 3 vs Ring 0 — what
  changes when you cross over?" (building analogy, the allowed/forbidden lists, and the
  Ring-3-reads-kernel-memory experiment that segfaults).
