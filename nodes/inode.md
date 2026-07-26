---
id: inode
title: Inode
summary: An inode is the single object — living both on disk and, while in use, cached in kernel memory — that holds everything about a file except its name.
type: concept
tags: [os/filesystem]
prereqs: [vfs]
sources: ["linux-internals-complete.html — §7 'Inodes and dentries — how files are tracked', 'Where inodes physically exist' (the 256-byte inode slot: type, permissions, owner, size, timestamps, link count, block pointers; filename NOT in the inode), 'Can you run out of inodes?'"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Inode

## Summary

An **inode** is the single object — living both on disk and, while in use, cached in
kernel memory — that holds *everything about a file except its name*. That "everything"
is of two kinds. First, the file's **metadata**: its type (regular file, directory,
device), its permission bits, its owner, its size in bytes, and its timestamps. Second,
the file's **block map**: the pointers that say *where on the disk the file's actual data
bytes live*. Each inode carries a unique **inode number**, and that number — not the
filename — is the file's true identity. A filename is merely a separate entry, kept in a
directory, that points at an inode number. Because the name is stored apart from the inode,
two names can point at the same inode, renaming a file touches only the name, and "deleting"
a file is really just removing one name. The inode is what the [[vfs]] actually tracks and
operates on once a path has been resolved.

## Grounded explanation

### What the concept is, and what it is not

Recall from [[vfs]] the chain the kernel follows to find a file: a **name** is looked up in a
directory to get an **inode number**, that number locates the **inode**, and the inode points
to the **data**. This node is about the third link in that chain — the inode — *as an object in
its own right*. It is not the name, and it is not the directory entry (the cached **name → inode
number** mapping the [[vfs]] node calls a *dentry*); both of those are plain machinery for
*reaching* an inode. The inode itself is the thing reached: the record that *is* the file.

Concretely, an inode is a **fixed-size record** — 256 bytes on the common Linux ext4 filesystem
— and it contains exactly two sorts of thing:

- **Metadata** — facts *about* the file. The **file type** (is this a regular file, a directory,
  or a device?), the **permission bits** (who may read, write, or execute it — e.g. `rw-r--r--`),
  the **owner** (a numeric user ID, and a group ID), the **size** in bytes, and three
  **timestamps** (when it was created, last modified, last accessed). One more metadata field is
  load-bearing below: the **link count**, an integer recording *how many names currently point at
  this inode*.
- **Block pointers** — the file's **block map**. A disk is divided into fixed-size **data blocks**
  (the chunks in which file contents are physically stored); the block pointers are the list of
  block addresses that hold *this* file's bytes. Reading the file means following these pointers to
  the right blocks. (On modern ext4 the raw list of pointers is replaced by **extents** — compact
  records each naming a *contiguous range* of blocks, e.g. "file blocks 0–1023 live at physical
  blocks 50000–51023" — but the role is identical: the inode still records *where the data lives*,
  just more compactly for large files. The detail does not change the concept.)

What the inode pointedly does **not** contain is the **filename**. That is the central structural
fact of this node, and everything below follows from it.

### Why the name is kept out of the inode — the key insight

Why separate the name from the file at all? Because doing so lets the [[vfs]] treat *identity* and
*label* as two independent things, and a great deal of ordinary filesystem behavior is exactly that
independence cashed out.

Picture the alternative the design rejects: if the name were stored *inside* the inode, then the
file and its name would be one inseparable thing. A file could have exactly one name; renaming it
would mean rewriting the file's own record; and you could never let two names refer to the same
bytes. By instead storing the name in a directory entry that merely *points at* an inode number,
the design makes the inode a **nameless, numbered identity** that any number of names can reference.

Three everyday behaviors are direct consequences (kept as prose here, since each is its own topic):

- **A file can have several names at once.** Two different directory entries can hold the *same*
  inode number; both names then reach the identical inode and therefore the identical data. (These
  multiple names are called *hard links*.) The inode's **link count** is simply how many such names
  currently exist.
- **Renaming is cheap and leaves the file untouched.** To rename `foo.txt` to `bar.txt`, the kernel
  edits only the directory entry — swap the text of the name beside the unchanged inode number. The
  inode, and every data block it points to, is not read or rewritten.
- **"Deleting" a file is really "removing a name."** Removing a name deletes that directory entry and
  decrements the inode's link count by one. The inode and its data blocks are reclaimed only when the
  link count reaches **zero** — i.e. when the *last* name is gone. Up to that point the file persists,
  nameless under its number, fully alive.

So the justification for the "magic-looking" step — that erasing a filename usually does *not* erase
the file — is the link count: the file is owned by its inode, the names are mere references, and the
file outlives any one of them until the references run out.

The deeper payoff connects back to [[vfs]]. Because every file, of every kind, is reachable as a
numbered inode carrying the same standard metadata fields, the [[vfs]] can treat all files
**uniformly**: resolve a path to an inode number, fetch the inode, read its type and permissions,
follow its block map. One numbered object centralizes a file's metadata and its data location, and
that uniformity is precisely what lets the [[vfs]] route operations without caring which filename
(or how many) happen to point at the file.

### Where the inode physically lives

When a disk is formatted, the formatter carves it into three regions: a **superblock** (a small
header describing the filesystem as a whole — its total size, its block size, *how many inodes it
has*, how much is free), an **inode table** (a big array of fixed-size inode slots, numbered
1, 2, 3, …), and the **data blocks** (where file contents go). The inode table is allocated *up
front*, at format time, with a **fixed number of slots** — and that fixed count drives the practical
consequence in the worked instance below.

Finding an inode by number needs no search: since every slot is the same size, the kernel computes
the slot's location by arithmetic — `inode_table_start + (inode_number × slot_size)` — a direct jump
to the right offset. (Real ext4 first picks one of several *block groups* and then offsets within that
group's slice of the table, but the principle, a calculation rather than a scan, is unchanged.) Once
read from disk, an inode is kept in an in-memory **inode cache**, so repeated access to the same file
does not re-read the disk; the on-disk copy is the permanent record, the cached copy the working one.

### A worked instance

Take a file `foo.txt`. Asking the system for its inode number — the command `ls -i foo.txt` does
this — prints, say, **inode 12345**. That number is the file's identity. Inside slot 12345 of the
inode table sits the 256-byte record. Suppose it reads:

- **type**: regular file
- **permissions**: `rw-r--r--` (octal mode `0644` — owner may read and write; group and others may
  only read)
- **owner**: user ID `0`, group ID `0` (root)
- **size**: 12 bytes
- **timestamps**: created / modified / accessed
- **link count**: `1` (exactly one name points here)
- **block pointers**: `[48320, -, -, …]` — "my 12 bytes of data are in data block 48320"

Now run the file through the three behaviors and watch what does and does not change:

1. **Rename** `foo.txt` to `bar.txt`. The kernel edits the directory entry: the text beside inode
   number 12345 changes from `foo.txt` to `bar.txt`. Inode 12345 is untouched — same permissions,
   same size, same block pointer `48320`, same link count `1`. The data block `48320` is never read.
   The file is identical; only its label moved.
2. **Add a hard link** named `baz.txt` to the same file. A *second* directory entry is created
   holding the *same* inode number, 12345. Now two names reach the one inode; its **link count rises
   to `2`**. Both `bar.txt` and `baz.txt` show inode 12345 under `ls -i`, and reading either follows
   pointer `48320` to the identical bytes.
3. **Remove** `bar.txt`. That directory entry is deleted and the link count drops to `1`. The file is
   *not* gone — `baz.txt` still reaches inode 12345 and its data block `48320` is intact. Only when
   `baz.txt` is also removed does the count hit `0`, and *then* inode slot 12345 and data block 48320
   are freed for reuse.

Finally, the consequence the source flags. Because the inode table has a **fixed number of slots**
fixed at format time, the count of inodes and the count of free data bytes are **separate budgets**,
and either can be exhausted first. Create millions of *tiny* files — each consuming one inode slot but
only a few bytes of data — and you can use up **every inode slot while the disk still has gigabytes of
free space**. The next file creation then fails for "no space," even though `df` reports free bytes,
because there is no free *inode* to hold its identity. (The command `df -i` reports inode usage
specifically; this failure is a classic one on mail servers and other systems that accumulate vast
numbers of small files.) This is the non-degenerate payoff of the whole design: an inode is a real,
separately-counted object, not a free side effect of having disk space — each file's identity costs
exactly one slot from a fixed pool.

## Prerequisites

- [[vfs]]

## Sources

- `linux-internals-complete.html` — §7 "Filesystem & I/O", sections
  "Inodes and dentries — how files are tracked" (the inode as a file's metadata-and-data structure
  identified by a number, distinct from its name; one file, multiple names) and "Where inodes
  physically exist" (the superblock / inode-table / data-blocks layout; the 256-byte ext4 inode slot
  listing file type, permissions `rw-r--r--`, owner UID/GID, size, timestamps, link count, and block
  pointers `[48320, …]`, with the explicit note that the filename is *not* in the inode; ext4 extents
  as the modern block map; the inode cache; and the Q&A "Can you run out of inodes?" — fixed slot
  count set at format time, `df -i`, millions of tiny files exhausting inodes while disk bytes remain).
