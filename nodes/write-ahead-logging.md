---
id: write-ahead-logging
title: Write-Ahead Logging (WAL)
summary: Write-Ahead Logging delivers transaction durability despite deferred writeback by forcing log records to stable storage before acknowledging COMMIT; recovery redoes committed effects and undoes any uncommitted effects that reached data pages.
type: concept
tags: [databases/storage]
prereqs: [transaction, page-cache, writeback, block-layer]
sources:
  - "https://www.postgresql.org/docs/current/wal-intro.html — PostgreSQL: Write-Ahead Logging (WAL)"
  - "C. Mohan et al., 'ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging' (ACM TODS, 1992)"
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Write-Ahead Logging (WAL)

## Summary

**Write-Ahead Logging (WAL)** is the mechanism a database uses to make a
[[transaction]]'s **Durability** real. Recall the durability promise: once `COMMIT`
returns, the transaction's effects must survive a crash. The obstacle is everything
[[writeback]] taught — when a transaction modifies a row, the database changes a *data
page* in the [[page-cache]], which marks that page **dirty** and returns at RAM speed;
the dirty page is flushed to disk only **later** by background [[writeback]], or **never**
if a crash intervenes first. So a transaction could `COMMIT`, be told it succeeded, and
then be **lost** in a crash because its data pages never reached disk. WAL closes that
gap with one rule — the **write-ahead invariant**: *before* a data page's change is
allowed to go to disk, **first append a record describing the change to a sequential
log**, and at `COMMIT` **force that log to stable storage with `fsync` and wait** —
only then report the commit as successful. The data pages themselves stay dirty and are
written lazily by ordinary [[writeback]]; only the *log* is forced at commit. This is
cheap because the log is a **sequential append** — one contiguous [[block-layer]] write,
fast — whereas the dirty data pages are **scattered** across the disk and would cost
many slow random writes. On restart after a crash, the engine **replays the log**: it
**REDO**es committed changes whose data pages never got flushed and **UNDO**es any
uncommitted changes that had reached data pages, reconstructing the last committed state.

## Grounded explanation

### The gap WAL exists to close — Durability vs. deferred writeback

[[transaction]] sets the bar: **Durability** says that once `COMMIT` returns, the
transaction's writes survive a crash, because the database "forced the write to stable
storage first." But *what* gets forced, and *how*, is exactly the question [[writeback]]
makes urgent. When a transaction updates a row, the database does not write a disk sector;
it modifies the **data page** holding that row inside the [[page-cache]]. As the
[[page-cache]] and [[writeback]] nodes establish, that write merely marks the cached page
**dirty** (changed in RAM, not yet matching disk) and returns in microseconds. The page is
carried to disk only **later** — by a background [[writeback]] flush on a 5–30 second
timer, under memory pressure, or never if the machine crashes in the meantime.

Now overlay durability on that timeline and the problem is stark. Suppose a transaction
commits, the client is told "success," but the two data pages it dirtied are still sitting
in the [[page-cache]], not yet flushed. **Crash.** Those volatile dirty pages vanish — the
very loss [[writeback]] warned about — and on reboot the disk holds the *pre-transaction*
contents. A committed transaction is **gone**, breaking Durability. The naive fix is the
one [[writeback]] names: `fsync` every dirty data page at commit and wait. But that is
exactly what is too slow, and *why* it is too slow is the heart of WAL — covered below.

### The write-ahead invariant — log first, force the log, flush data later

WAL splits durability into two separate writes with a strict order between them. Alongside
the data pages it keeps a **log**: an append-only sequence of small records, each
describing one change — "transaction T set row R on page P from old-value to new-value."
The defining rule, the one the whole technique is named for, is:

> **Write-ahead invariant: before a data page's change is permitted to reach disk, the
> log record describing that change must already be on stable storage.** The log goes out
> *ahead* of the page.

Concretely, a committing transaction does three things in order. (1) As it modifies each
row, it **appends a log record** to the in-memory tail of the log and dirties the
corresponding data page in the [[page-cache]] — both still in RAM. (2) At `COMMIT`, it
appends a **commit record** and then **`fsync`s the log** — the same forced, blocking flush
[[writeback]] defines, here aimed at the *log file*: it does not return until those log
records have physically reached the disk. (3) Only after that `fsync` returns does the
database report the commit as successful. The data pages are **not** forced; they remain
dirty and are flushed whenever ordinary [[writeback]] gets to them — seconds later, or
after the crash via replay. Durability is now carried entirely by the log: at the instant
`COMMIT` returns, the *record* of every change is durable, even though the changed *pages*
are not.

### Why this is fast — one sequential write instead of many random ones

Why force the log but not the data pages? Because of how a disk charges for writes, which
[[block-layer]] makes precise. The [[block-layer]] turns a file's logical blocks into
**sector** ranges on the device and queues, merges, and orders those requests; its central
lesson is that the expensive thing on storage is the **per-request positioning** — on a
spinning disk the seek between far-apart sectors, more generally the fixed cost paid *per
scattered request*. A run of **contiguous** sectors is one cheap, mergeable transfer; the
same number of bytes spread across **distant** sectors is many separate, slow ones.

Map the two writes onto that cost model:

- The **data pages** a transaction touches are **scattered**. Two updated rows may live on
  two different pages that map to far-apart sectors on the device. Forcing them at commit
  is **many random writes** — exactly the access pattern [[block-layer]] shows is slow,
  the head (or the per-request overhead) thrashing between distant locations.
- The **log** is **one sequential file written only by appending to its end.** Every commit
  from every transaction adds records to the same growing tail, so successive log writes hit
  **adjacent sectors** — the contiguous case the [[block-layer]] merges into a single fast
  transfer. One `fsync` of the log tail is one well-localized write.

So WAL **converts the per-commit durability cost from many random writes (the scattered data
pages) into one sequential write (the log append).** That is the trade that makes durable
commits affordable: you still pay one forced disk write per commit, but it is the cheap,
contiguous kind, and the expensive scattered writes are deferred to background [[writeback]],
which can then batch and reorder them at its leisure exactly as [[writeback]] describes.

### Crash recovery — replay the log

Deferring the data pages is only safe because the log lets the database **reconstruct** them
after a crash. On restart, before serving anyone, the engine **replays the log** from the
last checkpoint forward:

- **REDO.** For every change whose transaction has a **commit record** in the log, re-apply
  the change to the data page — read the (stale or pre-write) page off disk into the
  [[page-cache]] and write the logged new value into it. This recovers precisely the
  committed changes whose data pages never got flushed before the crash. Because the commit
  record was `fsync`ed *before* the client was told "success," every acknowledged commit has
  its records on disk to replay — Durability holds.
- **Ignore / UNDO.** For changes belonging to a transaction with **no** commit record (it
  was still in flight at the crash), do **not** apply them — and if a partially-applied
  uncommitted change had leaked to a data page, **undo** it using the logged old value. This
  enforces [[transaction]] Atomicity across the crash: an uncommitted transaction leaves *no*
  effect, just as a `ROLLBACK` would.

After replay the [[page-cache]] holds exactly the last committed state, and normal
[[writeback]] eventually flushes those recovered pages to disk.

### Worked instance — two rows on two pages, commit, crash, replay

Take a transaction T that updates two rows that happen to live on **two different data
pages**:

```
BEGIN T
  W1:  page 5, row "A.balance":  500 → 400      (append log record L1)
  W2:  page 9, row "B.balance":  200 → 300      (append log record L2)
COMMIT T                                         (append commit record L3)
```

Pages **5** and **9** are deliberately different pages, and on disk they map to far-apart
[[block-layer]] sectors — say sectors `40000` and `93000` — so flushing both would be **two
random writes**. Trace the write-ahead ordering:

1. **W1.** The engine appends **L1** = "T: page 5 row A 500→400" to the log tail and dirties
   **page 5** in the [[page-cache]]. Nothing is on disk; page 5 is dirty.
2. **W2.** It appends **L2** = "T: page 9 row B 200→300" and dirties **page 9**. Still
   nothing on disk; pages 5 and 9 both dirty.
3. **COMMIT.** It appends **L3** = "T committed" and **`fsync`s the log**. Now L1, L2, L3 are
   physically on disk, in **one contiguous append** to the log file (one fast sequential
   [[block-layer]] write). Only now does `COMMIT` return "success" to the client. Crucially,
   **pages 5 and 9 are still only dirty in the [[page-cache]]** — neither has been written
   back to sector 40000 or 93000.
4. **CRASH** — power loss, one second after the client saw "success," before any
   [[writeback]] flush ran. Volatile RAM is wiped: dirty pages 5 and 9 are **gone**. On disk,
   the data file still holds the *old* balances (A=500, B=200); the log file holds L1, L2, L3.

   Without WAL this is the lost-commit disaster: T committed but its data pages never reached
   disk, so the balances revert and `400 + 300` is lost. **With WAL, the log saves it.**

5. **RESTART — replay.** The engine reads the log, finds **L3** (T has a commit record), and
   **REDO**es T: it reads page 5 off disk (still showing A=500), applies L1 → writes A=400 into
   the cached page; reads page 9 (still B=200), applies L2 → writes B=300. The recovered
   [[page-cache]] now holds A=400, B=300 — the **committed** state — even though **neither data
   page was ever written to disk before the crash.** Ordinary [[writeback]] later flushes the
   recovered pages 5 and 9 out to sectors 40000 and 93000 at its own pace.

Had the crash instead struck *between* W2 and the `COMMIT` `fsync` — so the log held L1, L2 but
**no L3** — replay would find no commit record for T and **ignore/UNDO** both changes, leaving
A=500, B=200, as if T never ran. So every crash resolves to a legal [[transaction]] outcome:
fully applied (committed, REDONE) or fully absent (uncommitted, ignored), never half.

This ties the three levels of one example together: the **structure** is the log (a sequential
record sequence) standing in front of the scattered data pages; the **algorithm** is *append
log → dirty page → fsync log at commit → replay on restart*; and the **substrate** is the
[[block-layer]]'s disk, where the log's contiguous sectors make the commit `fsync` one cheap
write while the data pages' distant sectors are left for lazy [[writeback]].

## Prerequisites

- [[transaction]] — WAL is the *mechanism* that implements this node's **Durability** (commit
  survives a crash) and enforces its **Atomicity** across a crash (REDO committed, ignore/UNDO
  uncommitted); the worked instance is its $100-transfer made durable.
- [[page-cache]] — a row update is a write to a cached **data page** that goes **dirty** and
  returns before reaching disk; this is the volatile state WAL must protect, and the cache the
  log replays *into* on recovery.
- [[writeback]] — establishes the gap WAL fixes (dirty pages flushed only later, or lost on
  crash) and supplies the **`fsync`-and-wait** primitive WAL aims at the *log*; the scattered
  data pages are left to ordinary background writeback.
- [[block-layer]] — supplies the sequential-vs-random cost model that justifies WAL: the log
  append is one contiguous (cheap) sector write, the scattered data pages are many random
  (expensive) ones, so forcing the log instead of the pages is the fast choice.

## Sources

- PostgreSQL Documentation — *Write-Ahead Logging (WAL)* — https://www.postgresql.org/docs/current/wal-intro.html (log records describing changes are flushed to permanent storage before the data pages they describe; only the log need be flushed at commit to guarantee the transaction is durable, since changes are replayed from the log after a crash).
- C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, P. Schwarz, *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging*, ACM Transactions on Database Systems 17(1), 1992 — the canonical WAL/recovery method (write-ahead rule, REDO/UNDO replay).
