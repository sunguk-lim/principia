# Singleton Pattern

## Meaning

A singleton constrains a class or service to one instance within a defined scope, which is different from global discoverability.

## Mechanism

A **singleton** constrains instance creation so clients in a chosen scope receive the same object. That scope must be stated: one Python process, one application container, or one distributed deployment are different guarantees. A [[global-object-pattern]] makes one module-held object easy to reach but does not prevent another instance of its class from being constructed.

## One example

A metrics registry has one instance per process, but three workers still have three registries.

## Check your understanding

**Question:** Does a module global guarantee a class has only one instance? **Answer:** No; it provides one shared reference but does not restrict construction.
