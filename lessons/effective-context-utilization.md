# Effective Context Utilization

## Meaning

A large accepted input does not guarantee that a model uses its decisive evidence. Effective context utilization measures that behavior across positions, lengths and distractors. It differs from both the advertised context limit and retrieval recall.

## Mechanism

Track the evidence pipeline: the fact exists in the store, retrieval returns it, prompt assembly retains it and generation uses it correctly. Label sufficient assembled evidence separately from answer correctness. Conditional utilization accuracy is the number of correct answers among evidence-present tasks divided by the number of evidence-present tasks. It is undefined if that denominator is zero.

Compare paired inputs with the same relevant passage placed at different positions or surrounded by controlled distractors. Keep model, token budget and evaluation rubric fixed. Oracle evidence and equal-length controls help isolate hypotheses; a top-k curve alone does not prove a causal reader bottleneck.

## One example

Out of 100 tasks, retrieval depth five supplies sufficient assembled evidence for 60, of which 48 are answered correctly. Conditional accuracy is 48/60=.80. Depth twenty supplies evidence for 90, of which 54 pass: .60 conditional accuracy.

Recall improved and conditional accuracy fell, but the evidence-supported correct count rose from 48 to 54. These fractions also omit any correct answers outside the evidence-present subset. Report the full outcome and compare the common evidence-present tasks before attributing the decline to distraction: the evaluated subsets changed.

## Check your understanding

Does a decline in conditional accuracy prove that the embedding model cannot help? No. Sufficiency labels, task composition, stale evidence, truncation and generation behavior remain separate. Use paired interventions, report denominators and uncertainty, and assess answer support and total cost. A fixed retrieval budget is a measured policy choice rather than a universal law.
