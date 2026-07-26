---
id: hard-link
title: Hard Link
summary: A hard link is an additional name for a file that already exists — a directory entry (a name-to-number pair) pointing at an existing inode.
type: concept
tags: [os/filesystem]
prereqs: [inode, dentry]
sources: [linux-internals-complete.html]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Hard Link

## Summary

A hard link is an additional **name** for a file that already exists — a [[dentry]] (a name-to-number pair) pointing at an existing [[inode]]. Because a name and the [[inode]] it names are separate things, one [[inode]] can be reached through several names at once. Two hard links are therefore two equal names for the *same* file, not two copies: editing the file through either name changes the single shared file, because both names resolve to the same numbered object. The [[inode]] keeps a **link count** — a tally of how many names currently refer to it — and the file's data is freed only when that count falls to zero. This is why "deleting" a file is really *unlinking* a name: you remove one name, and the data survives as long as any other name still points at it.

## Grounded explanation

The key insight is the separation that the [[inode]] establishes: the [[inode]] is the numbered object holding a file's metadata and data-block pointers, and it does **not** contain the file's name. The name lives elsewhere, in a *[[dentry]]* — a pair binding a human-readable name to an [[inode]] number. A directory is just a list of such pairs. So the chain "name → number → object" has two independent halves, and nothing forces it to be one-to-one. A **hard link** is exactly what you get by adding a *second* directory entry whose number is that of an [[inode]] that already exists. No new [[inode]] is created and no data is copied; you have merely written one more name into some directory's list, pointing at the same numbered object the first name points at.

This is why the two names are interchangeable rather than independent. Resolving either name lands on the identical [[inode]], and the [[inode]] is the single thing that holds the data-block pointers — the actual file content. So a write performed by opening one name reaches the shared [[inode]], rewrites its data blocks, and is therefore immediately visible when you next open the other name. There is no synchronization to do, because there is nothing to synchronize: there is only one file, seen through two doors. By the same logic, metadata stored in the [[inode]] — size, permissions, timestamps — is one shared set of facts, not a per-name copy.

The mechanism that makes shared ownership *safe* is the **link count** kept inside the [[inode]]. The link count is a simple reference count: it records how many directory entries currently name this [[inode]]. The system maintains an invariant — the count always equals the number of names that exist — by updating it at exactly the two moments names appear and disappear. Creating a hard link (writing a new directory entry for the [[inode]]) **increments** the count by one. Removing a name (erasing a directory entry) **decrements** it by one. The non-obvious payoff is in what happens at removal: the system frees the [[inode]] and reclaims its data blocks **only when the decrement brings the count to zero**. As long as the count is still positive, some name can still reach the data, so the data must stay. This is the precise reason the file-removal operation is named *unlink*, not "delete": its primitive action is to remove one name and decrement the count; freeing the data is a conditional consequence, triggered only by the last name's departure. Reference counting via the link count thus gives shared ownership with automatic, correct cleanup — no name is ever left pointing at freed data, and no still-referenced data is ever freed.

Two constraints follow from how this is built. First, a hard link **cannot cross filesystems.** A directory entry stores an [[inode]] *number*, and those numbers are only meaningful within one filesystem — each filesystem has its own pool of [[inode]]s numbered independently. A name in filesystem A holding a bare number could not unambiguously denote an [[inode]] living in filesystem B, so the link is disallowed. Second, hard links to **directories** are traditionally forbidden. Directories are connected into a tree by their entries, and allowing arbitrary extra names for a directory would let that tree contain cycles — a directory reachable as its own descendant — which would break tree-walking traversals that assume they always make downward progress. Restricting hard links to non-directory files keeps the directory structure a tree.

A **soft link** (also called a *symbolic link*) is a different construct, and the contrast sharpens what a hard link is. A soft link is not a second name for the same [[inode]]; it is itself a small separate file — with its own [[inode]] — whose entire content is a *path string* naming another file. Following a soft link means reading that stored path and then resolving it from scratch. Because the soft link only records a textual path rather than binding directly to a numbered object, it does not participate in the target's link count, it *can* point across filesystems and at directories, and it becomes a dangling reference if the path it names is later removed. A hard link, binding straight to the [[inode]] number, has none of these properties: it is genuinely the same file, counted, same-filesystem, non-directory.

The deeper *why* is that decoupling the name from the [[inode]] buys two things at once. The same file can appear in several places — several directories, under several names — with zero duplication of its data, because all the names share one [[inode]] and one set of data blocks. And the link count turns that sharing into safe, self-managing ownership: every name is accounted for, and the storage is released at exactly the right instant, neither while a name still needs it nor any later.

**Worked instance.** Start with a file named `a.txt`. Suppose its directory entry maps the name `a.txt` to [[inode]] number 12345, and that [[inode]]'s link count is 1 (one name points here). Now create a hard link with the command `ln a.txt b.txt`. This writes a *second* directory entry, mapping the name `b.txt` to the **same** number, 12345, and increments the [[inode]]'s link count to **2**. No data was copied; both names now denote [[inode]] 12345. Edit the file through `b.txt` — open `b.txt`, which resolves to [[inode]] 12345, and write to it. Reading through `a.txt` resolves to that very same [[inode]] 12345, so it sees the change: the two names share one file. Now remove a name with `rm a.txt`. Despite its spelling, `rm` performs *unlink*: it erases the `a.txt` directory entry and decrements the link count to **1**. The count is still positive, so the data blocks of [[inode]] 12345 are untouched — the file is fully intact and still reachable as `b.txt`. Finally run `rm b.txt`. This erases the last entry and decrements the count to **0**. Now — and only now — the system frees [[inode]] 12345 and reclaims its data blocks. The file is gone precisely because its *last* name was removed, which is the whole point of unlink-and-count semantics.

## Prerequisites

- [[inode]]
- [[dentry]]

## Sources

- linux-internals-complete.html — §7 Filesystem & I/O: "one file can have multiple names — these are called hard links. Two different paths can point to the same inode. The file's data is only deleted when the last name (link) pointing to it is removed"; the inode slot's "Link count" field; "Filenames and files are separate. A filename (dentry) points to an inode."
