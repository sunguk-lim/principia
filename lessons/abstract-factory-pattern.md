# Abstract Factory Pattern

## Meaning

An abstract factory groups creation operations for related products behind one replaceable family contract.

## Mechanism

An **abstract factory** supplies a *family* of related products without clients naming their concrete classes. A rendering factory might create both a button and a dialog for one UI theme; swapping the factory changes both consistently. This differs from [[factory-method-pattern]], which delegates one creation choice to an overrideable method within a workflow.

## One example

Two themes each provide matching buttons and dialogs. One factory selects the theme as a family.

## Check your understanding

**Question:** How is this different from one factory method? **Answer:** It coordinates several related product types, not one overrideable construction point.
