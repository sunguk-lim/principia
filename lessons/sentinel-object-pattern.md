# Sentinel Object Pattern

## Meaning

A unique sentinel distinguishes an omitted value from valid data such as None.

## Mechanism

A **sentinel object** is a distinguished value whose identity means “not supplied” or “not found.” In Python, `None` works when it cannot be a legitimate value; otherwise `MISSING = object()` gives a unique identity. Check `value is MISSING`, not equality, because user-defined equality can be surprising.

## One example

A configuration map explicitly stores `None` for one key and omits another. `get(key, MISSING)` preserves the distinction.

## Check your understanding

**Question:** Why use `is` rather than `==` for a sentinel? **Answer:** Identity checks cannot be overridden by a user object’s equality method.
