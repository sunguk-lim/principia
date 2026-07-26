---
id: trie
title: Trie
summary: A trie (also called a prefix tree) stores a set of strings as a tree in which every edge is labelled with a single character, so the path from the root down to any node spells out…
type: concept
tags: [algorithms]
prereqs: [hash-map]
sources: [etc/study-notes.html]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Trie

## Summary

A trie (also called a *prefix tree*) stores a set of strings as a tree in which
every edge is labelled with a single character, so the path from the root down to
any node spells out one prefix, and strings that begin the same way share the same
upper path. In the representation used here each node is a [[hash-map]] from
"next character" to the child node reached by that character, plus a flag marking
whether the path so far is a complete stored word — a structure often nicknamed a
"dict of dicts." Inserting or looking up a string of length `L` walks `L`
characters from the root, doing one [[hash-map]] lookup per step, so the cost is
`O(L)` — proportional to the *length of the key*, not to how many strings the trie
holds. Its distinctive power is that it answers *prefix* questions naturally
("give me every stored word starting with `ca`"): you walk to the node for that
prefix, and the whole subtree beneath it is exactly the set of matching words.

## Grounded explanation

**The object and the problem it solves.** A trie stores a *set of strings* — for
instance the words `cat`, `car`, `dog` — and supports three things: *insert* a
string, *check* whether an exact string is present, and, the one that motivates
the whole structure, *enumerate every stored string that begins with a given
prefix*. A [[hash-map]] whose keys are the whole strings already gives you the
first two beautifully: insert and exact-lookup are each `O(1)` on average, because
the map computes a bucket directly from the entire string and goes straight there.
But that very strength is what makes prefix queries impossible for it. A
[[hash-map]] deliberately scatters keys across its buckets by their hash codes, so
`car` and `cat` — which a human sees as near-neighbours sharing `ca` — land in
unrelated, unpredictable buckets. The map has *no notion* that one string is a
prefix of, or shares a beginning with, another; to answer "all words starting with
`ca`" it would have to scan every stored key and test each one, which is `O(n)` in
the number of stored strings and throws away the map's entire advantage. The trie
exists to make prefix structure *first-class* instead of scattered.

**The central idea: spell strings out along the edges of a tree.** A *tree* here is
a branching structure of *nodes* connected by *edges*, starting from a single
top node called the *root*; following edges downward from the root reaches deeper
nodes. The trie's defining move is to label each edge with one *character* and let
*position in the tree carry meaning*: the sequence of edge-characters read from the
root down to a node spells exactly one *prefix* (a prefix of a string is any
starting chunk of it — `c`, `ca`, and `cat` are all prefixes of `cat`). The root
itself, reached by walking nothing, stands for the empty prefix. The decisive
consequence is *sharing*: two strings that begin with the same characters follow
the *same edges* out of the root for as long as they agree, so they travel through
the *same* nodes, and only *branch apart* at the first character where they differ.
`cat` and `car` agree on `c` then `a`, so they share the root → `c` → `a` path and
split only at the final step (one edge `t`, one edge `r`). This shared upper path
*is* the prefix `ca`, represented exactly once. That is the structural payoff a
[[hash-map]] of whole strings cannot offer: in the trie, a prefix is a *place* —
one specific node — not a property you must search the whole collection to test.

**How a node is built — a [[hash-map]] per node ("dict of dicts").** To represent a
node we must record, for each character that can lead out of it, *which* child node
that character reaches. That is precisely a key → value lookup — key is the next
character, value is the child node — so **each node is itself a [[hash-map]]** from
"next character" → "child node." A node's outgoing edges are simply the keys
present in its [[hash-map]]; an absent key means there is no edge for that character
and hence no stored string continuing that way. Because every node is a
[[hash-map]] and its children are nodes (which are themselves hash-maps), the whole
trie is a [[hash-map]] whose values are hash-maps whose values are hash-maps — the
"dict of dicts" nickname names exactly this nesting. One more piece is needed: the
path to a node spells a prefix, but we must know whether that prefix is also a
*complete stored word*. `ca` lies on the way to `cat` and `car` but is not itself a
stored word, whereas `cat` is. So each node also carries an *end-of-word flag* — a
true/false mark saying "a string ending here was inserted." Without it the trie
could not tell a genuine stored word from a mere waypoint.

**The operations, and why each costs `O(L)`.** Let `L` be the length of the string
being inserted or searched.

- *Insert* a string: start at the root and process its characters left to right,
  keeping a "current node" that begins at the root. For each character, look it up
  in the current node's [[hash-map]]. If a child already exists for it (a previous
  string used this edge), step into that existing child — this is where sharing
  happens, since nothing new is created for the common prefix. If no child exists,
  create a fresh empty node, store it in the current node's [[hash-map]] under that
  character, and step into it. After consuming all `L` characters, set the final
  node's end-of-word flag to true. The work is `L` iterations, each one
  [[hash-map]] lookup plus possibly one [[hash-map]] insertion — both `O(1)` average
  — so insert is `O(L)`.
- *Exact search* for a string: again walk from the root, one character at a time,
  following the [[hash-map]] edge for each. If at any step the needed character is
  *absent* from the current node's map, the string was never inserted — stop and
  report absent. If you consume all `L` characters successfully, the string is
  present *only if* the node you land on has its end-of-word flag set (otherwise
  you arrived at a waypoint like `ca`, not a stored word). This is `L` [[hash-map]]
  lookups, so `O(L)`.

The headline is that both costs are `O(L)` — proportional to the *length of the one
key in hand* — and **independent of `n`, the number of strings stored.** A trie
holding a million words finds a five-letter word in five steps, the same five it
would take if the trie held ten words. This is a different bargain from the
[[hash-map]] of whole strings, whose exact-lookup is `O(1)` (not even depending on
`L`, because it hashes the whole string in one conceptual shot); the trie gives up
that flat `O(1)` exact-lookup in exchange for the prefix power below.

**The prefix query — the operation the structure is built for.** To answer "every
stored word starting with prefix `P`," walk from the root following `P`'s
characters through the [[hash-map]] edges, exactly as in search but stopping after
`P`'s last character. If any character of `P` is missing along the way, no stored
word has that prefix — the answer is empty. Otherwise you arrive at *one* node: the
node whose root-path spells `P`. Now the structural insight pays off in full: every
string stored in the trie that begins with `P` must pass through this very node
(its path *starts* with `P`'s edges), and conversely everything reachable in the
subtree hanging below this node spells a string beginning with `P`. So the complete
answer is "this node together with everything beneath it" — gathered by walking
that subtree and emitting the path of every node whose end-of-word flag is set.
Reaching the prefix node costs `O(length of P)`; listing the matches then costs
time proportional to how many matches there are. No scan of unrelated strings ever
happens, because unrelated strings live in *other* subtrees entirely. This is the
query a [[hash-map]] of whole strings simply cannot do without inspecting all `n`
keys.

**Worked instance.** Build a trie and insert `cat`, `car`, `dog`. Start with just a
root node whose [[hash-map]] is empty and whose end-of-word flag is false.

- Insert `cat`. At the root, character `c`: the root's map has no `c`, so create a
  new node `N_c` and store `root["c"] = N_c`; step into `N_c`. Character `a`: `N_c`
  is empty, create `N_ca`, store `N_c["a"] = N_ca`, step in. Character `t`: create
  `N_cat`, store `N_ca["t"] = N_cat`, step in. End of string — set `N_cat`'s
  end-of-word flag true.
- Insert `car`. At the root, character `c`: this time `root["c"]` *already exists*
  (it is `N_c`), so step into the existing `N_c` — no new node, the `c` edge is
  shared. Character `a`: `N_c["a"]` already exists (`N_ca`), step into it — the `a`
  edge is shared too, so `cat` and `car` now share the whole root → `c` → `a` path.
  Character `r`: `N_ca` has a `t` edge but *no* `r` edge, so create `N_car`, store
  `N_ca["r"] = N_car`, step in. End — set `N_car`'s flag true. The branch happened
  exactly at `N_ca`, which now has two children: `t` → `N_cat` and `r` → `N_car`.
- Insert `dog`. At the root, character `d`: `root` has no `d` (it only has `c`), so
  create `N_d`, store `root["d"] = N_d`, step in; then `o` makes `N_do`, then `g`
  makes `N_dog`, whose flag is set true. `dog` shares nothing with the `c` words —
  it sits in a separate subtree under the root.

Now query prefix `ca`. Walk from the root: `c` → `N_c` (present), `a` → `N_ca`
(present); `ca` is consumed, so the prefix node is `N_ca`. Everything beneath it:
its `t` edge reaches `N_cat` (flag set → emit `cat`), its `r` edge reaches `N_car`
(flag set → emit `car`). Result: `{cat, car}`. Note `N_ca` *itself* has its flag
false, so `ca` is correctly *not* reported as a stored word — the flag earned its
keep. Query prefix `do` instead: `d` → `N_d`, `o` → `N_do`; beneath `N_do` lies
`g` → `N_dog` (flag set → emit `dog`), giving `{dog}`, and the `c`-subtree was never
touched. That selective reach — straight to the prefix node, then only its subtree —
is the entire reason the structure exists.

**Where this shows up.** The prefix query is exactly the engine behind
*autocomplete* (type `ca`, get back every completion stored under it), *spell-check
dictionaries* (is this word present, and what near-prefixes exist), and IP routing
tables (which use the same idea over the bits of an address to find the
longest-matching prefix). The source's "problem signal → structure" rule of thumb
states it crisply: when a problem says *"prefix / autocomplete,"* reach for a trie.
The recurring Python representation it names is the "dict of dicts" — each node a
[[hash-map]] from next character to child — which is the construction explained
above.

## Prerequisites

- [[hash-map]]

## Sources

- `etc/study-notes.html` §9 "Data structures cheat sheet" — the **Trie** row
  (`dict of dicts`, `insert / search O(L)`, "prefix queries, word dictionaries"),
  and the "Problem signal → structure" panel ("Prefix / autocomplete" → **trie**).
