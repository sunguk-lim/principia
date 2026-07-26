---
id: interrupt
title: Interrupt
summary: An interrupt is an electrical signal a hardware device sends to the CPU that preempts whatever the CPU is currently doing — that is, it forces the CPU to stop in the middle of the…
type: concept
tags: [os/kernel]
prereqs: [kernel]
sources:
  - "Linux internals study guide (etc/linux-internals-complete.html) — 'How the kernel runs — three entry points' (ENTRY POINT 2: Hardware interrupt), 'So what is the kernel doing at this very moment' (handling interrupts constantly; timer/keyboard/NIC/disk), 'Walkthrough — what happens when you press a key?', the IRQ glossary entry, and the interrupt-driven receive path / NAPI polling note"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Interrupt

## Summary

An **interrupt** is an electrical signal a hardware device sends to the CPU that
**preempts** whatever the CPU is currently doing — that is, it forces the CPU to stop
in the middle of the instruction stream it was running and immediately jump elsewhere.
Where it jumps is into the [[kernel]]: an interrupt is one of the [[kernel]]'s
**entry points**, the small fixed set of events that wake the otherwise-dormant
[[kernel]] and make its code execute. (The [[kernel]] has three everyday entry points —
a *system call* when a program asks for a service, an *interrupt* when hardware demands
attention, and the *timer tick*, which is itself a special interrupt that periodically
hands control back to the [[kernel]] so it can decide which process runs next.) The
purpose of the interrupt is to let devices — keyboard, network card, disk, timer —
get the [[kernel]]'s attention **asynchronously**, meaning at a moment the device
chooses rather than a moment the program planned for. The alternative, **polling**,
has the CPU repeatedly ask each device "anything yet? anything yet?" in a loop, burning
cycles on questions whose answer is almost always "no." An interrupt inverts that: the
CPU does useful work and the device taps it on the shoulder only when there is genuinely
something to handle. On an interrupt the CPU saves the state of the interrupted work,
switches into the [[kernel]]'s privileged mode, and runs the **handler** registered for
that device; because that handler must finish fast (other devices are waiting and the
interrupted program is frozen), Linux keeps it minimal — a **top half** — and defers the
heavier processing to a **bottom half** that runs a moment later. The single defining
idea: an interrupt is hardware's way of *entering the [[kernel]] on its own initiative*,
turning a passive chip that would otherwise have to keep checking into one that is
notified.

## Grounded explanation

### What the concept *is*: hardware's entry into the kernel

Recall from [[kernel]] the central, counter-intuitive fact: the [[kernel]] has **no loop
of its own**. Between events it is just code and data lying inert in memory; it executes
only when something **enters** it through one of a small, fixed set of **entry points**.
An entry point is a place the CPU is *wired* to jump to when a particular event occurs,
and the function it lands in is a **handler** — a routine the system calls *for you* when
the event fires, rather than one you call yourself.

An **interrupt** is the entry point used by **hardware**. Concretely it is a physical
electrical signal. Each device that may need attention is connected to the CPU by an
**interrupt line** — think of it as a dedicated wire. When the device wants the
[[kernel]], it raises a voltage on its line. This raised signal is also called an
**interrupt request**, abbreviated **IRQ**; the number identifying *which* line was
raised (and therefore which device) is the **IRQ number**. The word "interrupt" names
exactly what the signal does to the CPU: it interrupts.

Here is the mechanism, step by step, and it is the whole concept in miniature:

1. The CPU is partway through some program's instruction stream — adding numbers,
   copying bytes, whatever the current process is doing.
2. A device raises its IRQ line.
3. The CPU **finishes the single instruction it is on**, then — instead of fetching the
   next instruction of that program — **stops** and does something no software asked it
   to do. It **saves the interrupted work's state**: where it was in the code and the
   contents of its working registers (the CPU's tiny on-chip scratch slots), so the work
   can be resumed later exactly as if nothing had happened.
4. The CPU **switches to privileged mode** — the unrestricted hardware mode that
   [[kernel]] code is allowed to run in and ordinary programs are not.
5. The CPU **jumps to the handler registered for that IRQ number**. This handler lives
   inside the [[kernel]]. *This is the [[kernel]] waking up*: code that was inert a
   microsecond earlier is now executing.
6. The handler does its bounded piece of work and returns. The CPU **restores the saved
   state** and resumes the interrupted program at the exact instruction after the one in
   step 3 — which never noticed it was paused.

So an interrupt is not a thing the [[kernel]] *runs*; it is a thing that *happens to* the
CPU and, as a side effect, runs the [[kernel]]. The handler is often called the
**Interrupt Service Routine** (ISR) — "service routine" because it services the device
that raised the request.

### Where it sits among the kernel's entry points

[[kernel]] lists three everyday entry points; placing the interrupt among them is what
makes its role precise.

- A **system call** is the entry point used by **software**: a running program executes a
  special instruction meaning "I need a service I am not privileged to do myself," and the
  CPU jumps into the [[kernel]]. It is *synchronous* — it happens because the program
  deliberately asked, at a point the program chose.
- An **interrupt** is the entry point used by **hardware**, described above. It is
  *asynchronous* — it happens because a device decided, at a point unrelated to anything
  the running program is doing. The program that gets interrupted is usually an innocent
  bystander that simply happened to be holding the CPU.
- The **timer tick** is the third, and it is simply *a specific interrupt*: a hardware
  timer chip is wired to raise its IRQ at a fixed cadence (every few milliseconds). Its
  handler runs the **scheduler** — the part of the [[kernel]] that decides which process
  should next get the CPU. This is why the timer interrupt is the [[kernel]]'s heartbeat:
  without it, a program that never voluntarily called into the [[kernel]] could hold the
  CPU forever, because nothing else would forcibly take control back. The timer interrupt
  guarantees the [[kernel]] regains control on a schedule no program can suppress.

(There is also a fourth path — a CPU *exception* or *fault*, raised when a program does
something the CPU cannot immediately complete — which traps into a handler the very same
way; the [[kernel]] node covers it. The shared shape of all of these is: an event, a
forced jump into privileged [[kernel]] code, a bounded handler, a return.)

### The WHY: interrupts versus polling

Why build hardware this way at all? Because the alternative wastes the CPU. Suppose the
[[kernel]] wanted to know whether a key had been pressed *without* interrupts. It would
have to **poll**: run a loop that asks the keyboard controller "is there a key? is there a
key?" over and over. A human types a few characters a second; the CPU executes billions of
instructions a second. So essentially every one of those checks answers "no," and the CPU
has spent its time asking pointless questions instead of running programs. Worse, it must
poll *every* device this way, and if it polls too slowly it misses events; if it polls fast
enough not to miss them, it burns even more cycles.

The interrupt **inverts the direction of attention.** Instead of the CPU continually
checking the device, the device signals the CPU exactly once, exactly when there is
something real to handle. In between, the CPU runs useful work — or, if every process is
asleep, it executes a halt instruction and sits in a low-power state, doing literally
nothing until the next interrupt jolts it awake. This is the key insight and the reason
the mechanism exists: **an interrupt converts the question "has anything happened yet?"
from something the CPU must keep asking into something hardware answers unprompted.** The
cost — saving and restoring state on every interrupt — is paid only when an event actually
occurs, not on every fruitless check.

(Polling is not always wrong. When events arrive in a torrent — a network card receiving
millions of packets a second — one interrupt *per packet* would itself overwhelm the CPU
with save/restore overhead, so Linux flips back: it takes the first interrupt and then
polls the card in tight batches until the flood subsides. The general rule still holds:
interrupts win when events are sparse and unpredictable, polling wins when they are dense
and continuous.)

### The WHY of top half / bottom half: keep the handler short

There is one non-obvious design rule that looks like a quirk until you see its reason.
While an ISR runs, two costs are accruing at once: the program that was interrupted is
**frozen** (its state is saved, it is making no progress), and — crucially — *other*
devices that want attention may be made to **wait**, because while servicing one interrupt
the [[kernel]] commonly blocks further interrupts on that path so the handler is not itself
interrupted mid-step. An ISR that did slow work would therefore stall both the bystander
program and every other device behind it.

So Linux splits the response into two pieces:

- The **top half** is the ISR proper — the code that runs *immediately*, inside the
  interrupt, with other interrupts held off. It is deliberately tiny: do only what cannot
  wait. For a keyboard that means "grab the raw key code out of the controller's register
  before the next keypress overwrites it, stash it in a buffer, and note that there is work
  to finish." Then it returns at once, re-enabling interrupts.
- The **bottom half** is the deferred remainder — the heavier processing that *can* safely
  happen a moment later, once the urgent grab is done and interrupts are flowing again. It
  runs outside the interrupt, scheduled by the [[kernel]] as ordinary [[kernel]] work.
  (Linux has a few flavours of bottom half — *softirqs*, *tasklets*, and *workqueues* —
  differing in how soon and in what context they run; on a Linux machine the bottom-half
  worker for soft interrupts even shows up as a [[kernel]] background thread named
  `ksoftirqd`. The distinction among the three is operational detail; the load-bearing idea
  is the split itself.)

The invariant the split maintains: **time spent with interrupts disabled stays as short as
possible.** Urgent-but-tiny work goes in the top half so the device is serviced before it
loses data; everything else is pushed to the bottom half so the CPU can get back to running
programs and fielding other devices.

### Worked instance: one keystroke

Take a concrete, non-degenerate event: at a shell prompt you press the key `l`. This
exercises a real IRQ, a real top-half/bottom-half split, a buffer, and a process actually
moving from asleep to running — none of the steps collapses away. Trace it through the
[[kernel]]'s entry points.

Set the scene first. The shell (call it `bash`) earlier made a `read` **system call** —
"give me a character from the keyboard." There was none yet, so the [[kernel]] marked
`bash` **asleep** (off the CPU, consuming no cycles) and recorded that it is waiting on the
keyboard. The CPU went on to other work or halted. The [[kernel]] is dormant; nothing of it
is executing. Now:

1. **Hardware signals.** Your finger closes a switch in the keyboard. The keyboard
   controller raises its **IRQ line** to the CPU.
2. **The interrupt fires (entry point: interrupt).** The CPU finishes its current
   instruction, saves the interrupted work's state, switches to privileged mode, and jumps
   to the keyboard's registered handler inside the [[kernel]]. The [[kernel]] is now awake.
3. **Top half.** The handler reads the raw **scancode** — the numeric code the keyboard
   hardware emits for the physical key — out of the controller's register (a privileged
   hardware access no ordinary program could perform), converts it toward the character
   `'l'`, and places it into the keyboard/terminal **input buffer**, a small [[kernel]]-owned
   data structure in main memory. It notes that a waiter may need waking, then returns
   immediately so interrupts are no longer held off. This minimal, urgent slice is exactly
   the top half: get the byte before the next keypress can clobber it, and get out.
4. **Wake the waiter (bottom-half / deferred work).** A moment later, outside the
   interrupt, the [[kernel]] finishes the response: it checks "is any process asleep waiting
   on this keyboard?", finds `bash`, and marks it **runnable** — moved from asleep to
   ready-to-run. This is the heavier part the top half deferred.
5. **The scheduler picks it up.** At the next **timer interrupt**, the scheduler sees
   `bash` is runnable and gives it the CPU.
6. **The system call returns.** `bash` resumes inside its `read` call; the [[kernel]]
   copies `'l'` out of the buffer into `bash`'s own memory, switches the CPU back to
   restricted mode, and returns. From `bash`'s point of view, `read` simply returned `'l'`.
   `bash` then echoes it to the screen and calls `read` again, finding nothing, so the
   [[kernel]] marks it asleep once more. Back to a dormant [[kernel]] and an idle CPU.
   Elapsed time: microseconds.

Notice what the trace demonstrates about the interrupt specifically. The keyboard got the
[[kernel]]'s attention **asynchronously** — `bash` was asleep and not asking, yet the
device still reached the [[kernel]] — which is precisely what polling could not have done
without wasting the CPU. The response was **split**: a tiny urgent grab inside the interrupt
(top half) and the rest deferred (bottom half), keeping the window with interrupts disabled
as short as one register read. And the whole thing was driven by hardware *entering* the
[[kernel]], not by the [[kernel]] running on its own. That is the entire concept in one
keystroke: an interrupt is a hardware signal that preempts the CPU and forces it into a
[[kernel]] handler, so devices can be *notified-from* rather than *polled-for*.

## Prerequisites

- [[kernel]]

## Sources

- Linux internals study guide (`etc/linux-internals-complete.html`) — "How the kernel 'runs' — three entry points" (ENTRY POINT 2: Hardware interrupt — "Hardware fires an interrupt … CPU stops whatever it's doing … jumps to the registered handler for that IRQ … returns to whatever was running"; and the timer-tick entry point as the scheduler's heartbeat), "So what is the kernel doing at this very moment?" (interrupts firing constantly — timer/keyboard/NIC/disk — and the low-power halt between them), the "Walkthrough — what happens when you press a key?" trace (IRQ → keyboard handler → keycode → TTY input buffer → wake bash → read() returns), the IRQ glossary entry ("Interrupt Request — a signal from hardware to the CPU that something needs attention"), the `ksoftirqd` kernel thread that "handles soft interrupts," and the interrupt-driven network receive path with its NAPI interrupt-then-poll note (the polling contrast). The top-half/bottom-half framing and the polling-versus-interrupt argument are the standard reading of these passages.
