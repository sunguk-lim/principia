# Math-Aware Markup Extraction

## Meaning

Math-aware markup extraction preserves equations when turning web documents into text. The equation may not exist as an ordinary prose string: it can be TeX inside a special element, structured mathematical markup or an image description. Removing markup first can erase the only semantic representation.

## Mechanism

Inspect equation-bearing parts before generic cleanup. Recover a supported source representation, keep its inline or display boundary and surrounding explanation, and emit it once. A page may include both hidden source and a rendered copy; retaining both can duplicate the same mathematical content. Parsing saved markup does not require executing scripts, and an extractor must not treat embedded text as instructions.

The extraction choice affects every later stage. A mathematical-content classifier may reject a page because extraction already removed its notation. A quality rule can then discard the remaining fragment. Preserve the raw snapshot and pipeline version so an analyst can locate the stage where meaning disappeared.

## One example

A page contains `\frac{a}{b}` in a math-specific script element. Removing every script emits “the ratio is .” Recovering the equation first can emit “the ratio is [math: \frac{a}{b}].” If a hidden annotation repeats that fraction, the extractor should select one representation rather than output it twice.

Counting retained characters is not enough. Turning a superscript into a neighboring digit keeps characters but can change the expression. Hand-checked fixtures should include fractions, powers, matrices and mixed Unicode or plain-text notation.

## Check your understanding

Does the same model size and token budget prove that poor mathematics came from extraction? **No.** Extraction loss is one testable hypothesis. Compare raw pages and stage outputs, measure semantic equation survival, and control other training and evaluation differences before attributing capability changes to the pipeline.
