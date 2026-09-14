# Matrix multiplication

## Meaning

**Goal:** determine a matrix product's shape and compute an entry using its row and column.

A matrix is a rectangular table of numbers. Matrix multiplication combines each row of the first table with each column of the second. Every pairing produces one output entry through a [[vector-dot-product]]. It is not multiplication of entries in matching table positions.

## Mechanism

Let $A$ have $m$ rows and $k$ columns, and $B$ have $k$ rows and $n$ columns. The product $C=AB$ has $m$ rows and $n$ columns. Its entry in row $i$, column $j$ is

$$C_{ij}=\sum_{r=1}^{k}A_{ir}B_{rj}.$$

Here $r$ walks across row $i$ of $A$ and down column $j$ of $B$. The shared dimension $k$ must match because those lists need equal lengths. The remaining dimensions tell us how many row–column pairs there are.

## One example

Take

$$A=\begin{bmatrix}1&2\\3&4\end{bmatrix},\qquad B=\begin{bmatrix}5\\6\end{bmatrix}.$$

The shapes are $2\times2$ and $2\times1$, so the output is $2\times1$. Its first entry is $1(5)+2(6)=17$; its second is $3(5)+4(6)=39$. Therefore $AB=[17,39]^T$, where the superscript means write the displayed list as a column.

## Check your understanding

Can you reverse these matrices and compute $BA$?

**Answer:** not for these shapes. The inner dimensions would be 1 and 2, which do not match. Even when both orders are defined, they need not produce the same result. Check shapes before calculating entries.
