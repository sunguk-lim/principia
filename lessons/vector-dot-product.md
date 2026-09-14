# Vector dot product

## Meaning

**Goal:** combine two equal-length lists of numbers into one weighted total.

A vector here is an ordered list of numbers. The dot product multiplies matching positions and adds the results. It produces one number, not another vector. Position matters: pair the first entry with the first, and so on.

## Mechanism

Let $a$ and $b$ be vectors with $n$ entries. Their entries at position $i$ are $a_i$ and $b_i$. Then

$$a\cdot b=\sum_{i=1}^{n}a_i b_i.$$

The summation symbol means “add the products for all positions.” This uses only [[arithmetic]]. Equal lengths are required so every entry has a partner.

You can interpret one vector as measurements and the other as weights. Positive weights add a contribution; negative weights subtract one. The total therefore reflects both the size and sign of each paired contribution. A large result is not automatically evidence of similar direction: larger input magnitudes can also make it large.

## One example

For $a=[2,-1,3]$ and $b=[4,5,2]$, the paired products are $8,-5,6$. Adding them gives

$$a\cdot b=8-5+6=9.$$

Multiplying corresponding entries without adding would instead give $[8,-5,6]$. That is a different operation.

## Check your understanding

If only the last entry of $b$ changes from 2 to 4, how does the result change?

**Answer:** it increases by $3(4-2)=6$, from 9 to 15. Only the last paired contribution changes.
