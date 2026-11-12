# Null Object Pattern

## Meaning

A null object is a real object that responds to the expected operations with a documented neutral behavior. Instead of every caller testing for missing behavior, the system supplies an implementation whose behavior represents intentional absence. It is not merely None or an object used as a missing-value marker.

## Mechanism

Identify an interface and specify the neutral result for each operation. Through the behavioral contract associated with [[object-oriented-inheritance]], callers use the same operations on active and null implementations. Concrete inheritance is optional when a language supports structural interfaces; the key requirement is substitutable behavior, not a particular class declaration.

A logger-like object can accept emit(record) and intentionally discard the record. Python's logging NullHandler is a standard-library example of a handler that does nothing. A null cache might always miss and ignore stores, but only if those semantics are allowed by the caller's contract. Returning arbitrary success from an operation requiring a real effect is not neutral behavior.

## One example

An invented report generator calls progress.start(total), progress.advance(1) per item and progress.finish(). An interactive implementation renders progress; a null implementation accepts the same calls with no output. Processing three records still produces the same report in both cases. Returning None instead would force three call sites to guard every method call. If a caller relies on advance returning a count, the null implementation must honor that result contract too.

## Boundaries and check

Use a null object for optional behavior, not to hide broken configuration or required auditing. A missing payment processor must fail explicitly rather than behave as a successful no-op. Test the same caller against real and null implementations, including return values, exceptions and lifecycle. Distinguish a sentinel, which must be recognized by the caller, from a null object, which performs the interface's permitted neutral behavior.


## Check your understanding

Should a missing mandatory payment processor become a no-op? No; neutral behavior is valid only when the interface contract permits absence.
