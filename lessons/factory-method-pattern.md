# Factory Method Pattern

## Meaning

A factory method is an overrideable creation method. A stable workflow asks that method for an object and uses the object through a shared contract; subclasses choose the concrete product.

## Mechanism

A base class can define `run()` to call `make_writer()` and then `writer.write(data)`. One subclass returns a CSV writer and another a JSON writer. Python [[object-oriented-inheritance]] makes the override possible; an [[abstract-base-class]] may define the required method. The workflow does not switch on a product string itself.

This differs from a standalone function with an `if format == ...` branch, which is a simple factory. In Python, passing a class or constructor function directly is often simpler than adding subclasses, so use the pattern only when product selection genuinely belongs to an extensible class hierarchy.

## One example

A report pipeline has fixed validation and save steps but different output writers. Each pipeline subclass overrides `make_writer()` while `run()` stays unchanged. Test the new writer without editing `run()`.

## Check your understanding

**Question:** Why might this pattern be unnecessary in Python? **Answer:** Classes and functions are first-class values, so passing a constructor can be clearer than creating subclasses solely to choose a product.
