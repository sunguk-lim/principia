---
id: mpi-datatype
title: MPI Datatype
summary: An MPI datatype is the part of a message that says what each element is.
type: concept
tags: [parallel-computing]
prereqs: [message-passing]
sources: [etc/mpi_collective_operations.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# MPI Datatype

## Summary

An **MPI datatype** is the part of a message that says *what each element is*. In
[[message-passing]] one process hands some data to another, but the bytes alone do
not say how to read them. MPI fixes this by describing every transfer as a triple:
a **buffer** (a starting address in the sender's or receiver's private memory), a
**count** (how many elements), and a **datatype** (what one element looks like in
memory). The datatype is the type tag on the wire: it tells the library how big one
element is, how to translate it when the two machines store numbers differently, and
even how the elements are spread out in memory when they are not packed back-to-back.

## Grounded explanation

In [[message-passing]] a process can only obtain another process's data by an
explicit send matched by an explicit receive; the bytes are copied from one private
memory into another. But a raw run of bytes is ambiguous: eight bytes could be one
64-bit number, or two 32-bit numbers, or eight characters. The sender and receiver
must agree on the interpretation, or the copy is meaningless. **MPI** (the Message
Passing Interface, the standard library that implements message passing) removes the
ambiguity by never letting you describe a message as bare bytes. Every send and
every receive is given as a **(buffer, count, datatype)** triple. Define each term:

- **Buffer** — the memory address where the elements begin. This is *where* in a
  process's private memory the data sits.
- **Count** — a plain integer: *how many* elements of the given datatype to move.
- **Datatype** — the description of *one* element: its size in bytes and how its
  bytes are laid out and to be interpreted.

Three jobs follow from having the datatype, and they are the reason the type tag
exists rather than a raw byte count.

**(1) Computing the byte count safely.** The library multiplies count by the size
the datatype declares to learn how many bytes to copy. You say "100 elements of this
type," not "800 bytes"; the byte arithmetic is the library's job, so it cannot drift
out of sync with what the elements actually are.

**(2) Interoperating across different machines.** Two machines need not store a
number the same way. *Endianness* is the order in which a machine lays out the bytes
of a multi-byte number (most-significant byte first, or least-significant byte
first); machines also sometimes disagree on how many bytes a given kind of number
takes. Because the datatype names the *kind* of value rather than a fixed byte
pattern, the library can convert the representation as it moves the data — the
receiver gets the same numeric value even on a machine that stores it differently.
This matters because the processes in [[message-passing]] may run on physically
different computers.

These two jobs are served by **basic datatypes**: named constants, each standing for
one primitive value and its size. `MPI_INT` is one integer; `MPI_DOUBLE` is one
double-precision floating-point number; `MPI_CHAR` is one character. Naming the kind
(not the byte count) is exactly what lets job (1) compute sizes and job (2) convert
between machines.

**(3) Moving non-contiguous shapes in one call.** *Contiguous* means the elements sit
back-to-back in memory with nothing between them; *non-contiguous* means they are
spread out — there are gaps, or the pieces have different kinds. A **derived
datatype** is a datatype you build to describe such a spread-out shape, so that a
single send or receive can move it directly, with no manual copying into a packed
temporary buffer first. Two common shapes:

- A **strided vector**: take an element, skip a fixed *stride* (a fixed distance in
  memory), take the next, and so on — every k-th element. This describes, for
  instance, one column of a matrix stored *row-major* (a matrix laid out one whole
  row after another, so the entries of a single column are not adjacent — they are
  one row's width apart).
- A **struct**: a fixed bundle of fields of *mixed* kinds — say an integer followed
  by two doubles — moved together as one element.

So the full picture: the datatype turns an opaque byte transfer into a typed one.
That single decision buys all three properties at once — safe byte arithmetic,
cross-machine conversion, and in-place transfer of scattered data — and it is why
every MPI operation carries a datatype argument. A point-to-point send is a
(buffer, count, datatype) triple, and a group-wide ("collective") operation is the
same triple wired to many peers. In a one-to-many broadcast, written
`MPI_Bcast(buffer, count, type, root, comm)`, the *root* (the one process that owns
the data) sends the same `count` elements of `type` to everyone. When the data sent
and the data received have different shapes — as in a *scatter*, where the root cuts
one array into chunks and sends one chunk to each process — the operation carries a
*sendtype* and a separate *recvtype*, e.g.
`MPI_Scatter(sendbuf, sendcount, sendtype, recvbuf, recvcount, recvtype, root, comm)`,
because the source layout and the destination layout are described independently.

Worked instance. Suppose process A must send process B one hundred double-precision
numbers that sit back-to-back in memory. A names them with the triple
`(buf, 100, MPI_DOUBLE)`. The library reads from `MPI_DOUBLE` that one element is 8
bytes, multiplies by the count of 100, and moves 800 bytes — and if B runs on a
machine with the opposite endianness, the library reorders each number's bytes so B
reads the same hundred values. Now the non-degenerate case. A holds a 4x4 matrix
stored row-major, so its sixteen doubles lie in memory as row 0, then row 1, then
row 2, then row 3. A wants to send only *column 0*: entries at positions 0, 4, 8,
and 12 — every 4th element, because each row is 4 wide. A builds a derived strided
vector: **4 blocks, each 1 double, with a stride of 4 doubles between block
starts.** A single send with this derived datatype moves the four scattered column
entries directly, with no intermediate copy. The stride of 4 (not 1) is the whole
point — it is what makes the type *derived* rather than a plain contiguous run, and
it is exactly the row width that separates one column entry from the next.

## Prerequisites

- [[message-passing]]

## Sources

- etc/mpi_collective_operations.html — collective signatures showing the
  `(buffer, count, type)` triple and the separate `sendtype`/`recvtype` arguments
  (e.g. `MPI_Bcast`, `MPI_Scatter`).
