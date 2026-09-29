# Byte-Pair Encoding Tokenization

## Meaning

[[byte-pair-encoding-tokenization]] (BPE) is one recipe for creating [[subword-tokenization]]. It learns which neighboring symbols occur together frequently and makes those pairs reusable vocabulary entries. It is a statistical text-segmentation method, not a rule for finding true linguistic words.

## Mechanism

After normalization and any pre-tokenization, begin with small symbols. Count each adjacent pair in the training corpus, select a frequent pair, merge it into a new symbol, and repeat until reaching a vocabulary budget. Keep the merge order. When encoding new text, use the frozen rules; do not recalculate frequencies from the user's prompt. A [[hash-map]] is a convenient way to maintain pair counts during training.

An implementation's base alphabet matters. Byte-level BPE can represent arbitrary UTF-8 bytes without an unknown character, but may use several pieces for one character. A character-level variant can have different unknown-token behavior. Some pre-tokenizers forbid merges across whitespace; others attach a leading space to the following word. Therefore “BPE” alone does not specify exact prompt boundaries or round-trip behavior.

## One example

If `l` followed by `o` is frequent, the tokenizer may learn `lo`. If `lo` followed by `w` is later frequent, it may learn `low`. A completed word could now use fewer tokens. But when a user has typed only `lo` at a cursor, its terminal tokens and continuation task can differ from the tokens for the completed word. The compression gain is not an autocomplete result.

## Check your understanding

**Question:** Does BPE choose the globally shortest tokenization of every new string? **Answer:** No. It follows learned merge rules and pre-tokenization constraints. Test actual encoding, round trips, and downstream quality.
