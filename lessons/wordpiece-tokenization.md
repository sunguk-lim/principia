# WordPiece Tokenization

## Meaning

[[wordpiece-tokenization]] is a subword method associated with BERT. Given a fixed vocabulary, its familiar inference behavior takes the longest valid piece at each position of a pre-tokenized word. A continuation marker such as `##` means a piece can occur inside a word, not necessarily at its start.

## Mechanism

First normalize and split input according to the deployed tokenizer. At the beginning of a word, find the longest vocabulary entry that matches. Move forward, then look for a continuation entry at the new position. Repeat until the word is covered. A [[trie]] can make prefix lookup efficient, but an ordinary search would express the same rule. If no valid continuation exists, some implementations replace the whole word with an unknown token. Do not assume the byte-level coverage of a different tokenizer.

WordPiece is often compared with BPE because both use subword vocabularies. The inference algorithms are not the same: BPE applies learned merge priorities, whereas WordPiece greedily selects vocabulary pieces. Discussions of the original WordPiece *training* score should be qualified, because Google's original trainer was not publicly released. A deployed model's actual vocabulary and encoder are the reliable facts to inspect.

## One example

With vocabulary entries `play` and `##ing`, `playing` can become `play`, `##ing`. If `##ing` is absent, the encoder needs a different valid continuation or its documented fallback. Test unseen names, punctuation, casing, and the difference between beginning and interior positions, not only common words.

## Check your understanding

**Question:** What does `##ing` signal? **Answer:** It is a continuation piece, valid after a preceding piece within the word; it is not automatically a word-initial token.
