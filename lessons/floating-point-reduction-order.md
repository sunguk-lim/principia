# Floating-Point Reduction Order

## Meaning

Floating-point reduction order is the grouping of rounded partial sums in a machine calculation. It matters because exact addition is associative but rounded addition is not. A different answer does not automatically mean the hardware ran an unpredictable program.

## Mechanism

A parallel sum splits values among workers, combines local results, and then combines those partial results. Every intermediate addition can discard information. If small values disappear into a large partial sum before they can accumulate together, the final result may differ from another valid grouping. The operand format and the accumulator format are separate choices; do not infer the latter from the former.

A kernel may select one reduction tree for a small batch and another for a large batch. Each tree may be repeatable on its own. This is why repeating one exact batch does not establish invariance across batch shapes.

## One example

Use binary16 rounding after each addition. Near 1,024 the representable spacing is one. Adding 0.4 to 1,024 rounds back to 1,024; another 0.4 is lost again. Combining the two small represented numbers first gives about 0.7998, and adding that to 1,024 rounds to 1,025. Grouping alone changed the final machine value.

This is an arithmetic example, not evidence that a particular inference kernel accumulates in binary16. Diagnose the actual kernel before attributing output differences to this mechanism.

## Check your understanding

If a GPU sum is identical on 100 repeated fixed-shape runs, must it match a different-shaped implementation? **No.** The new shape can select another reduction tree. Test fixed-run repeatability, shape invariance and accuracy against a reference as distinct properties.
