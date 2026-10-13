# Composite Pattern

## Meaning

A composite gives individual objects and containers a common operation so clients can traverse a hierarchy uniformly.

## Mechanism

A **composite** represents a part-whole tree through a common operation on leaves and containers. A file and a directory can both answer a size query; the directory delegates to its children and combines their answers. [[composition-over-inheritance]] lets a container hold components rather than inherit all their implementation.

## One example

Files and directories both answer `size()`, with directories summing child results.

## Check your understanding

**Question:** What should clients not need to do for the core operation? **Answer:** Branch on whether an object is a leaf or a container.
