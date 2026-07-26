---
id: boot-process
title: Boot Process
summary: The boot process is the chain of steps that carries a machine from the instant power is applied to a fully running system.
type: concept
tags: [os/kernel]
prereqs: [kernel]
sources:
  - "Linux internals study guide (etc/linux-internals-complete.html) — §1 'Boot: from power button to login prompt' (the five steps, the chicken-and-egg of GRUB, initrd/initramfs), 'The relay race — each layer disappears', and 'The complete boot chain'"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Boot Process

## Summary

The **boot process** is the chain of steps that carries a machine from the instant
power is applied to a fully running system. Its defining shape is a **relay race**: a
sequence of separate programs, each of which does just enough to load and hand control
to the next, then is discarded — *each runner carries the baton just far enough to hand
it off.* The puzzle it solves is that at power-on the machine knows **nothing** — no
operating system, no drivers, no notion of files — yet it must end up with the
[[kernel]] (the resident, privileged program that brokers all access to hardware)
loaded and running. No single early program is capable of the whole job, so the work is
split into rungs of a disposable ladder, each more capable than the one before. The
chain is: (1) **firmware** baked into the motherboard runs first, checks the hardware,
and finds a startup program on disk; (2) that program — the **bootloader** — copies the
[[kernel]] and a small emergency filesystem into memory and jumps into the [[kernel]];
(3) the [[kernel]] takes over for good, sets up the machine's hardware, and reaches the
real disk; (4) the [[kernel]] launches the first ordinary program, which then starts
every other service. Each rung exists only because the next one cannot start itself —
that "why" is the heart of the concept.

## Grounded explanation

### What the concept *is*: a relay of disposable loaders

A running computer is a [[kernel]] sitting in memory with ordinary programs on top of
it. But at the instant you press the power button, none of that exists: memory holds
nothing useful, no program is running, and the machine has no idea what an operating
system even is. The boot process is the bridge across that gap — the ordered sequence
of steps that turns a powered-but-empty machine into one with the [[kernel]] resident
and programs running.

The reason it must be a *sequence of separate programs* rather than one is a stack of
chicken-and-egg problems, and seeing those problems is the whole point. The single
defining structure is a **relay race**: program A runs, does the one thing it is capable
of, loads program B into memory, jumps to B, and is then never executed again; B does
its one thing, loads C, jumps to C, and disappears; and so on until the [[kernel]] —
the last runner — takes the baton and, unlike the others, keeps running for the whole
life of the machine. The earlier runners are a **disposable ladder**: each rung exists
only to reach the next, and the memory it occupied is reclaimed afterward. At no point
does the hardware "know" it is booting an operating system — the processor (the chip
that executes one instruction after another, forever) simply runs whatever instruction
sits at the address it is told to look at next.

### The WHY of each rung: why no earlier program can do the next one's job

Walk down the ladder and ask, at each rung, *why can't the thing before it just do this
itself?* That question is the explanation.

**Rung 1 — firmware, because the processor is dumb.** When power flows, the processor
does the only thing it can do: fetch the instruction at the address held in its
*instruction pointer* (the register naming the next instruction to run) and execute it.
At power-on that pointer holds a single **hardwired, fixed address** — call it the
**reset vector**, the always-the-same place the processor begins after a reset. The
machine's builder physically wires a small flash-memory chip to answer at that address,
and the program on that chip is the **firmware** (modern PCs call its standard *UEFI*;
the older one was *BIOS* — these are incidental names). So firmware runs *first* not by
choice but because someone put code where the processor is forced to look. The firmware
does just two jobs: a **POST** (power-on self-test — a quick check that the memory,
disks, keyboard, and display are present and working) and then a search of the attached
disks for a startup program to load. *Why does it stop there?* Because firmware lives in
a tiny fixed chip; it has no idea how Linux is laid out and cannot contain the whole
operating system. It is just capable enough to find and launch the next runner.

**Rung 2 — the bootloader, because the [[kernel]] cannot load itself.** The [[kernel]]
is an ordinary file on the disk. To read a file you need filesystem support — the code
that understands how files are arranged on the disk — and *that code is part of the
[[kernel]]*. So you cannot use the [[kernel]] to load the [[kernel]]: the thing that
reads files is the very thing not yet running. This is the central chicken-and-egg of
booting, and it is why a separate **bootloader** exists (on Linux it is usually a
program named *GRUB* — an incidental product name). The bootloader carries its *own*
tiny, just-enough filesystem reader so it can find the [[kernel]] file on disk without
the [[kernel]]'s help. It does three things and then vanishes: it copies the [[kernel]]
image into memory, copies alongside it a small emergency filesystem (described next),
and jumps into the [[kernel]] — after which the bootloader's code never runs again.

**Rung 3 — the [[kernel]], and the initramfs, because the drivers live on the disk the
[[kernel]] can't yet reach.** Once the bootloader jumps into it, the [[kernel]] is in
charge for good. It decompresses itself into a fixed region of memory (it ships
compressed to save space) and begins initializing the machine: it sets up the memory
manager, detects the hardware, and loads its **device drivers** — the per-device
translators that turn the [[kernel]]'s generic requests into the exact commands a
*specific* piece of hardware understands. But now a third chicken-and-egg appears. To
read the real disk that holds the [[kernel]]'s files, the [[kernel]] needs the driver
for *that particular* disk controller — and the driver is itself a file *on that very
disk*. The [[kernel]] cannot read the disk to get the driver it needs in order to read
the disk. The solution the bootloader supplied is the **initramfs** (initial RAM
filesystem): a small, complete root filesystem that the bootloader loaded straight into
memory beside the [[kernel]], pre-stocked with *just enough* drivers to reach the real
disk. The [[kernel]] mounts this in-memory filesystem first — needing no disk at all —
uses the drivers inside it to reach and mount the real disk, and then **pivots**:
switches its idea of the root filesystem from the throwaway in-memory one to the real
on-disk one. The initramfs has done its one job and is discarded — another rung of the
ladder, falling away.

**Rung 4 — the first program, because the [[kernel]] is not a program that runs on its
own.** The [[kernel]] is *reactive*: it has no loop of its own and only executes when
something enters it. So a running system needs at least one ordinary program for the
[[kernel]] to serve and to keep things moving. As its final boot step, the [[kernel]]
starts that first program (conventionally called **init**, and assigned process
identifier **1** — "PID 1"). This first program is the ancestor of every other ordinary
program; it reads its configuration and launches all the system's services — networking,
logging, the login prompt, and the rest. The mechanics of *how* the [[kernel]] creates
this first program and how it parents all the others is its own subject and is left for
a separate node; here it is enough that the last act of booting is to hand the system
over to userspace, after which the boot process is finished and the [[kernel]] settles
into its permanent reactive role.

### Why a *ladder* of growing capability, not one big program

Notice the pattern across the rungs: each one builds a *more capable* version of what
the previous one had and throws the previous away. Firmware can barely find a disk; the
bootloader brings a tiny filesystem reader; the [[kernel]] brings full-blown drivers and
a real filesystem. The firmware's crude disk reader is forgotten the moment the
bootloader's better one loads; the bootloader's reader is forgotten the moment the
[[kernel]]'s own drivers take over; the initramfs is forgotten the moment the real root
is mounted. This is *why* the boot process is a relay and not a monolith: you cannot put
the full, driver-rich [[kernel]] at the reset vector (it is far too large for the fixed
firmware chip, and it could not read itself in anyway), so the system bootstraps itself
upward through ever-more-capable disposable loaders until the one permanent runner, the
[[kernel]], is in place.

### Worked instance: power button to login prompt

Trace one concrete boot of a Linux laptop, so every step has a real cause:

1. **Power on.** Current reaches the processor. Its instruction pointer holds the
   hardwired reset vector, so it begins executing the firmware chip wired to that
   address — not by choice, but because that is the only address it knows.
2. **Firmware + POST.** The firmware runs its power-on self-test (RAM present? disk
   present? keyboard? display?), initializes basic hardware, then scans the disks and
   finds a startup program — the bootloader — in a known spot, loads it into memory, and
   jumps to it. The firmware's job is now over.
3. **Bootloader.** The bootloader uses its own small filesystem reader to locate two
   files on disk: the [[kernel]] image and the initramfs. It copies both into memory and
   jumps into the [[kernel]]. The bootloader never runs again.
4. **[[Kernel]] init.** The [[kernel]] decompresses itself, sets up memory management,
   detects hardware, and loads drivers. It mounts the initramfs (already in memory) as a
   temporary root, uses the drivers inside it to reach the laptop's real disk, mounts the
   real root filesystem, and pivots onto it. The initramfs is discarded.
5. **First program (PID 1).** As its last boot step the [[kernel]] launches the first
   userspace program, init (PID 1), and from here on the [[kernel]] only runs when
   entered. PID 1 starts the system's services, among them a login service.
6. **Login prompt.** The login service prints a prompt and waits for input. The blinking
   cursor you see is that program, sitting idle, waiting for you to type. The machine
   that knew nothing a few seconds ago is now a fully running system — the relay is
   complete, and only the last runner, the [[kernel]], is still on the track.

## Prerequisites

- [[kernel]]

## Sources

- Linux internals study guide (`etc/linux-internals-complete.html`) — §1 "Boot: from power button to login prompt": the five-step walkthrough (firmware and POST, firmware loads the bootloader, the kernel takes over, PID 1 starts, the login prompt), the "CPU is dumb" / hardwired fixed-address framing, the GRUB chicken-and-egg passage, and the initrd/initramfs description; "The relay race — each layer disappears" (each runner carries the baton just far enough; the disposable-ladder framing); and "The complete boot chain" (POWER ON → firmware → bootloader → kernel → PID 1 → login).
