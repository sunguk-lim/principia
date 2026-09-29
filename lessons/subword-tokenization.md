# Subword Tokenization

## Meaning

A language model operates on token IDs, while people write characters and bytes. [[subword-tokenization]] is the conversion layer that chooses reusable pieces of text and maps them to IDs. Pieces can be smaller than a word but longer than a character. It gives common fragments short representations without requiring a separate vocabulary entry for every possible word, name, or identifier.

## Mechanism

A tokenizer is trained or configured once, then frozen for use with a model. Its normalization, base alphabet, vocabulary, and segmentation rule decide the output. A whole-word scheme struggles with unseen words. A character or byte scheme covers more inputs but often produces longer sequences. Subword schemes trade between those extremes. Some start from bytes and can represent any UTF-8 text; others need an unknown-token fallback. Encoding and decoding should be tested as a pair because normalization can deliberately or accidentally change the original text.

The same file can produce different token counts under two vocabularies. A shorter sequence may reduce generation steps, but that does not prove better predictions: the model may have learned rare pieces poorly, and its output layer may be larger. Compare task quality and runtime on the intended workload, not only compression on a sample file.

## One example

`unhelpful` might be one token, `un` plus `helpful`, or a sequence of letters. All three can spell the same word. If the user types `unhel` and pauses, however, the tokenizer sees a different input than it would for the finished word. An editor must test that prefix situation separately.

## Check your understanding

**Question:** Why is loss *per token* insufficient to compare tokenizers? **Answer:** The token is the denominator and its size changes. Compare loss per common unit, such as source byte, and downstream task outcomes.
