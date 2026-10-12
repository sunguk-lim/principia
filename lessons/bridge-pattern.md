# Bridge Pattern

## Meaning

A bridge decouples two design dimensions that can change independently. One object represents the abstraction; it delegates a separate implementation concern to a collaborator.

## Mechanism

If notifications can be urgent or routine and can travel by email or SMS, creating one subclass per combination is awkward. A notification policy can instead hold a transport object. [[composition-over-inheritance]] keeps the urgency policy separate from delivery mechanics.

## One example

Add push delivery to the notification system. If the bridge is well chosen, implement one new transport and use it with both urgent and routine policies. Test the same delivery contract under success, timeout, and retry conditions.

## Check your understanding

**Question:** What makes this more than ordinary delegation? **Answer:** It is a deliberate separation of two axes that both need to vary independently.
